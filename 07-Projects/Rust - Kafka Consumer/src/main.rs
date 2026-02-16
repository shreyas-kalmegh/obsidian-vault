```rust
use rdkafka::consumer::{Consumer, StreamConsumer};
use rdkafka::config::ClientConfig;
use rdkafka::Message;
use futures::StreamExt;
use std::time::Duration;

#[tokio::main]
async fn main() {
    let consumer: StreamConsumer = ClientConfig::new()
        .set("group.id", "personal_rust_consumer")
        .set("bootstrap.servers", "localhost:9092")
        .set("enable.partition.eof", "false")
        .create()
        .expect("Consumer creation failed");

    consumer.subscribe(&["test_topic"]).expect("subscribe failed");

    let mut message_stream = consumer.stream();
    while let Some(message) = message_stream.next().await {
        match message {
            Ok(m) => {
                if let Some(payload) = m.payload_view::<str>().ok().flatten() {
                    println!("Received: {}", payload);
                }
            }
            Err(e) => {
                eprintln!("Kafka error: {}", e);
            }
        }
    }
}
```
