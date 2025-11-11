#!/bin/bash
# Script to run tests and enforce 100% coverage for pre-commit hook

echo "Running tests with coverage..."

# Step 1: Run pytest with all flags and capture output
pytest --cov=src \
       --cov-report=term-missing \
       --cov-report=html \
       --cov-fail-under=100

pytest_exit_code=$? # Capture the exit code of the pytest command

# Step 2: Check if the command succeeded or failed
if [ $pytest_exit_code -eq 0 ]; then
    echo "✅ Success! Tests passed with 100% coverage!"
    echo "--- Report generated. Starting web server at http://localhost:8000 ---"
    echo "--- Press Ctrl+C to stop the server ---"
    # Serve the generated report
    (cd htmlcov && python3 -m http.server 8000)
else
    echo "❌ Failure! Either tests failed or coverage is below 100%."
    echo "--- Report generated. Starting web server at http://localhost:8000 ---"
    echo "--- Press Ctrl+C to stop the server ---"
    # Serve the generated report
    (cd htmlcov && python3 -m http.server 8000)
    echo "Output:"
    echo "$pytest_output"
    exit 1 # Exit with a failure code to stop any further automated processes
fi
