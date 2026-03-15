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


def evaluate_late_event(
    raw: str,
    max_replay_age_seconds: int,
    replay_flag_field: str,
) -> Tuple[bool, str, str]:
    """
    Return (is_eligible, key, payload_json).

    Eligibility rules:
    1) Event must contain id/order_id.
    2) If replay_flag_field exists and is false, skip.
    3) Event age based on event_time_ms must be <= max_replay_age_seconds.
    """
    event: Dict = json.loads(raw)

    order_id = str(event.get("order_id") or event.get("id") or "")
    if not order_id:
        return False, "", raw

    replay_flag = event.get(replay_flag_field, True)
    if isinstance(replay_flag, str):
        replay_flag = replay_flag.lower() == "true"
    if not replay_flag:
        return False, order_id, raw

    event_ts_ms = int(event.get("event_time_ms", 0))
    if event_ts_ms <= 0:
        return False, order_id, raw

    now_ms = int(time.time() * 1000)
    max_age_ms = max_replay_age_seconds * 1000
    if (now_ms - event_ts_ms) > max_age_ms:
        return False, order_id, raw

    event["order_id"] = order_id
    event["replay_time_ms"] = now_ms
    event["replayed_from"] = "orders-late"
    return True, order_id, json.dumps(event, separators=(",", ":"))


def build_job(
    source_bootstrap_servers: str,
    source_topic: str,
    source_group_id: str,
    sink_bootstrap_servers: str,
    sink_topic: str,
    reject_topic: str,
    max_replay_age_seconds: int,
    replay_flag_field: str,
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

    stream = env.from_source(source, watermark_strategy=None, source_name="orders-late-source")

    evaluated = stream.map(
        lambda raw: evaluate_late_event(raw, max_replay_age_seconds, replay_flag_field),
        output_type=Types.TUPLE([Types.BOOLEAN(), Types.STRING(), Types.STRING()]),
    )

    replayable = evaluated.filter(lambda r: r[0]).map(
        lambda r: (r[1], r[2]),
        output_type=Types.TUPLE([Types.STRING(), Types.STRING()]),
    )
    rejected = evaluated.filter(lambda r: not r[0]).map(
        lambda r: (r[1], r[2]),
        output_type=Types.TUPLE([Types.STRING(), Types.STRING()]),
    )

    replay_sink = (
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

    reject_sink = (
        KafkaSink.builder()
        .set_bootstrap_servers(sink_bootstrap_servers)
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic(reject_topic)
            .set_key_serialization_schema(SimpleStringSchema())
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
        .build()
    )

    replayable.sink_to(replay_sink).name("orders-late-replay-sink")
    rejected.sink_to(reject_sink).name("orders-late-rejected-sink")
    env.execute("replay-late-orders-to-msk")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consume late orders, replay eligible records to main MSK topic."
    )
    parser.add_argument("--source-bootstrap-servers", required=True)
    parser.add_argument("--source-topic", default="orders-late")
    parser.add_argument("--source-group-id", default="flink-orders-late-replayer")
    parser.add_argument("--sink-bootstrap-servers", required=True)
    parser.add_argument("--sink-topic", default="orders-by-id")
    parser.add_argument("--reject-topic", default="orders-late-rejected")
    parser.add_argument("--max-replay-age-seconds", type=int, default=604800)
    parser.add_argument(
        "--replay-flag-field",
        default="replay_allowed",
        help="If present and false, event is not replayed.",
    )
    args = parser.parse_args()

    build_job(
        source_bootstrap_servers=args.source_bootstrap_servers,
        source_topic=args.source_topic,
        source_group_id=args.source_group_id,
        sink_bootstrap_servers=args.sink_bootstrap_servers,
        sink_topic=args.sink_topic,
        reject_topic=args.reject_topic,
        max_replay_age_seconds=args.max_replay_age_seconds,
        replay_flag_field=args.replay_flag_field,
    )


if __name__ == "__main__":
    main()
