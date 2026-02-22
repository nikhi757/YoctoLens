import sys
from yoctolens.parser import extract_last_failure
from yoctolens.classifier import classify_error

def analyze(log_path):
    try:
        with open(log_path, "r") as f:
            content = f.read()

        failure = extract_last_failure(content)

        print("YoctoLens v0.3\n")

        if failure:
            print("Failure Summary:")
            print(f"  Recipe: {failure['recipe']}")
            print(f"  Task: {failure['task']}")

            # NEW: classification step
            error_type = classify_error(failure.get("error_snippet", []))
            print(f"  Error Type: {error_type}")

            if failure["error_snippet"]:
                print("\nError Snippet:")
                for line in failure["error_snippet"]:
                    print(f"  {line}")
        else:
            print("No failure detected.")

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
