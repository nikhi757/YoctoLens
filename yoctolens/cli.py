import sys
from yoctolens.classifier import classify_error
from yoctolens.parser import extract_all_failures
import json
from datetime import datetime

def analyze(log_path, output_json=False):
    try:
        with open(log_path, "r") as f:
            content = f.read()

        failures = extract_all_failures(content)

        enriched_failures = []

        for failure in failures:
            error_type = classify_error(
                failure.get("error_snippet", []),
                task=failure.get("task")
            )

            enriched_failures.append({
                "recipe": failure["recipe"],
                "task": failure["task"],
                "error_type": error_type,
                "error_snippet": failure.get("error_snippet", [])
            })

        if output_json:
            result = {
                "tool": "YoctoLens",
                "version": "0.5",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "total_failures": len(enriched_failures),
                "failures": enriched_failures
            }

            print(json.dumps(result, indent=2))
            return

        # Human-readable output
        print("YoctoLens v0.5\n")

        if not enriched_failures:
            print("No failures detected.")
            return

        print(f"Detected {len(enriched_failures)} failure(s)\n")

        for idx, failure in enumerate(enriched_failures, 1):
            print(f"[Failure {idx}]")
            print(f"  Recipe: {failure['recipe']}")
            print(f"  Task: {failure['task']}")
            print(f"  Error Type: {failure['error_type']}")

            if failure["error_snippet"]:
                print("  Error Snippet:")
                for line in failure["error_snippet"]:
                    print(f"    {line}")

            print()

    except Exception as e:
        print(f"Error reading log: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m yoctolens.cli analyze <build.log> [--json]")
        sys.exit(1)

    command = sys.argv[1]
    log_path = sys.argv[2]

    output_json = "--json" in sys.argv

    if command == "analyze":
        analyze(log_path, output_json=output_json)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
