import os
import sys
from pathlib import Path
import waitress

BASE_DIR = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application

if __name__ == "__main__":
    print("Serving high-performance Chessflow with Waitress on http://127.0.0.1:8000 (8 worker threads)...")
    waitress.serve(
        application,
        host="127.0.0.1",
        port=8000,
        threads=8,
        connection_limit=200,
        channel_timeout=60,
    )

