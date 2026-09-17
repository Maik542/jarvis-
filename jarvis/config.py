from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
# Die lokale .env liegt im Projektordner und darf nicht ins Repository.
ENV_PATH = ROOT_DIR / ".env"


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    # Leere Werte bedeuten "nicht eingerichtet"; Secrets nie fest einkodieren.
    log_level: str = "INFO"
    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    spotify_redirect_uri: str = "http://127.0.0.1:8888/callback"

    @classmethod
    def from_env(cls) -> Settings:
        # .env erg?nzt fehlende Umgebungsvariablen; vorhandene Werte bleiben erhalten.
        load_dotenv(ENV_PATH, override=False)
        return cls(
            log_level=os.getenv("JARVIS_LOG_LEVEL", "INFO"),
            llm_provider=os.getenv("LLM_PROVIDER", ""),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            spotify_client_id=os.getenv("SPOTIFY_CLIENT_ID", ""),
            spotify_client_secret=os.getenv("SPOTIFY_CLIENT_SECRET", ""),
            spotify_redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
        )

    @property
    def has_llm_config(self) -> bool:
        # Pr?ft nur, ob Werte gesetzt sind; ein LLM-Aufruf ist noch nicht integriert.
        return bool(self.llm_provider and self.llm_api_key and self.llm_model)

    @property
    def has_spotify_config(self) -> bool:
        return bool(self.spotify_client_id and self.spotify_client_secret)


# Einmaliger Snapshot beim Import; sp?tere .env-?nderungen brauchen einen Neustart.
settings = Settings.from_env()
