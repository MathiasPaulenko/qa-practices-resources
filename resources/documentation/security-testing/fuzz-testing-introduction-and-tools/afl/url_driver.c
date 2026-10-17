/* afl-fuzz driver: read the input file given as argv[1] and run parse_url on it. */
#include <stdio.h>
#include <stdlib.h>
#include "url_parser.h"

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    char buf[4096];
    size_t n = fread(buf, 1, sizeof(buf), f);
    fclose(f);
    struct parsed_url out;
    parse_url(buf, n, &out);
    return 0;
}
