import json
import sys

from log_parser import (
    read_logs,
    extract_error_lines,
    classify_error,
    extract_stage,
    determine_severity,
    extract_error_message,
)


OUTPUT_FILE = "output/failure_analysis.json"


def analyze_pipeline(log_file: str) -> dict:
    """Analyze a pipeline log file and return structured failure information."""

    logs = read_logs(log_file)

    error_lines = extract_error_lines(logs)

    error_type = classify_error(error_lines)
    stage = extract_stage(error_lines)
    severity = determine_severity(error_type)
    error_message = extract_error_message(error_lines)

    return {
        "status": "FAILED",
        "error_type": error_type,
        "stage": stage,
        "severity": severity,
        "error_message": error_message,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    try:
        analysis = analyze_pipeline(log_file)
    except FileNotFoundError:
        print(f"Error: Log file not found: {log_file}")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4)

    print("Pipeline Failure Analysis")
    print("-------------------------")
    print(json.dumps(analysis, indent=4))