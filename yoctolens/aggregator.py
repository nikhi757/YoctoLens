from collections import Counter


def summarize_failures(failures):
    """
    Generate summary statistics from enriched failures list.
    """

    error_types = [f["error_type"] for f in failures]
    counts = Counter(error_types)

    return {
        "total_failures": len(failures),
        "by_error_type": dict(counts)
    }
