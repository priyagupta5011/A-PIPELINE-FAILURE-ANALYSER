from src.log_parser import (
    classify_error,
    determine_severity,
    extract_error_lines,
    extract_error_message,
    extract_stage,
)


def test_out_of_memory_error():
    logs = """
    2026-08-25 10:22:31 ERROR Stage 4 failed
    2026-08-25 10:22:32 ERROR Executor lost
    2026-08-25 10:22:32 ERROR OutOfMemoryError
    """

    error_lines = extract_error_lines(logs)

    assert classify_error(error_lines) == "OUT_OF_MEMORY"
    assert extract_stage(error_lines) == "Stage 4"
    assert determine_severity("OUT_OF_MEMORY") == "HIGH"


def test_file_not_found_error():
    logs = """
    2026-08-25 11:10:10 ERROR Stage 2 failed
    2026-08-25 11:10:10 ERROR FileNotFoundException
    """

    error_lines = extract_error_lines(logs)

    assert classify_error(error_lines) == "FILE_NOT_FOUND"
    assert extract_stage(error_lines) == "Stage 2"
    assert determine_severity("FILE_NOT_FOUND") == "HIGH"


def test_timeout_error():
    logs = """
    2026-08-25 12:16:10 ERROR Stage 1 failed
    2026-08-25 12:16:10 ERROR TimeoutException
    """

    error_lines = extract_error_lines(logs)

    assert classify_error(error_lines) == "TIMEOUT"
    assert extract_stage(error_lines) == "Stage 1"
    assert determine_severity("TIMEOUT") == "MEDIUM"


def test_unknown_error():
    logs = """
    2026-08-25 13:00:01 ERROR Stage 3 failed
    2026-08-25 13:00:02 ERROR SomethingUnexpectedHappened
    """

    error_lines = extract_error_lines(logs)

    assert classify_error(error_lines) == "UNKNOWN"
    assert extract_stage(error_lines) == "Stage 3"
    assert determine_severity("UNKNOWN") == "UNKNOWN"


def test_error_message_extraction():
    logs = """
    2026-08-25 10:22:31 ERROR Executor lost
    2026-08-25 10:22:32 ERROR OutOfMemoryError
    """

    error_lines = extract_error_lines(logs)

    message = extract_error_message(error_lines)

    assert message == "Executor lost - OutOfMemoryError"