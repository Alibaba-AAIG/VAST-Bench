# Load the build environment and build widgetctl

Build widgetctl at API level 7 and save its version output to `artifacts/widgetctl-version.txt`.
Read the project-provided `incoming/vendor-env.sh` and build entry point, then run in one shell:

    source incoming/vendor-env.sh
    ./scripts/build-widgetctl
    mkdir -p artifacts
    ./build/widgetctl > artifacts/widgetctl-version.txt

The environment initializer sets the build variables locally. Check the resulting API level
and deliver the executable and matching version file.
