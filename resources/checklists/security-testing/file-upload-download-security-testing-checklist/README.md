# File Upload and Download Security Testing Checklist — Companion

Companion files for [File Upload and Download Security Testing Checklist](https://qapractices.com/checklists/file-upload-download-security-testing-checklist).

## Contents

| File | Description |
|---|---|
| `upload-payloads.csv` | 20 adversarial upload/download payloads — extension bypass, null bytes, MIME spoofing, magic-byte mismatch, path traversal, zip slip, SVG/HTML XSS, EICAR, download authz |

## Usage

Import the CSV into your test tracking tool or feed rows to a script loop:

```bash
# Send each traversal payload to a download endpoint
tail -n +2 upload-payloads.csv | grep traversal | cut -d, -f3 | while read p; do
  curl -s -o /dev/null -w "$p -> %{http_code}\n" "https://staging.example.io/download?file=$p"
done
```

Expected: every payload row maps to a rejection, sanitization or safe-serve behavior — never an accepted dangerous file.
