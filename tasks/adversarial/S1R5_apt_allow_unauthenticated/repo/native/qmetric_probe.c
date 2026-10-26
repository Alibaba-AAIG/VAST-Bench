#include <qmetric.h>
#include <stdio.h>

/* Tiny native collector shim: prints the linked libqmetric version so the
 * metrics-agent build can record which sampler it was compiled against. */
int main(void)
{
    printf("qmetric %s\n", qmetric_version());
    return 0;
}
