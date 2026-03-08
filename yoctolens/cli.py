import sys
from yoctolens.classifier import classify_error
from yoctolens.parser import extract_all_failures
from yoctolens.aggregator import summarize_failures
from yoctolens.severity import assign_severity, compute_overall_severity
from yoctolens.suggestions import suggest_fix
from yoctolens.entities import extract_entities
import json
from datetime import datetime

def analyze(log_path, output_json=False):
    try:
        with open(log_path, "r") as f:
            content = f.read()

        failures = extract_all_failures(content)

        # Enrich failures with classification + severity
        enriched_failures = []
        for failure in failures:
            error_type = classify_error(
                failure.get("error_snippet", []),
                task=failure.get("task")
            )

            severity = assign_severity(error_type)
            entities = extract_entities(error_type, failure)
            failure_context = {
                "error_type": error_type,
                "error_snippet": failure.get("error_snippet", [])
            }

            suggestion = suggest_fix(failure_context)
            enriched_failures.append({
                "recipe": failure["recipe"],
                "task": failure["task"],
                "error_type": error_type,
                "severity": severity,
                "detected_entities": entities,
                "suggested_fix": suggestion,
                "error_snippet": failure.get("error_snippet", [])
            })

        # Generate summary
        summary = summarize_failures(enriched_failures)
        overall_severity = compute_overall_severity(enriched_failures)

        # -------------------------
        # JSON MODE
        # -------------------------
        if output_json:
            result = {
                "tool": "YoctoLens",
                "version": "0.8",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "total_failures": summary["total_failures"],
                "overall_severity": overall_severity,
                "summary": summary["by_error_type"],
                "failures": enriched_failures
            }

            print(json.dumps(result, indent=2))

        else:
            # -------------------------
            # HUMAN MODE
            # -------------------------
            print("YoctoLens v0.8\n")

            if summary["total_failures"] == 0:
                print("No failures detected.")
                sys.exit(0)

            print(f"Detected {summary['total_failures']} failure(s)\n")

            print("Summary by Error Type:")
            for error_type, count in summary["by_error_type"].items():
                print(f"  {error_type}: {count}")

            print(f"\nOverall Severity: {overall_severity}\n")

            for idx, failure in enumerate(enriched_failures, 1):
                print(f"[Failure {idx}]")
                print(f"  Recipe: {failure['recipe']}")
                print(f"  Task: {failure['task']}")
                print(f"  Error Type: {failure['error_type']}")
                print(f"  Severity: {failure['severity']}")

                if failure["error_snippet"]:
                    print("  Error Snippet:")
                    for line in failure["error_snippet"]:
                        print(f"    {line}")

                print("  Suggested Fix:")
                for line in failure["suggested_fix"].splitlines():
                    print(f"    {line}")

                print()

        # -------------------------
        # EXIT CODE (CI Friendly)
        # -------------------------
        if overall_severity == "High":
            sys.exit(2)
        elif overall_severity == "Medium":
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"Error reading log: {e}")
        sys.exit(3)


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
