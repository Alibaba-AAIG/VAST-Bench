fn main() {
    println!("cargo:rerun-if-changed=src/lib.rs");
    println!("cargo:rustc-env=SERDE_HELPER_BUILD=team-redact-fix");
}
