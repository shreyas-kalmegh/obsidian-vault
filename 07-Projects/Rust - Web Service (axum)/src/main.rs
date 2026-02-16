```rust
use axum::{routing::get, Router};
use std::net::SocketAddr;

async fn root() -> &'static str {
    "Personal Rust Service"
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(root));
    let addr = SocketAddr::from(([127,0,0,1], 3000));
    println!("Listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```
