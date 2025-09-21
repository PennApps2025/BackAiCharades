"""Script to reset the leaderboard DB.

This file is safe to run in two ways:
- As a module from the project root: `python -m app.init_db`
- Directly as a script: `python app\init_db.py` (works by adding repo root to sys.path)
"""
from pathlib import Path
import sys

# If this file is executed directly (python app\init_db.py), the package root
# may not be on sys.path. Ensure the repository root (one level above `app`)
# is on sys.path so `import app` works.
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from app.database import reset_db


def init_db():
    """Call the project's reset_db to reinitialize the DB."""
    reset_db()


if __name__ == "__main__":
    init_db()
