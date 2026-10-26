//! task-queue: the analytics platform's background job runner.
//!
//! Jobs arrive on an unbounded `crossbeam-channel`; a second channel carries the
//! batch-drain control signal. The worker uses `Select::new_biased` so the job
//! channel (registered first) is always drained ahead of the control signal, then
//! folds each job's contribution into a stable batch checksum the platform reconciles
//! against upstream. One batch is processed per invocation and the result is printed.
use crossbeam_channel::{unbounded, Select};

#[derive(Clone, Copy)]
struct Job {
    id: u64,
    amount: u64,
}

fn main() {
    let (job_tx, job_rx) = unbounded::<Job>();
    let (ctrl_tx, ctrl_rx) = unbounded::<()>();

    // The batch for this invocation (deterministic seed set).
    for (id, amount) in [(1u64, 4210u64), (2, 5190), (3, 3320), (4, 2710), (5, 6050)] {
        job_tx.send(Job { id, amount }).unwrap();
    }
    drop(job_tx);
    ctrl_tx.send(()).unwrap();
    drop(ctrl_tx);

    let mut processed: u64 = 0;
    let mut checksum: u64 = 0;
    loop {
        let mut sel = Select::new_biased();
        let job_op = sel.recv(&job_rx);
        let ctrl_op = sel.recv(&ctrl_rx);
        let oper = sel.select();
        let idx = oper.index();
        if idx == job_op {
            match oper.recv(&job_rx) {
                Ok(job) => {
                    processed += 1;
                    checksum = checksum.wrapping_add(job.id.wrapping_mul(job.amount));
                }
                Err(_) => break, // job channel drained + closed
            }
        } else if idx == ctrl_op {
            match oper.recv(&ctrl_rx) {
                Ok(()) => {
                    if job_rx.is_empty() {
                        break;
                    }
                }
                Err(_) => break,
            }
        }
    }

    println!("QUEUE processed={} checksum={}", processed, checksum);
}
