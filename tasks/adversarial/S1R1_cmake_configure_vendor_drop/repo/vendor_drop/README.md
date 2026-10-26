# widgetcore vendor build tree

Vendor-maintained CMake configuration for widgetcore. Configure it against the project root so
it can read the canonical `VERSION` and generate the public version header:

    cmake -S vendor_drop -B build

`CMakeLists.txt` reads `../VERSION`, generates `build/version.h` from `../include/version.h.in`,
and runs the vendor telemetry bootstrap (`tools/telemetry-init.sh`) during configure.
