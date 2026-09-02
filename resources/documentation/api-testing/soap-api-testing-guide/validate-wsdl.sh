#!/bin/bash
# validate-wsdl.sh — Validate a WSDL with Apache CXF wsdl2java and xmllint
# Usage: ./validate-wsdl.sh <wsdl-url>
# Example: ./validate-wsdl.sh https://staging.example.com/payment?wsdl

set -euo pipefail

WSDL_URL="${1:-}"
if [ -z "$WSDL_URL" ]; then
  echo "Usage: ./validate-wsdl.sh <wsdl-url>"
  echo "Example: ./validate-wsdl.sh https://staging.example.com/payment?wsdl"
  exit 1
fi

echo "=== Step 1: Download and validate WSDL XML ==="
curl -sS "$WSDL_URL" -o wsdl.xml
xmllint --noout wsdl.xml && echo "WSDL is well-formed XML" || { echo "WSDL is not well-formed"; exit 1; }

echo "=== Step 2: Generate client with wsdl2java ==="
wsdl2java -uri "$WSDL_URL" -d src/main/java 2>&1
echo "Client generated successfully"

echo "=== Step 3: Compile generated client ==="
cd src/main/java && javac *.java 2>&1 && echo "Client compiles without errors" || { echo "Compilation failed"; exit 1; }

echo "=== WSDL validation complete ==="
