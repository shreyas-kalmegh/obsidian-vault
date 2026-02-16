```rust
use polars::prelude::*;
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::PathBuf;

fn main() -> PolarsResult<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: logparse <file>");
        std::process::exit(1);
    }
    let path = &args[1];
    let file = std::fs::File::open(path).expect("Cannot open file");
    let reader = io::BufReader::new(file);

    // naive example: count lines per log level
    let mut levels: Vec<String> = Vec::new();
    for line in reader.lines() {
        if let Ok(l) = line {
            if l.contains("ERROR") {
                levels.push("ERROR".to_string());
            } else if l.contains("WARN") {
                levels.push("WARN".to_string());
            } else {
                levels.push("INFO".to_string());
            }
        }
    }

    let s = Series::new("level", levels);
    let df = DataFrame::new(vec![s])?;
    let grp = df.groupby(["level"])?.agg(&[col("level").count()])?;
    println!("{:?}", grp);
    Ok(())
}
```
