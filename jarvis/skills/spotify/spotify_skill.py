from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import spotipy  # type: ignore[import-untyped]
from spotipy.oauth2 import SpotifyOAuth  # type: ignore[import-untyped]

from jarvis.config import settings
from jarvis.core.tool import RiskLevel, SyncTool, ToolParameter

ROOT_DIR = Path(__file__).resolve().parents[3]
TOKEN_CACHE = ROOT_DIR / ".spotify_cache"

SPOTIFY_SCOPES = "user-read-playback-state user-modify-playback-state"


class SpotifySkill:
    """Search for music and control the Spotify desktop application."""

    def __init__(self) -> None:
        self._spotify: spotipy.Spotify | None = None

        self.tools = [
            SyncTool(
                name="spotify.search_track",
                description="Look up a track in Spotify.",
                func=self.search_track,
                parameters=[
                    ToolParameter(
                        "query",
                        "str",
                        "Track, artist or search text.",
                        required=True,
                    )
                ],
                risk_level=RiskLevel.SAFE,
            ),
            SyncTool(
                name="spotify.play_track",
                description="Play a track in the Spotify desktop application.",
                func=self.play_track,
                parameters=[
                    ToolParameter(
                        "query",
                        "str",
                        "Track, artist or search text.",
                        required=True,
                    )
                ],
                risk_level=RiskLevel.SAFE,
            ),
            SyncTool(
                name="spotify.pause",
                description="Pause the active Spotify playback.",
                func=self.pause,
                parameters=[],
                risk_level=RiskLevel.SAFE,
            ),
        ]

    def _get_client(self) -> spotipy.Spotify:
        if self._spotify is not None:
            return self._spotify

        if not settings.has_spotify_config:
            raise RuntimeError("Spotify is not configured. Check the Spotify values in .env.")

        auth_manager = SpotifyOAuth(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            scope=SPOTIFY_SCOPES,
            cache_path=str(TOKEN_CACHE),
            open_browser=True,
        )

        self._spotify = spotipy.Spotify(auth_manager=auth_manager)
        return self._spotify

    def _find_track(self, query: str) -> dict[str, Any]:
        spotify = self._get_client()
        result = spotify.search(q=query, type="track", limit=1) or {}
        tracks_data = result.get("tracks") or {}
        tracks = tracks_data.get("items") or []

        if not tracks:
            raise RuntimeError(f"No Spotify track found for '{query}'.")

        return tracks[0]

    def _get_device_id(self) -> str:
        spotify = self._get_client()
        local_computer = os.environ.get("COMPUTERNAME", "").casefold()

        for _ in range(10):
            result = spotify.devices() or {}
            devices = result.get("devices") or []
            computers = [
                device
                for device in devices
                if device.get("type", "").casefold() == "computer"
                and device.get("id")
                and not device.get("is_restricted")
            ]

            for device in computers:
                name = str(device.get("name", "")).casefold()
                if local_computer and name == local_computer:
                    return str(device["id"])

            time.sleep(1)

        raise RuntimeError(
            f"No controllable Spotify device named '{local_computer}' found. "
            "Make sure Spotify is open on this computer and logged in."
        )

    def _activate_device(self, device_id: str) -> None:
        spotify = self._get_client()
        devices = (spotify.devices() or {}).get("devices") or []
        if any(d.get("id") == device_id and d.get("is_active") for d in devices):
            return

        spotify.transfer_playback(device_id=device_id, force_play=False)
        for _ in range(10):
            time.sleep(0.5)
            devices = (spotify.devices() or {}).get("devices") or []
            if any(d.get("id") == device_id and d.get("is_active") for d in devices):
                return

        raise RuntimeError(
            "Spotify did not activate this computer. No new track was requested. "
            "Check the device selection in the Spotify desktop app."
        )

    def _wait_until_playing(
        self,
        device_id: str,
        track: dict[str, Any],
    ) -> bool:
        spotify = self._get_client()
        target_track_id = track.get("id")
        if not target_track_id:
            return False

        previous_progress: int | None = None

        for _ in range(10):
            time.sleep(0.5)
            playback = spotify.current_playback() or {}
            playback_device = playback.get("device") or {}
            current_track = playback.get("item") or {}
            linked_from = current_track.get("linked_from") or {}

            correct_device = playback_device.get("id") == device_id
            correct_track = target_track_id in {
                current_track.get("id"),
                linked_from.get("id"),
            }

            progress = playback.get("progress_ms")
            if (
                playback.get("is_playing")
                and correct_device
                and correct_track
                and isinstance(progress, int)
            ):
                if previous_progress is not None and progress > previous_progress:
                    return True
                previous_progress = progress
            else:
                previous_progress = None

        return False

    @staticmethod
    def _track_description(track: dict[str, Any]) -> str:
        name = track.get("name", "Unknown track")
        artists = track.get("artists", [])
        artist_names = ", ".join(artist.get("name", "Unknown artist") for artist in artists)
        return f"{name} by {artist_names}"

    def search_track(self, query: str) -> str:
        track = self._find_track(query)
        return f"Found {self._track_description(track)}"

    def play_track(self, query: str) -> str:
        os.startfile("spotify:")
        time.sleep(3)

        spotify = self._get_client()
        track = self._find_track(query)
        device_id = self._get_device_id()
        track_uri = track.get("uri")
        album_uri = (track.get("album") or {}).get("uri")

        if not track_uri:
            raise RuntimeError("The Spotify track has no playable URI.")
        if not album_uri:
            raise RuntimeError("The Spotify track has no album context for desktop playback.")

        self._activate_device(device_id)
        # The Windows client can accept a bare URI list but leave its player empty.
        # Starting the same track within its album works with this client.
        spotify.start_playback(
            device_id=device_id,
            context_uri=album_uri,
            offset={"uri": track_uri},
            position_ms=0,
        )

        if self._wait_until_playing(device_id, track):
            return f"Playing {self._track_description(track)}"

        raise RuntimeError(
            "Spotify accepted the command, but playback of this track on this computer "
            "could not be confirmed. Check the Spotify desktop player."
        )

    def pause(self) -> str:
        spotify = self._get_client()
        device_id = self._get_device_id()
        spotify.pause_playback(device_id=device_id)
        return "Spotify playback paused."
