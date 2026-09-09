"""Parse a user story into a test outline.

Takes a standard user story format ("As a X, I want Y so that Z")
and generates a list of test cases to consider.
"""

import re
import sys


def parse_user_story(story: str) -> dict:
    """Parse a user story into actor, action, and benefit.

    Args:
        story: User story in "As a X, I want Y so that Z" format.

    Returns:
        Dict with actor, action, benefit, and test_cases.
    """
    role_match = re.search(r"As a (\w+)", story)
    action_match = re.search(r"I want to (.+?) so that", story)
    benefit_match = re.search(r"so that (.+)", story)

    role = role_match.group(1) if role_match else "user"
    action = action_match.group(1) if action_match else "perform action"
    benefit = benefit_match.group(1) if benefit_match else "achieve goal"

    test_cases = [
        f"{role} can {action}",
        f"{role} cannot {action} with invalid input",
        f"{role} receives confirmation after {action}",
        f"{role} can {action} and {benefit}",
    ]

    return {"actor": role, "action": action, "benefit": benefit, "test_cases": test_cases}


if __name__ == "__main__":
    story = sys.argv[1] if len(sys.argv) > 1 else "As a user, I want to reset my password so that I can regain access."
    result = parse_user_story(story)
    print(f"Actor: {result['actor']}")
    print(f"Action: {result['action']}")
    print(f"Benefit: {result['benefit']}")
    print("Tests:")
    for tc in result["test_cases"]:
        print(f"  - {tc}")
