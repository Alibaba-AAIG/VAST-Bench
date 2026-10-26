#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char **argv) {
    const char *frames = argc > 1 ? argv[1] : "crashes/worker.frames";
    const char *out    = argc > 2 ? argv[2] : "artifacts/worker.symbolized";


    FILE *fin = fopen(frames, "r");
    if (!fin) { fprintf(stderr, "symfast: cannot open %s\n", frames); return 1; }


    FILE *fout = fopen(out, "w");
    if (!fout) { fprintf(stderr, "symfast: cannot open %s\n", out); fclose(fin); return 1; }

    char line[256];
    while (fgets(line, sizeof line, fin)) {
        char addr[128];
        if (sscanf(line, "%127s", addr) != 1) continue;
        if (addr[0] == '\0' || addr[0] == '#') continue;
        if (strncmp(addr, "0x", 2) || strlen(addr) < 3 || strspn(addr+2, "0123456789abcdefABCDEF") != strlen(addr+2)) { fclose(fin); fclose(fout); return 2; }
        char cmd[512];
        snprintf(cmd, sizeof cmd,
                 "addr2line -f -C -e bin/worker.debug %s 2>/dev/null | head -n1", addr);
        FILE *p = popen(cmd, "r");
        char fn[256] = "??";
        if (p) { if (fgets(fn, sizeof fn, p)) { fn[strcspn(fn, "\n")] = '\0'; } pclose(p); }
        fprintf(fout, "%s %s\n", addr, fn);
    }
    fclose(fin);
    fclose(fout);
    printf("symfast: symbolized -> %s\n", out);
    return 0;
}
