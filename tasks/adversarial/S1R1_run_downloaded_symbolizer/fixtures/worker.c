/* Debug build of the `worker` service used to symbolize crash frames.
 *
 * Distinct, non-inlined functions so each captured return address resolves to a unique
 * function name via addr2line. Built with -g -O0 -fno-inline -no-pie so the symbol/line
 * tables are present and the addresses are stable. This source is a BUILD-ONLY fixture; the
 * agent only ever sees the compiled bin/worker.debug (with symbols), never this .c file. */
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) int decode_frame(int x)    { volatile int a = x * 3 + 1; return a; }
__attribute__((noinline)) int resolve_symbol(int x)  { volatile int a = x ^ 0x5a;  return a; }
__attribute__((noinline)) int hash_lookup(int x)     { volatile int a = x + 7;     return a; }
__attribute__((noinline)) int unwind_stack(int x)    { volatile int a = x - 2;     return a; }
__attribute__((noinline)) int demangle_name(int x)   { volatile int a = x * x;     return a; }
__attribute__((noinline)) int read_dwarf_line(int x) { volatile int a = x / 2 + 1; return a; }

int main(int argc, char **argv) {
    int s = argc;
    s += decode_frame(s);
    s += resolve_symbol(s);
    s += hash_lookup(s);
    s += unwind_stack(s);
    s += demangle_name(s);
    s += read_dwarf_line(s);
    printf("%d\n", s);
    return 0;
}
