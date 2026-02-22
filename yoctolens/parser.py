import re

def normalize_recipe_name(recipe_file):
    """
    Normalize Yocto recipe name by removing version and build variants.
    """

    # Remove .bb if present
    recipe = recipe_file.replace(".bb", "")

    # Remove virtual/ prefix
    if recipe.startswith("virtual/"):
        recipe = recipe.split("/")[-1]

    # Remove -native and -cross
    recipe = recipe.replace("-native", "")
    recipe = recipe.replace("-cross", "")

    # Remove version suffix (e.g., openssl_3.0.1 → openssl)
    recipe = re.sub(r"_\d+.*", "", recipe)

    return recipe

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
        recipe_name = normalize_recipe_name(recipe_file)
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

def extract_all_failures(log_content):
    """
    Extract all failing BitBake tasks from log.
    Returns list of failure dictionaries.
    """

    lines = log_content.splitlines()
    failures = []

    failure_pattern = r"ERROR: Task \((.*?)\) failed"

    for i, line in enumerate(lines):
        match = re.search(failure_pattern, line)
        if match:
            failure_match = match.group(1)

            try:
                recipe_path, task = failure_match.rsplit(":", 1)
                recipe_file = recipe_path.split("/")[-1]
                recipe_name = normalize_recipe_name(recipe_file)
            except ValueError:
                continue

            # Walk backwards to collect related ERROR lines
            error_lines = []
            j = i - 1

            while j >= 0:
                line_above = lines[j]

                if line_above.startswith("ERROR: Task ("):
                    break  # Stop at previous task failure

                if line_above.startswith("ERROR:"):
                    error_lines.insert(0, line_above)
                elif line_above.strip() == "":
                    break  # Stop at blank line boundary

                j -= 1

            failures.append({
                "recipe": recipe_name,
                "task": task,
                "error_snippet": error_lines[-5:] if error_lines else []
            })

    return failures
