from pathlib import Path
import sys

# Добавляем корень проекта в sys.path, чтобы можно было импортировать src.widget
ROOT = Path(__file__).resolve().parents[1]  # тесты/.. -> корень проекта
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
