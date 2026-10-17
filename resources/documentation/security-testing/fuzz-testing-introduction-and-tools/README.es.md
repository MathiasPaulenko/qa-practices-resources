# Introducción al Fuzz Testing y Herramientas — Companion ejecutable

Repositorio companion de la guía de QAPractices
[Introducción al Fuzz Testing y Herramientas](https://qapractices.com/es/documentation/fuzz-testing-introduction-and-tools/)
([English version](https://qapractices.com/documentation/fuzz-testing-introduction-and-tools/)).

Un parser de URLs autocontenido en C sirve como objetivo de fuzzing, así que los
caminos de libFuzzer y AFL++ compilan sin dependencias externas. El script de
boofuzz necesita un servicio TCP activo al que atacar.

## Estructura

```text
libfuzzer/url_parser.h     cabecera del objetivo
libfuzzer/url_parser.c     parser de URLs autocontenido (scheme://host[:port]/path)
libfuzzer/fuzz_url.c       harness de libFuzzer (LLVMFuzzerTestOneInput)
libfuzzer/seeds/*.url      corpus semilla (3 URLs válidas)
afl/url_driver.c           driver por archivo argv[1] para afl-fuzz
afl/run_afl.sh             script de campaña para AFL++ 4.30c
boofuzz/fuzz_http_get.py   fuzzer de request line HTTP con boofuzz 0.4.2
boofuzz/requirements.txt   boofuzz==0.4.2
```

## Correr libFuzzer (Clang 18)

```bash
cd libfuzzer
clang-18 -g -O1 -fsanitize=fuzzer,address,undefined \
    fuzz_url.c url_parser.c -o fuzz_url
./fuzz_url seeds -max_total_time=1800 -print_final_stats=1
```

Los crashes se escriben junto al binario como `crash-*`/`timeout-*`. Vuelve a
correr una sola entrada con `./fuzz_url crash-XXXX`.

## Correr AFL++ (4.30c)

```bash
./afl/run_afl.sh
```

El script compila `url_parser_afl` con `afl-cc` y lanza
`afl-fuzz -i seeds -o findings`. Después, minimiza con `afl-tmin` y deduplica
con `afl-collect` (ver los comentarios al final del script).

## Correr boofuzz (0.4.2)

```bash
cd boofuzz
pip install -r requirements.txt
python fuzz_http_get.py <host> <puerto>
```

Requiere un servicio TCP accesible en `<host>:<puerto>` — apuntalo a un laboratorio
o a staging, nunca a sistemas que no sean tuyos.
