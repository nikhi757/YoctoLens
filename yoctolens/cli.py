import sys
from yoctolens.parser import extract_last_failure
from yoctolens.classifier import classify_error
from yoctolens.parser import extract_all_failures


def analyze(log_path):
    try:
        with open(log_path, "r") as f:
            content = f.read()

        failures = extract_all_failures(content)

        print("YoctoLens v0.4\n")

        if not failures:
            print("No failures detected.")
            return

        print(f"Detected {len(failures)} failure(s)\n")

        for idx, failure in enumerate(failures, 1):
            error_type = classify_error(
                failure.get("error_snippet", []),
                task=failure.get("task")
            )

            print(f"[Failure {idx}]")
            print(f"  Recipe: {failure['recipe']}")
            print(f"  Task: {failure['task']}")
            print(f"  Error Type: {error_type}")

            if failure["error_snippet"]:
                print("  Error Snippet:")
                for line in failure["error_snippet"]:
                    print(f"    {line}")

            print()

    except Exception as e:
        print(f"Error reading log: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python yoctolens/cli.py analyze <build.log>")
        sys.exit(1)

    command = sys.argv[1]
    log_path = sys.argv[2]

    if command == "analyze":
        analyze(log_path)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
