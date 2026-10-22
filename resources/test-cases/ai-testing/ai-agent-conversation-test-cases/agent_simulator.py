"""Deterministic model of an LLM agent conversation turn.

Stands in for the real pipeline (guardrails -> intent -> tool call -> response
-> context store) so the test cases from the article can run offline. The real
implementation would call a model API; here each behavior is a rule so the
tests exercise the contract, not the probabilities.
"""

from __future__ import annotations

import re

INJECTION_MARKERS = (
    "ignore all previous instructions",
    "ignore previous instructions",
    "ignore the above",
    "reveal your system prompt",
    "tell me the system prompt",
)

HARMFUL_MARKERS = ("hack", "exploit", "malware")

REQUIRED_FLIGHT_PARAMS = ("origin", "destination", "date")


class ToolError(Exception):
    pass


class ToolRegistry:
    """Tools the agent can call; failures are injected per tool name."""

    def __init__(self) -> None:
        self.fail: set[str] = set()

    def weather(self, location: str) -> dict:
        if "weather" in self.fail:
            raise ToolError("timeout")
        return {"location": location, "temp_c": 22, "condition": "clear"}

    def flight_search(self, **params: str) -> dict:
        missing = [p for p in REQUIRED_FLIGHT_PARAMS if not params.get(p)]
        if missing:
            raise ToolError(f"missing params: {', '.join(missing)}")
        if "flight_search" in self.fail:
            raise ToolError("HTTP 500")
        return {"flights": [{"id": "FL-1", **params}]}


class AgentSimulator:
    """Session-scoped agent with context, tool use and guardrails."""

    def __init__(self, tools: ToolRegistry | None = None, max_turns_loop: int = 3) -> None:
        self.tools = tools or ToolRegistry()
        self.max_turns_loop = max_turns_loop
        self._sessions: dict[str, list[tuple[str, str]]] = {}

    def send_message(self, session_id: str, message: str) -> str:
        history = self._sessions.setdefault(session_id, [])
        response = self._respond(history, message)
        history.append(("user", message))
        history.append(("agent", response))
        return response

    def _respond(self, history: list[tuple[str, str]], message: str) -> str:
        text = message.strip()
        lower = text.lower()

        if not text:
            return "I didn't receive a message — what would you like to ask?"

        if any(marker in lower for marker in INJECTION_MARKERS):
            return "I can't share or modify my instructions. How can I help you otherwise?"

        if any(marker in lower for marker in HARMFUL_MARKERS):
            return "I can't help with that. If you're interested in security, try an ethical hacking course."

        if self._is_repeat(history, lower):
            return "You asked the same thing several times — can you rephrase or should I escalate to a human agent?"

        name, city = self._recall_identity(history)
        if "my name is" in lower or "me llamo" in lower:
            return "Got it, I'll remember that."
        if "what is my name" in lower or "cómo me llamo" in lower:
            if name and city:
                return f"You're {name} and you live in {city}."
            return "You haven't told me your name yet."

        if "weather" in lower or "clima" in lower:
            return self._handle_weather(lower)

        if "flight" in lower or "vuelo" in lower:
            return self._handle_flight(lower)

        if "speak to a human" in lower or "hablar con un humano" in lower:
            return "Transferring you now — estimated wait time 3 minutes. Your history travels with you."

        if lower in ("hello", "hi", "hola") or "how are you" in lower:
            return "Hello! How can I help you today?"

        return "Let me check that for you."

    def _handle_weather(self, lower: str) -> str:
        m = re.search(r"weather in ([a-zA-Z ]+?)(?:\s+right now|\s+now)?[?.!]*$", lower) or \
            re.search(r"clima en ([a-zA-Z ]+?)[?.!]*$", lower)
        location = m.group(1).strip().title() if m else "Unknown"
        try:
            data = self.tools.weather(location)
        except ToolError:
            return "The weather service is unavailable right now — want me to retry in a bit?"
        return f"Current weather in {data['location']}: {data['temp_c']}°C, {data['condition']}."

    def _handle_flight(self, lower: str) -> str:
        params: dict[str, str] = {}
        to = re.search(r"(?:to|a)\s+([a-zA-Z ]+?)(?:\s+on|\s+el|\s+for|\s+para|\?|\.)", lower)
        on = re.search(r"(?:on|el)\s+([a-zA-Z0-9 ]+?)(?:\s+for|\s+para|\?|\.)", lower)
        frm = re.search(r"from ([a-zA-Z ]+?)\s+to", lower) or \
            re.search(r"de ([a-zA-Z ]+?)\s+a", lower)
        if frm:
            params["origin"] = frm.group(1).strip().title()
        if to:
            params["destination"] = to.group(1).strip().title()
        if on:
            params["date"] = on.group(1).strip()
        try:
            result = self.tools.flight_search(**params)
        except ToolError as err:
            if "missing params" in str(err):
                return "Sure — what's the origin airport and the date?"
            return "The flight search is unavailable right now — I can't fabricate prices."
        return f"Found a flight: {result['flights'][0]['id']} {params['origin']} to {params['destination']}."

    def _is_repeat(self, history: list[tuple[str, str]], lower: str) -> bool:
        recent = [m for role, m in history[-self.max_turns_loop * 2:] if role == "user"]
        return len(recent) >= self.max_turns_loop and all(m.lower() == lower for m in recent[-self.max_turns_loop:])

    @staticmethod
    def _recall_identity(history: list[tuple[str, str]]) -> tuple[str | None, str | None]:
        name = city = None
        for role, message in history:
            if role != "user":
                continue
            m = re.search(r"my name is ([a-zA-Z]+)", message.lower())
            if m:
                name = m.group(1).title()
            m = re.search(r"(?:i live in|vivo en) ([a-zA-Z ]+)", message.lower())
            if m:
                city = m.group(1).strip().title()
        return name, city
