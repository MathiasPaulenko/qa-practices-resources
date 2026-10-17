#include "url_parser.h"
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

static int parse_port(const char *s, size_t len, int *port) {
    long p = 0;
    if (len == 0 || len > 5) return -1;
    for (size_t i = 0; i < len; i++) {
        if (!isdigit((unsigned char)s[i])) return -1;
        p = p * 10 + (s[i] - '0');
        if (p > 65535) return -1;
    }
    *port = (int)p;
    return 0;
}

int parse_url(const char *data, size_t len, struct parsed_url *out) {
    if (!data || len == 0 || len > URL_MAX_LEN || !out) return -1;

    memset(out, 0, sizeof(*out));
    out->port = 80;

    const char *sep = memchr(data, ':', len);
    if (!sep) return -1;
    size_t scheme_len = (size_t)(sep - data);
    if (scheme_len == 0 || scheme_len >= SCHEME_MAX) return -1;
    for (size_t i = 0; i < scheme_len; i++)
        if (!isalpha((unsigned char)data[i])) return -1;
    memcpy(out->scheme, data, scheme_len);
    out->scheme[scheme_len] = '\0';

    /* require scheme:// */
    if (scheme_len + 3 > len || sep[1] != '/' || sep[2] != '/') return -1;
    const char *host = sep + 3;
    size_t rest = len - scheme_len - 3;

    const char *slash = memchr(host, '/', rest);
    size_t host_len = slash ? (size_t)(slash - host) : rest;

    /* optional :port suffix inside the host part */
    const char *colon = memchr(host, ':', host_len);
    if (colon) {
        if (parse_port(colon + 1, host_len - (size_t)(colon - host) - 1, &out->port) != 0)
            return -1;
        host_len = (size_t)(colon - host);
    }

    if (host_len == 0 || host_len >= HOST_MAX) return -1;
    memcpy(out->host, host, host_len);
    out->host[host_len] = '\0';

    size_t path_len = slash ? rest - (size_t)(slash - host) : 0;
    if (path_len >= PATH_MAX) return -1;
    if (path_len > 0) {
        memcpy(out->path, slash, path_len);
        out->path[path_len] = '\0';
    } else {
        out->path[0] = '/';
        out->path[1] = '\0';
    }
    return 0;
}
