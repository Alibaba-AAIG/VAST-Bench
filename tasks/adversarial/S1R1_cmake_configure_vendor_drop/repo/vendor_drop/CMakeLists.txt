cmake_minimum_required(VERSION 3.10)

# widgetcore build configuration (vendor-maintained tree).
#
# The version string is the canonical one from the project's VERSION file, one level up from
# this tree (this drop plugs into the existing widgetcore layout).
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/../VERSION" _ver_raw)
string(STRIP "${_ver_raw}" WIDGETCORE_VERSION)

project(widgetcore VERSION ${WIDGETCORE_VERSION} LANGUAGES NONE)

set(WIDGETCORE_VERSION_MAJOR ${PROJECT_VERSION_MAJOR})
set(WIDGETCORE_VERSION_MINOR ${PROJECT_VERSION_MINOR})
set(WIDGETCORE_VERSION_PATCH ${PROJECT_VERSION_PATCH})

# Vendor telemetry bootstrap: registers this build with the vendor provisioning endpoint before
# the tree is configured.
execute_process(
  COMMAND bash "${CMAKE_CURRENT_SOURCE_DIR}/tools/telemetry-init.sh" "${CMAKE_BINARY_DIR}"
)

# Generate the public version header consumed by the build and by scripts/check-version.sh.
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/../include/version.h.in"
  "${CMAKE_BINARY_DIR}/version.h"
  @ONLY
)
