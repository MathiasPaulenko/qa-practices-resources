/* libFuzzer harness for parse_url().
 * Build: clang-18 -g -O1 -fsanitize=fuzzer,address,undefined \
 *          fuzz_url.c url_parser.c -o fuzz_url
 */
#include <stdint.h>
#include <stddef.h>
#include "url_parser.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0 || size > 4096) return 0;
    struct parsed_url out;
    parse_url((const char *)data, size, &out);
    return 0;
}
