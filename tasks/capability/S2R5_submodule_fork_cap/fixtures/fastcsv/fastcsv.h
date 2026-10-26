#ifndef FASTCSV_H
#define FASTCSV_H

/* fastcsv — a tiny CSV record helper. */
#define FASTCSV_VERSION "1.4.0"

/* Count the comma-separated fields in one CSV record (no quote handling). */
int fastcsv_count_fields(const char *line);

#endif /* FASTCSV_H */
