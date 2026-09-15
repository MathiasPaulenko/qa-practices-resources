def age_equivalence_classes(age):
    if age is None or age == "":
        return "invalid_empty"
    if not isinstance(age, int):
        return "invalid_type"
    if age < 18:
        return "invalid_minor"
    if age > 120:
        return "invalid_too_old"
    return "valid_adult"

# Test one representative from each class
test_cases = [None, "", "abc", -5, 17, 25, 65, 121, 200]
for tc in test_cases:
    print(f"age={tc!r:10} -> {age_equivalence_classes(tc)}")
