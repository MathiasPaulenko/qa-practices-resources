#!/bin/bash
# Generate RSA key pair for JWT testing
set -e

openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
echo "Generated private.pem and public.pem"
