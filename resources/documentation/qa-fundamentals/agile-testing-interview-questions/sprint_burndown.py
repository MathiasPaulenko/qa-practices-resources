"""Sprint burndown tracker: QA effort alongside dev tasks."""

sprint_tasks = [
    {"name": "Login feature", "dev_hours": 8, "qa_hours": 4, "done": True},
    {"name": "Payment fix", "dev_hours": 3, "qa_hours": 2, "done": True},
    {"name": "Search refactor", "dev_hours": 10, "qa_hours": 6, "done": False},
]

total_qa = sum(t["qa_hours"] for t in sprint_tasks)
qa_done = sum(t["qa_hours"] for t in sprint_tasks if t["done"])
print(f"QA progress: {qa_done}/{total_qa} hours ({100 * qa_done / total_qa:.0f}%)")
