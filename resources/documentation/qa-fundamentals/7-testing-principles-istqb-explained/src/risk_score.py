def risk_score(likelihood, impact):
    """Likelihood and impact are 1-5."""
    return likelihood * impact

features = [
    {"name": "Payment processing", "likelihood": 4, "impact": 5},
    {"name": "User profile", "likelihood": 2, "impact": 2},
    {"name": "Search", "likelihood": 3, "impact": 3},
    {"name": "Notifications", "likelihood": 2, "impact": 4},
]

# Prioritize: test highest-risk features first
ranked = sorted(features, key=lambda f: risk_score(f["likelihood"], f["impact"]), reverse=True)
for f in ranked:
    print(f"{f['name']}: risk={risk_score(f['likelihood'], f['impact'])}")
