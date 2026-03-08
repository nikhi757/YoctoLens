import re


SUGGESTION_MAP = {
    "Fetch Failure": (
        "Check SRC_URI and network access. "
        "Verify that the source URL is reachable."
    ),

    "ABI Symbol Missing": (
        "Missing symbol during linking. "
        "Ensure the correct library dependency is added "
        "to DEPENDS or RDEPENDS."
    ),

    "Patch Failure": (
        "Patch failed to apply. "
        "Refresh patch using 'devtool modify' or quilt."
    ),

    "QA Failure": (
        "Review QA issue and adjust packaging rules "
        "(FILES, RDEPENDS, INSANE_SKIP)."
    ),
}


# -----------------------------
# Entity Extraction Helpers
# -----------------------------

def extract_missing_provider(error_snippet):
    for line in error_snippet:
        match = re.search(r"Nothing PROVIDES '([^']+)'", line)
        if match:
            return match.group(1)
    return None


def extract_runtime_dependency(error_snippet):
    for line in error_snippet:
        match = re.search(r"requires\s+/(?:usr/)?bin/([a-zA-Z0-9_\-]+)", line)
        if match:
            return match.group(1)
    return None


# -----------------------------
# Suggestion Rules
# -----------------------------

def missing_provider_rule(failure):
    snippet = failure.get("error_snippet", [])

    pkg = extract_missing_provider(snippet)

    if pkg:
        return (
            f"Package '{pkg}' is missing.\n"
            f"Add dependency in recipe:\n"
            f"    RDEPENDS:${{PN}} += \"{pkg}\""
        )

    return None


def runtime_dependency_rule(failure):
    snippet = failure.get("error_snippet", [])

    dep = extract_runtime_dependency(snippet)

    if dep:
        return (
            f"Missing runtime dependency '{dep}'.\n"
            f"Add dependency in recipe:\n"
            f"    RDEPENDS:${{PN}} += \"{dep}\""
        )

    return None


def generic_rule(failure):
    error_type = failure.get("error_type")
    return SUGGESTION_MAP.get(error_type)


# -----------------------------
# Rule Registry
# -----------------------------

SUGGESTION_RULES = [
    missing_provider_rule,
    runtime_dependency_rule,
    generic_rule
]


# -----------------------------
# Suggestion Engine
# -----------------------------

def suggest_fix(failure):

    for rule in SUGGESTION_RULES:

        suggestion = rule(failure)

        if suggestion:
            return suggestion

    return "Review error snippet and BitBake logs."
