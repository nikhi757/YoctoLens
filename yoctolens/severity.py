SEVERITY_MAP = {
    "Missing Provider": "High",
    "Fetch Failure": "High",
    "ABI Symbol Missing": "High",
    "Patch Failure": "Medium",
    "QA Failure": "Medium",
    "Runtime Dependency Missing": "High",
    "Circular Dependency": "High",
    "Taskhash Mismatch": "Medium",
    "Unknown": "Low"
}


SEVERITY_RANK = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}


def assign_severity(error_type):
    return SEVERITY_MAP.get(error_type, "Low")


def compute_overall_severity(failures):
    if not failures:
        return "None"

    highest = 0
    for failure in failures:
        severity = assign_severity(failure["error_type"])
        rank = SEVERITY_RANK.get(severity, 1)
        highest = max(highest, rank)

    for sev, rank in SEVERITY_RANK.items():
        if rank == highest:
            return sev

    return "Low"
