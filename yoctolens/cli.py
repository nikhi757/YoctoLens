import sys
from yoctolens.parser import extract_last_failure


def analyze(log_path):
    try:
        with open(log_path, "r") as f:
            content = f.read()

        failure = extract_last_failure(content)

        print("YoctoLens v0.2\n")

        if failure:
            print("Failure Summary:")
            print(f"  Recipe: {failure['recipe']}")
            print(f"  Task: {failure['task']}")
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
