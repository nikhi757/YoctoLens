import re

def extract_entities(error_type, failure):
    """
    Extract structured entities from error snippet.
    """

    snippet = failure.get("error_snippet", [])
    entities = {}

    # Missing provider detection
    if error_type == "Missing Provider":
        for line in snippet:
            match = re.search(r"Nothing PROVIDES '([^']+)'", line)
            if match:
                entities["missing_provider"] = match.group(1)

    # Runtime dependency detection
    if error_type == "QA Failure":
        for line in snippet:
            match = re.search(r"requires\s+/(?:usr/)?bin/([a-zA-Z0-9_\-]+)", line)
            if match:
                entities["missing_runtime_dependency"] = match.group(1)

    return entities
