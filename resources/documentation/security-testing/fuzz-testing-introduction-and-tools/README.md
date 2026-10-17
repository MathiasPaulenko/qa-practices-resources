# Fuzz Testing Introduction and Tools — Runnable Companion

Companion repository for the QAPractices guide
[Fuzz Testing Introduction and Tools](https://qapractices.com/documentation/fuzz-testing-introduction-and-tools/)
([versión en español](https://qapractices.com/es/documentation/fuzz-testing-introduction-and-tools/)).

A self-contained C URL parser serves as the fuzz target, so the libFuzzer and
AFL++ paths compile with no external dependencies. The boofuzz script needs a
live TCP service to attack.

## Layout

```text
libfuzzer/url_parser.h     fuzz target header
libfuzzer/url_parser.c     self-contained URL parser (scheme://host[:port]/path)
libfuzzer/fuzz_url.c       libFuzzer harness (LLVMFuzzerTestOneInput)
libfuzzer/seeds/*.url      seed corpus (3 valid URLs)
afl/url_driver.c           argv[1] file driver for afl-fuzz
afl/run_afl.sh             AFL++ 4.30c campaign script
boofuzz/fuzz_http_get.py   boofuzz 0.4.2 HTTP request-line fuzzer
boofuzz/requirements.txt   boofuzz==0.4.2
```

## Run libFuzzer (Clang 18)

```bash
cd libfuzzer
clang-18 -g -O1 -fsanitize=fuzzer,address,undefined \
    fuzz_url.c url_parser.c -o fuzz_url
./fuzz_url seeds -max_total_time=1800 -print_final_stats=1
```

Crashes are written next to the binary as `crash-*`/`timeout-*` files. Re-run a
single input with `./fuzz_url crash-XXXX`.

## Run AFL++ (4.30c)

```bash
./afl/run_afl.sh
```

The script builds `url_parser_afl` with `afl-cc` and launches
`afl-fuzz -i seeds -o findings`. Afterwards, minimize with `afl-tmin` and dedupe
with `afl-collect` (see the comments at the bottom of the script).

## Run boofuzz (0.4.2)

```bash
cd boofuzz
pip install -r requirements.txt
python fuzz_http_get.py <host> <port>
```

Requires a reachable TCP service on `<host>:<port>` — point it at a lab or
staging target, never at systems you do not own.
