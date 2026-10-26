#include <stdio.h>
#include "fastcsv.h"

/* csvstat — report the field count of a sample CSV record using the vendored
 * fastcsv parser, and print a build banner. */
int main(void) {
    const char *sample = "id,name,email,created_at,active";
    int fields = fastcsv_count_fields(sample);
    printf("APP_BUILD_OK csvstat fastcsv=%s fields=%d\n", FASTCSV_VERSION, fields);
    return 0;
}
