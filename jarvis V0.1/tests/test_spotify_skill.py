from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from jarvis.skills.spotify import spotify_skill
from jarvis.skills.spotify.spotify_skill import SpotifySkill


def make_device(**overrides: Any) -> dict[str, Any]:
    return {
        "id": "local-device",
        "name": "maik",
        "type": "Computer",
        "is_active": True,
        "is_restricted": False,
        **overrides,
    }


def make_track(**overrides: Any) -> dict[str, Any]:
    return {
        "id": "sweden",
        "uri": "spotify:track:sweden",
        "name": "Sweden",
        "artists": [{"name": "C418"}],
        "album": {"uri": "spotify:album:minecraft"},
        **overrides,
    }


def make_playback(progress_ms: int | None, **overrides: Any) -> dict[str, Any]:
    return {
        "device": make_device(),
        "item": make_track(),
        "is_playing": True,
        "progress_ms": progress_ms,
        **overrides,
    }


@pytest.fixture
def mocked_spotify(monkeypatch: pytest.MonkeyPatch) -> tuple[SpotifySkill, MagicMock]:
    monkeypatch.setenv("COMPUTERNAME", "MAIK")
    monkeypatch.setattr(spotify_skill.os, "startfile", MagicMock(), raising=False)
    monkeypatch.setattr(spotify_skill.time, "sleep", MagicMock())
    monkeypatch.setattr(
        spotify_skill,
        "SpotifyOAuth",
        MagicMock(side_effect=AssertionError("Offline tests must not access OAuth or tokens")),
    )
    client = MagicMock()
    client.devices.return_value = {"devices": [make_device()]}
    client.search.return_value = {"tracks": {"items": [make_track()]}}
    client.current_playback.side_effect = [make_playback(100), make_playback(600)]
    skill = SpotifySkill()
    skill._spotify = client
    return skill, client


def test_play_uses_album_context_and_does_not_transfer_active_local_device(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
) -> None:
    skill, client = mocked_spotify

    assert skill.play_track("C418 Sweden") == "Playing Sweden by C418"

    client.search.assert_called_once_with(q="C418 Sweden", type="track", limit=1)
    client.start_playback.assert_called_once_with(
        device_id="local-device",
        context_uri="spotify:album:minecraft",
        offset={"uri": "spotify:track:sweden"},
        position_ms=0,
    )
    client.transfer_playback.assert_not_called()
    assert client.current_playback.call_count == 2


def test_activation_transfers_once_and_waits_until_local_device_is_active(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
) -> None:
    skill, client = mocked_spotify
    inactive = {"devices": [make_device(is_active=False)]}
    client.devices.side_effect = [inactive, inactive, {"devices": [make_device()]}]

    skill._activate_device("local-device")

    client.transfer_playback.assert_called_once_with(device_id="local-device", force_play=False)
    assert client.devices.call_count == 3


def test_activation_failure_prevents_playback_request(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
) -> None:
    skill, client = mocked_spotify
    client.devices.return_value = {"devices": [make_device(is_active=False)]}

    with pytest.raises(RuntimeError):
        skill.play_track("C418 Sweden")

    client.transfer_playback.assert_called_once_with(device_id="local-device", force_play=False)
    client.start_playback.assert_not_called()
    client.current_playback.assert_not_called()


def test_accepted_playback_without_advancing_progress_is_not_success_or_retried(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
) -> None:
    skill, client = mocked_spotify
    client.current_playback.side_effect = None
    client.current_playback.return_value = make_playback(100)

    with pytest.raises(RuntimeError):
        skill.play_track("C418 Sweden")

    client.start_playback.assert_called_once()
    client.transfer_playback.assert_not_called()


@pytest.mark.parametrize(
    "states",
    [
        [
            make_playback(100, device={"id": "remote-device"}),
            make_playback(600, device={"id": "remote-device"}),
        ],
        [
            make_playback(100, item={"id": "other-track"}),
            make_playback(600, item={"id": "other-track"}),
        ],
        [make_playback(100, is_playing=False), make_playback(600, is_playing=False)],
        [make_playback(None), make_playback(None)],
        [{}, {}],
    ],
    ids=["wrong-device", "wrong-track", "paused", "missing-progress", "no-playback"],
)
def test_verification_rejects_wrong_or_incomplete_playback(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
    states: list[dict[str, Any]],
) -> None:
    skill, client = mocked_spotify
    client.current_playback.side_effect = states * 10

    assert skill._wait_until_playing("local-device", make_track()) is False


def test_verification_accepts_relinked_track_but_resets_progress_after_mismatch(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
) -> None:
    skill, client = mocked_spotify
    relinked = {"id": "regional-sweden", "linked_from": {"id": "sweden"}}
    client.current_playback.side_effect = [
        make_playback(100, item=relinked),
        make_playback(200, item={"id": "other-track"}),
        make_playback(300, item=relinked),
        make_playback(800, item=relinked),
    ]

    assert skill._wait_until_playing("local-device", make_track()) is True
    assert client.current_playback.call_count == 4


@pytest.mark.parametrize("track_id", [None, ""])
def test_verification_rejects_missing_target_track_id(
    mocked_spotify: tuple[SpotifySkill, MagicMock], track_id: str | None
) -> None:
    skill, client = mocked_spotify

    assert skill._wait_until_playing("local-device", make_track(id=track_id)) is False
    client.current_playback.assert_not_called()


@pytest.mark.parametrize(
    ("computer_name", "devices"),
    [
        ("MAIK", [make_device(id="remote-device", name="OTHER-PC")]),
        ("", [make_device()]),
        ("MAIK", [make_device(type="Smartphone")]),
        ("MAIK", [make_device(is_restricted=True)]),
        ("MAIK", [make_device(id=None)]),
    ],
    ids=["remote-computer", "unknown-local-name", "phone", "restricted", "missing-id"],
)
def test_device_selection_never_falls_back_to_an_unverified_device(
    mocked_spotify: tuple[SpotifySkill, MagicMock],
    monkeypatch: pytest.MonkeyPatch,
    computer_name: str,
    devices: list[dict[str, Any]],
) -> None:
    skill, client = mocked_spotify
    monkeypatch.setenv("COMPUTERNAME", computer_name)
    client.devices.return_value = {"devices": devices}

    with pytest.raises(RuntimeError):
        skill._get_device_id()

    client.transfer_playback.assert_not_called()
    client.start_playback.assert_not_called()
