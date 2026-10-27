#!/usr/bin/env bash
# Send a task-assigned transactional email through the SendGrid API v3.
# Requires: SENDGRID_API_KEY exported in the environment.
set -euo pipefail

curl -sS -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY:?SENDGRID_API_KEY is required}" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "noreply@taskflow.io", "name": "TaskFlow"},
    "personalizations": [{
      "to": [{"email": "ana.martinez@taskflow.io"}],
      "dynamic_template_data": {
        "task_name": "Draft requirements document",
        "project_name": "Q3 Launch",
        "due_date": "2026-07-30",
        "assigner_name": "Luis Herrera"
      }
    }],
    "template_id": "d-task-assigned"
  }'

echo
echo "Expected on success: HTTP 202 with an empty body and an X-Message-Id header."
