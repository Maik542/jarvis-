from __future__ import annotations

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
# Logdateien bleiben lokal im Projekt; das Verzeichnis bei Bedarf anlegen.
LOG_DIR.mkdir(exist_ok=True)


def configure_logging() -> logging.Logger:
    """Configure console and file logging for the application."""
    logger = logging.getLogger("jarvis")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Bereits konfigurierte Handler wiederverwenden, sonst g?be es doppelte Logs.
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    file_handler = logging.FileHandler(LOG_DIR / "jarvis.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    # Dieselben Meldungen gehen in die Datei und auf die Konsole.
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a logger for a given module."""
    return logging.getLogger(f"jarvis.{name}")
