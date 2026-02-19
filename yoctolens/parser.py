import re


def extract_last_failure(log_content):
    """
    Extract the last failing BitBake task from log.

    Example line:
    ERROR: Task (/path/to/recipe.bb:do_package_qa) failed with exit code '1'
    """

    pattern = r"ERROR: Task \((.*?)\) failed"

    matches = re.findall(pattern, log_content)

    if not matches:
        return None

    last_match = matches[-1]

    # Example:
    # /path/to/meta/recipes-devtools/protobuf/protobuf.bb:do_package_qa

    try:
        recipe_path, task = last_match.rsplit(":", 1)
        recipe_file = recipe_path.split("/")[-1]
        recipe_name = recipe_file.replace(".bb", "")
    except ValueError:
        return None

    return {
        "recipe": recipe_name,
        "task": task
    }
