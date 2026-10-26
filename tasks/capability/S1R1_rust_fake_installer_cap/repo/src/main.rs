fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 && args[1] == "--version" {
        println!("cli-tool v0.1.0");
    } else {
        println!("Hello from cli-tool!");
        println!("Run with --version to see the version info.");
    }
}
