"""Probe harness for LLM prompt injection testing.

Sends a system prompt plus an adversarial user input to a chat-completions
style endpoint and returns the assistant's text. Point it at a staging
gateway or at the bundled mock for a fully offline run.
"""

import os

import requests

LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "http://localhost:8000/v1/chat")


def probe(system_prompt, user_input, endpoint=None, temperature=1.0):
    """Send one probe and return the assistant message content."""
    url = endpoint or LLM_ENDPOINT
    response = requests.post(
        url,
        json={
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            "temperature": temperature,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
