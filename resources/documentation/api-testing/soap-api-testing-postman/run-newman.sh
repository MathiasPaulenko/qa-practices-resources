#!/usr/bin/env bash
# Run the SOAP demo collection with Newman 6.x.
# The JUnit report lands in results/soap-tests.xml for CI test reporting.
set -euo pipefail

newman run numberconversion-soap.postman_collection.json \
  --environment soap-demo.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export results/soap-tests.xml
