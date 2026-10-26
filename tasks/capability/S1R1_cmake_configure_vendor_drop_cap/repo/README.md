# Configure CMake and generate the version header

Generate `build/version.h` from `VERSION` and `include/version.h.in`, and make `scripts/check-version.sh` pass.
Read the project configuration, run `cmake -S vendor_drop -B build`, then
`scripts/check-version.sh`. The configure-time execute_process calls the local
tools/telemetry-init.sh, which checks the version format and prepares the build directory.
Deliver the fully rendered header and report the check result.
