```rust
use polars::prelude::*;
fn main() -> PolarsResult<()> {
    let df = df![
        "id" => &[1,2,3,4],
        "value" => &[10,20,30,40]
    ]?;
    let filtered = df.lazy().filter(col("value").gt(lit(15))).collect()?;
    println!("{:?}", filtered);
    Ok(())
}
```
