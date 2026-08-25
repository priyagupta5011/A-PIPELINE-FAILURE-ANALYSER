from log_parser import (
    read_logs,
    extract_error_lines,
    classify_error,
    extract_stage,
)


LOG_FILE = "data/sample_logs.txt"


def main():
    logs = read_logs(LOG_FILE)

    error_lines = extract_error_lines(logs)

    error_type = classify_error(error_lines)

    stage = extract_stage(error_lines)

    print("Pipeline Failure Analysis")
    print("-------------------------")
    print(f"Error Type : {error_type}")
    print(f"Stage      : {stage}")


if __name__ == "__main__":
    main()