# -*- coding: utf-8 -*-
"""
Модуль conftest содержит общие фикстуры и настройки для всех тестов.

Этот файл автоматически загружается pytest и предоставляет:
- Настройку путей для импорта модулей из src/
- Общие фикстуры, используемые в нескольких тестовых файлах

Располагается в корневой директории tests/ для применения ко всем тестам.
"""

from pathlib import Path
import sys

# Добавляем корень проекта в sys.path, чтобы можно было импортировать src.widget
ROOT = Path(__file__).resolve().parents[1]  # tests/.. -> корень проекта
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
