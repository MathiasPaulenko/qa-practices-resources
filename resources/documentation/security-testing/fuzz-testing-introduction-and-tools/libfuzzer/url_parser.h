#ifndef URL_PARSER_H
#define URL_PARSER_H

#include <stddef.h>

#define URL_MAX_LEN 1024
#define SCHEME_MAX 16
#define HOST_MAX 256
#define PATH_MAX 512

struct parsed_url {
    char scheme[SCHEME_MAX];
    char host[HOST_MAX];
    char path[PATH_MAX];
    int port;
};

/* Parses `len` bytes of `data` as a URL into `out`.
 * Returns 0 on success, -1 on malformed input. */
int parse_url(const char *data, size_t len, struct parsed_url *out);

#endif
