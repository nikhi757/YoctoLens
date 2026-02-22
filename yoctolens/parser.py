import re


def extract_last_failure(log_content):
    """
    Extract the last failing BitBake task and related error snippet.
    """

    lines = log_content.splitlines()

    failure_pattern = r"ERROR: Task \((.*?)\) failed"

    failure_index = None
    failure_match = None

    for i, line in enumerate(lines):
        match = re.search(failure_pattern, line)
        if match:
            failure_index = i
            failure_match = match.group(1)

    if failure_index is None:
        return None

    # Extract recipe and task
    try:
        recipe_path, task = failure_match.rsplit(":", 1)
        recipe_file = recipe_path.split("/")[-1]
        recipe_name = recipe_file.replace(".bb", "")
    except ValueError:
        return None

    # Extract error snippet (look 15 lines above failure)
    snippet_start = max(0, failure_index - 15)
    snippet_lines = lines[snippet_start:failure_index]

    # Keep only ERROR lines (excluding the final Task failure line)
    error_lines = [
        line for line in snippet_lines
        if line.startswith("ERROR:")
        and "Task (" not in line
    ]

    return {
        "recipe": recipe_name,
        "task": task,
        "error_snippet": error_lines[-5:] if error_lines else []
    }
