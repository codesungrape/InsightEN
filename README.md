# InsightEN

# 1️⃣ Clone the repo
git clone git@github.com:codesungrape/InsightEN.git
cd InsightEN

# 2️⃣ Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR on Windows: venv\Scripts\activate

# 3️⃣ Install dependencies from pyproject.toml
pip install .

# 4️⃣ Install pre-commit hooks (only needed once)
pip install pre-commit
pre-commit install