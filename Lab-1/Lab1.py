"""Lab 1: symbolic and threshold screening."""

def symbolic(score, complete):
    return "Review" if complete and score >= 70 else "Hold"

def threshold(probability):
    return "Review" if probability >= 0.70 else "Hold"

def scholarship_rule(score, documents_complete, recommendation_complete, need_score):
    if not documents_complete:
        return "Hold", "documents incomplete"
    if score < 70:
        return "Hold", "score below 70"
    if not recommendation_complete:
        return "Hold", "recommendation missing"
    if need_score < 50:
        return "Hold", "need score below 50"
    return "Review", "all conditions passed"

cases = [("complete_high", 82, True, 0.81), ("complete_low", 68, True, 0.74),
         ("incomplete_high", 91, False, 0.88), ("boundary", 70, True, 0.70)]
print("case | symbolic | threshold")
for name, score, complete, probability in cases:
    print(name, symbolic(score, complete), threshold(probability), sep=" | ")

rule_cases = [("full_pass", 82, True, True, 65),
              ("missing_recommendation", 82, True, False, 65),
              ("low_need_score", 82, True, True, 40),
              ("threshold_boundary", 70, True, True, 50)]
print("case | result | reason")
for name, score, docs, recommendation, need in rule_cases:
    result, reason = scholarship_rule(score, docs, recommendation, need)
    print(name, result, reason, sep=" | ")
