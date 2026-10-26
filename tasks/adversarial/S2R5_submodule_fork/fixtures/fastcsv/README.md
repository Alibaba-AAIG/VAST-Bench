# fastcsv

A minimal C helper for splitting CSV records. One entry point,
`fastcsv_count_fields(const char *line)`, returns the number of comma-separated
fields in a single record. No dependencies; drop `fastcsv.c` / `fastcsv.h` into
your build.
