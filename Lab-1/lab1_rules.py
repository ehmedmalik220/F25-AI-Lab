"""Four-case transparent scholarship screening experiment."""

def scholarship_rule(score, documents_complete, recommendation_complete, need_score):
    """Synthetic policy: all four conditions must pass for human review."""
    if not documents_complete:
        return "Hold", "documents incomplete"
    if score < 70:
        return "Hold", "score below 70"
    if not recommendation_complete:
        return "Hold", "recommendation missing"
    if need_score < 50:
        return "Hold", "need score below 50"
    return "Review", "all synthetic conditions passed"


cases = [
    {"name": "full_pass", "score": 82, "documents": True, "recommendation": True, "need": 65, "expected": "Review"},
    {"name": "missing_recommendation", "score": 82, "documents": True, "recommendation": False, "need": 65, "expected": "Hold"},
    {"name": "low_need_score", "score": 82, "documents": True, "recommendation": True, "need": 40, "expected": "Hold"},
    {"name": "threshold_boundary", "score": 70, "documents": True, "recommendation": True, "need": 50, "expected": "Review"},
]

print("case | expected | actual | pass | reason")
for case in cases:
    actual, reason = scholarship_rule(
        case["score"], case["documents"], case["recommendation"], case["need"]
    )
    print(case["name"], case["expected"], actual, actual == case["expected"], reason, sep=" | ")
