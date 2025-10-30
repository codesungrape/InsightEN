# InsightEN

### 1️⃣ Clone the repository
```bash
git clone git@github.com:codesungrape/InsightEN.git
cd InsightEN
```

### 2️⃣ Create and activate virtual environment
```
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```
**OR on Windows:** venv\Scripts\activate

### 3️⃣ Install dependencies from pyproject.toml
```
pip install .
```

### 4️⃣ Install pre-commit hooks (only needed once)
```
pip install pre-commit
pre-commit install
```

### ✅ Run tests with coverage
To run all tests, enforce 100% coverage, and automatically serve the HTML coverage report, execute:
```
./scripts/run_tests-cov.sh
```

This command will:
- Run all tests with pytest and coverage reporting
- Enforce 100% code coverage
- Generate an interactive HTML report
- Automatically start a local web server at http://localhost:8000

**Note:** Press Ctrl + C to stop the coverage server when you’re done.
