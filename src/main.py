import json

from log_parser import (
    read_logs,
    extract_error_lines,
    classify_error,
    extract_stage,
    determine_severity,
    extract_error_message,
)


LOG_FILE = "data/sample_logs.txt"
OUTPUT_FILE = "output/failure_analysis.json"


def main():
    logs = read_logs(LOG_FILE)

    error_lines = extract_error_lines(logs)

    error_type = classify_error(error_lines)
    stage = extract_stage(error_lines)
    severity = determine_severity(error_type)
    error_message = extract_error_message(error_lines)

    analysis = {
        "status": "FAILED",
        "error_type": error_type,
        "stage": stage,
        "severity": severity,
        "error_message": error_message,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4)

    print("Pipeline Failure Analysis")
    print("-------------------------")
    print(json.dumps(analysis, indent=4))


if __name__ == "__main__":
    main()