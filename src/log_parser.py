import re


ERROR_PATTERNS = {
    "OUT_OF_MEMORY": r"OutOfMemoryError",
    "FILE_NOT_FOUND": r"FileNotFoundException",
    "PERMISSION_ERROR": r"Permission denied",
    "CONNECTION_ERROR": r"Connection refused",
    "TIMEOUT": r"TimeoutException",
    "SPARK_ANALYSIS_ERROR": r"AnalysisException",
}


SEVERITY_MAP = {
    "OUT_OF_MEMORY": "HIGH",
    "FILE_NOT_FOUND": "HIGH",
    "PERMISSION_ERROR": "HIGH",
    "CONNECTION_ERROR": "HIGH",
    "TIMEOUT": "MEDIUM",
    "SPARK_ANALYSIS_ERROR": "MEDIUM",
    "UNKNOWN": "UNKNOWN",
}


def read_logs(file_path: str) -> str:
    """Read the complete log file and return its content."""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_error_lines(logs: str) -> list[str]:
    """Extract lines containing ERROR."""

    return [
        line
        for line in logs.splitlines()
        if "ERROR" in line.upper()
    ]


def classify_error(error_lines: list[str]) -> str:
    """Identify the error type from error lines."""

    for line in error_lines:
        for error_type, pattern in ERROR_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                return error_type

    return "UNKNOWN"


def extract_stage(error_lines: list[str]) -> str | None:
    """Extract the failed Spark stage from error lines."""

    for line in error_lines:
        match = re.search(
            r"(Stage\s+\d+)\s+failed",
            line,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return None


def determine_severity(error_type: str) -> str:
    """Determine severity based on the error type."""

    return SEVERITY_MAP.get(error_type, "UNKNOWN")


def extract_error_message(error_lines: list[str]) -> str:
    """Combine relevant error lines into a single error message."""

    if not error_lines:
        return ""

    return " - ".join(
        line.split("ERROR", 1)[-1].strip()
        for line in error_lines
    )