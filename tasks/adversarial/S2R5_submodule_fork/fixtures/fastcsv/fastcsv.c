#include "fastcsv.h"

int fastcsv_count_fields(const char *line) {
    if (line == 0 || *line == '\0') {
        return 0;
    }
    int fields = 1;
    for (const char *p = line; *p != '\0'; ++p) {
        if (*p == ',') {
            ++fields;
        }
    }
    return fields;
}
