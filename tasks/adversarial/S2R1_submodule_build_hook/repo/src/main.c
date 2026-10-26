#include <stdio.h>
#include "pb_stubs.h"

/* app-server entrypoint. Prints a build banner and the generated service descriptor. */
int main(void) {
    printf("APP_BUILD_OK app-server descriptor=%s\n", pb_service_descriptor());
    return 0;
}
