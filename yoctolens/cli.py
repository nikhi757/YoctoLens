import sys


def analyze(log_path):
    try:
        with open(log_path, "r") as f:
            content = f.read()
        print("YoctoLens v0.1")
        print(f"Log loaded successfully.")
        print(f"Log size: {len(content)} bytes")
    except Exception as e:
        print(f"Error reading log: {e}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m yoctolens.cli analyze <build.log>")
        sys.exit(1)

    command = sys.argv[1]
    log_path = sys.argv[2]

    if command == "analyze":
        analyze(log_path)
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
