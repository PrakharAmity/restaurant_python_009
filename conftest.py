import json
import time

import pytest


_results = {}
_started = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    _started[item.nodeid] = time.perf_counter()
    outcome = yield
    record = _results.setdefault(item.nodeid, {})
    record["duration"] = time.perf_counter() - _started[item.nodeid]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        record = _results.setdefault(item.nodeid, {})
        record["status"] = "passed" if report.passed else "failed"
        if report.failed:
            detail = next((line.split("AssertionError:", 1)[1].strip() for line in report.longreprtext.splitlines() if "AssertionError:" in line), None)
            error_lines = [line.strip()[2:].strip() for line in report.longreprtext.splitlines() if line.strip().startswith("E ")]
            record["error"] = detail or (error_lines[-1] if error_lines else "Assertion failed")


def pytest_sessionfinish(session, exitstatus):
    tests = {}
    total_ms = 0
    for nodeid, record in _results.items():
        name = nodeid.rsplit("::", 1)[-1]
        elapsed = round(record.get("duration", 0) * 1000)
        total_ms += elapsed
        entry = {"Status": record.get("status", "failed"), "Execution time": f"{elapsed}ms"}
        if record.get("error"):
            entry["Error"] = record["error"]
        tests[name] = entry
    passed = sum(1 for result in tests.values() if result["Status"] == "passed")
    failed = len(tests) - passed
    payload = {
        **tests,
        "Passed": passed,
        "Failed": failed,
        "Total bugs": len(tests),
        "Total Execution time": f"{total_ms}ms",
    }
    print(json.dumps(payload, separators=(",", ":")))
