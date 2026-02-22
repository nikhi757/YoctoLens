def classify_error(error_snippet, task=None):
    """
    Classify Yocto error based on known patterns.
    """

    joined = " ".join(error_snippet).lower()

    # Pattern-based classification
    if "nothing provides" in joined:
        return "Missing Provider"

    if "qa issue" in joined:
        return "QA Failure"

    if "requires" in joined and "no providers found" in joined:
        return "Runtime Dependency Missing"

    if "hunk failed" in joined or "patch does not apply" in joined:
        return "Patch Failure"

    if "fetcher failure" in joined or task == "do_fetch":
        return "Fetch Failure"

    if "circular dependency detected" in joined:
        return "Circular Dependency"

    if "taskhash mismatch" in joined:
        return "Taskhash Mismatch"

    if "undefined reference" in joined:
        return "ABI Symbol Missing"

    return "Unknown"
