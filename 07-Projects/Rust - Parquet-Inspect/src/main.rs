```rust
use parquet::file::reader::{FileReader, SerializedFileReader};
use std::fs::File;
use std::path::Path;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: parquet-inspect <file.parquet>");
        std::process::exit(1);
    }
    let path = &args[1];
    let file = File::open(path).expect("cannot open parquet file");
    let reader = SerializedFileReader::new(file).expect("failed to create reader");
    let metadata = reader.metadata();
    println!("Row groups: {}", metadata.num_row_groups());
    println!("Schema: {:?}", metadata.file_metadata().schema_descr());
}
```
