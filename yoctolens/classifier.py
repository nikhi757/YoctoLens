def classify_error(error_snippet):
    """
    Classify Yocto error based on known patterns.
    """

    if not error_snippet:
        return "Unknown"

    joined = " ".join(error_snippet)

    rules = {
        "Missing Provider": [
            "Nothing PROVIDES"
        ],
        "Runtime Dependency Missing": [
            "requires",
            "no providers found"
        ],
        "QA Failure": [
            "QA Issue"
        ],
        "Patch Failure": [
            "Hunk FAILED",
            "patch does not apply"
        ],
        "Fetch Failure": [
            "do_fetch",
            "Fetcher failure"
        ],
        "Circular Dependency": [
            "Circular dependency detected"
        ],
        "Taskhash Mismatch": [
            "Taskhash mismatch"
        ],
        "ABI Symbol Missing": [
            "undefined reference"
        ],
    }

    for category, patterns in rules.items():
        if all(p.lower() in joined.lower() for p in patterns):
            return category

    return "Unknown"
