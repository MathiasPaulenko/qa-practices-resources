#!/usr/bin/env bash
# AFL++ 4.30c campaign for the url_parser harness.
# Needs a main() wrapper — afl-fuzz feeds a file, so build a small driver.
set -euo pipefail

cd "$(dirname "$0")/../libfuzzer"

# 1. Instrumented build with afl-cc
afl-cc -g -O2 -I. url_parser.c ../afl/url_driver.c -o url_parser_afl

# 2. Run the campaign (Ctrl+C to stop; findings land in ./findings)
mkdir -p findings
afl-fuzz -i seeds -o findings -- ./url_parser_afl @@

# 3. After crashes appear:
#    afl-tmin findings/default/crashes/id* -- ./url_parser_afl @@
#    afl-collect -d findings -e gdb_script -- ./url_parser_afl @@
