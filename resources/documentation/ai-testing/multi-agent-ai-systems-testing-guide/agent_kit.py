"""Minimal multi-agent fixtures for the QAPractices testing guide.

Pure Python, no external dependencies: the goal is exercising the
interaction patterns from the guide (message validation, quorum,
tool isolation, deadlock detection, swarm stability), not a real LLM.
"""

from collections import Counter

REQUIRED_FIELDS = {"from", "payload"}


class MessageBus:
    """In-memory bus with required-field validation and seq ordering."""

    def __init__(self) -> None:
        self.queues: dict[str, list[dict]] = {}

    def validate(self, message: dict) -> None:
        missing = REQUIRED_FIELDS - message.keys()
        if missing:
            raise ValueError(f"missing required fields: {sorted(missing)}")

    def deliver(self, message: dict, to: str = "agent_a") -> None:
        self.validate(message)
        self.queues.setdefault(to, []).append(message)

    def consume(self, agent: str) -> list[dict]:
        return sorted(self.queues.pop(agent, []), key=lambda m: m["seq"])


def majority_vote(votes: list[str], required_quorum: int | None = None) -> str:
    """Return the majority vote, or 'no_consensus' below quorum."""
    if required_quorum and len(votes) < required_quorum:
        return "no_consensus"
    if not votes:
        return "no_consensus"
    return Counter(votes).most_common(1)[0][0]


class SharedTool:
    """Tool whose state is namespaced per calling agent."""

    def __init__(self) -> None:
        self._state: dict[str, object] = {}

    def use(self, agent: str, action: str, value: object = None) -> None:
        if action == "set":
            self._state[agent] = value
        else:
            raise ValueError(f"unsupported action: {action}")

    def read(self, agent: str):
        return self._state.get(agent)


def detect_deadlock(wait_for: dict[str, str]) -> dict:
    """Detect a cycle in a wait-for graph {agent: agent_it_waits_for}."""
    for start in wait_for:
        seen: set[str] = set()
        node = start
        while node in wait_for:
            if node in seen:
                return {"deadlock": True, "involved_agents": sorted(seen)}
            seen.add(node)
            node = wait_for[node]
    return {"deadlock": False, "involved_agents": []}


class Agent:
    """Dumb worker unit used by the swarm fixture."""


class SwarmSystem:
    """Toy swarm: each step nudges the global metric toward a fixed point."""

    def __init__(self, agents: list[Agent]) -> None:
        self.agents = list(agents)
        self._metric = 0.0
        self._work = 0

    def step(self) -> None:
        self._work += len(self.agents)
        self._metric += (1.0 - self._metric) * 0.5

    def global_metric(self) -> float:
        return self._metric

    def total_work_done(self) -> int:
        return self._work

    def remove_random_agent(self) -> None:
        if self.agents:
            self.agents.pop()


class Orchestrator:
    """Routes a task through named agent callables with bounded retries."""

    def __init__(self, agents: dict, max_retries: int = 2) -> None:
        self.agents = agents
        self.max_retries = max_retries

    def run(self, task: str) -> dict:
        results: dict[str, object] = {}
        for name, agent in self.agents.items():
            attempts = 0
            while True:
                try:
                    results[name] = agent(task)
                    break
                except Exception:
                    attempts += 1
                    if attempts > self.max_retries:
                        raise
        return {"status": "success", "results": results}
