import argparse
import json
import time
from typing import Dict, Tuple

from pyflink.common import Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaRecordSerializationSchema,
    KafkaSink,
    KafkaSource,
)


def parse_order(raw: str, event_time_field: str, late_threshold_seconds: int) -> Tuple[str, str, bool]:
    """
    Parse input JSON order event and return (id_as_key, normalized_json_value, is_late).
    Expected input contains an integer/string "id" field.
    """
    event: Dict = json.loads(raw)
    if "id" not in event or event["id"] is None:
        raise ValueError(f"Missing required order id in event: {raw}")

    order_id = str(event["id"])
    event_ts_ms = int(event.get(event_time_field, 0))
    ingest_ts_ms = int(time.time() * 1000)
    is_late = event_ts_ms > 0 and (ingest_ts_ms - event_ts_ms) > (late_threshold_seconds * 1000)

    # Add metadata that Pinot can use for hybrid upsert/ordering.
    event["order_id"] = order_id
    event["event_time_ms"] = event_ts_ms
    event["ingest_time_ms"] = ingest_ts_ms
    normalized = json.dumps(event, separators=(",", ":"))
    return order_id, normalized, is_late


def build_job(
    source_bootstrap_servers: str,
    source_topic: str,
    source_group_id: str,
    sink_bootstrap_servers: str,
    sink_topic: str,
    late_topic: str,
    event_time_field: str,
    late_threshold_seconds: int,
) -> None:
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(3)

    source = (
        KafkaSource.builder()
        .set_bootstrap_servers(source_bootstrap_servers)
        .set_topics(source_topic)
        .set_group_id(source_group_id)
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )

    stream = env.from_source(source, watermark_strategy=None, source_name="orders-source")

    parsed = (
        stream.map(
            lambda raw: parse_order(raw, event_time_field, late_threshold_seconds),
            output_type=Types.TUPLE([Types.STRING(), Types.STRING(), Types.BOOLEAN()]),
        )
        # Logical repartition in Flink by order id.
        .key_by(lambda kv: kv[0], key_type=Types.STRING())
    )

    on_time = (
        parsed.filter(lambda kv: not kv[2]).map(
            lambda kv: (kv[0], kv[1]),
            output_type=Types.TUPLE([Types.STRING(), Types.STRING()]),
        )
    )
    late = (
        parsed.filter(lambda kv: kv[2]).map(
            lambda kv: (kv[0], kv[1]),
            output_type=Types.TUPLE([Types.STRING(), Types.STRING()]),
        )
    )

    sink = (
        KafkaSink.builder()
        .set_bootstrap_servers(sink_bootstrap_servers)
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic(sink_topic)
            .set_key_serialization_schema(SimpleStringSchema())
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
        .build()
    )

    late_sink = (
        KafkaSink.builder()
        .set_bootstrap_servers(sink_bootstrap_servers)
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic(late_topic)
            .set_key_serialization_schema(SimpleStringSchema())
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
        .build()
    )

    on_time.sink_to(sink).name("orders-id-partitioned-sink")
    late.sink_to(late_sink).name("orders-late-events-sink")
    env.execute("repartition-orders-by-id-to-msk")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read orders from Kafka, repartition by id, and write to MSK topic."
    )
    parser.add_argument("--source-bootstrap-servers", required=True)
    parser.add_argument("--source-topic", required=True)
    parser.add_argument("--source-group-id", default="flink-orders-repartitioner")
    parser.add_argument("--sink-bootstrap-servers", required=True)
    parser.add_argument("--sink-topic", required=True)
    parser.add_argument("--late-topic", default="orders-late")
    parser.add_argument(
        "--event-time-field",
        default="event_time_ms",
        help="Field in source JSON payload used to detect late events.",
    )
    parser.add_argument(
        "--late-threshold-seconds",
        type=int,
        default=900,
        help="Event is marked late if processing_time - event_time exceeds this threshold.",
    )
    args = parser.parse_args()

    build_job(
        source_bootstrap_servers=args.source_bootstrap_servers,
        source_topic=args.source_topic,
        source_group_id=args.source_group_id,
        sink_bootstrap_servers=args.sink_bootstrap_servers,
        sink_topic=args.sink_topic,
        late_topic=args.late_topic,
        event_time_field=args.event_time_field,
        late_threshold_seconds=args.late_threshold_seconds,
    )


if __name__ == "__main__":
    main()
