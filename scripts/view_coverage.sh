#!/bin/bash
# Convenience script to view the HTML coverage report.

echo "--- Generating and serving coverage report at http://localhost:8000 ---"
echo "--- Press Ctrl+C to stop the server ---"

# First, re-run pytest to make sure the report is up-to-date.
pytest --cov=src --cov-report=html

# Then, serve the generated report.
(cd htmlcov && python3 -m http.server 8000)
