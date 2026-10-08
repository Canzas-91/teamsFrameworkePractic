#!/usr/bin/env python
"""Django command-line utility."""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamfinder.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "Django не установлен. Выполните: pip install -r requirements.txt"
        ) from error
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
