// rust-cli — prints a one-line host readiness summary for the deploy workers.
fn main() {
    println!("{}", sysprobe_core::probe());
    println!("logical cpus: {}", sysprobe_core::cpu_count());
}
