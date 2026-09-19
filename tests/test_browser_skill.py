from unittest.mock import AsyncMock, MagicMock

import pytest

import main as jarvis_cli
from jarvis.skills.browser.browser_skill import BrowserSkill


@pytest.fixture
def browser(monkeypatch: pytest.MonkeyPatch, tmp_path) -> BrowserSkill:
    # Ein temporärer Profilpfad verhindert Zugriff auf dein echtes Chrome-Profil.
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    return BrowserSkill()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("service", "expected_url"),
    [
        ("youtube", "https://www.youtube.com/results?search_query=C418+Sweden"),
        ("google", "https://www.google.com/search?q=C418+Sweden"),
        ("github", "https://github.com/search?q=C418+Sweden"),
    ],
)
async def test_search_opens_results_without_playing(
    browser: BrowserSkill,
    monkeypatch: pytest.MonkeyPatch,
    service: str,
    expected_url: str,
) -> None:
    page = MagicMock()
    open_url = AsyncMock(return_value=page)
    reject_cookies = AsyncMock()
    monkeypatch.setattr(browser, "open_url", open_url)
    monkeypatch.setattr(browser, "_reject_youtube_cookies", reject_cookies)

    result = await browser.search(service, "C418 Sweden")

    assert result is page
    open_url.assert_awaited_once_with(expected_url)
    page.locator.assert_not_called()  # Kein Video-Treffer angeklickt.

    if service == "youtube":
        reject_cookies.assert_awaited_once_with(page)
    else:
        reject_cookies.assert_not_awaited()


@pytest.mark.asyncio
async def test_play_youtube_opens_first_video(
    browser: BrowserSkill,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page = MagicMock()
    first_video = MagicMock()
    first_video.wait_for = AsyncMock()
    first_video.get_attribute = AsyncMock(return_value=" Sweden - C418 ")
    first_video.click = AsyncMock()
    page.locator.return_value.first = first_video
    page.wait_for_url = AsyncMock()

    search = AsyncMock(return_value=page)
    monkeypatch.setattr(browser, "search", search)

    title = await browser.play_youtube("C418 Sweden")

    assert title == "Sweden - C418"
    search.assert_awaited_once_with("youtube", "C418 Sweden")
    page.locator.assert_called_once_with("ytd-video-renderer a#video-title")
    first_video.click.assert_awaited_once_with(timeout=15000)
    page.wait_for_url.assert_awaited_once_with("**/watch?*", timeout=15000)


@pytest.mark.asyncio
async def test_next_command_creates_tab_after_ctrl_w(browser: BrowserSkill) -> None:
    # Wir simulieren, dass Chrome den bisherigen Tab geschlossen hat.
    old_page = MagicMock()
    old_page.is_closed.return_value = False
    old_page.goto = AsyncMock()

    new_page = MagicMock()
    new_page.goto = AsyncMock()

    context = MagicMock()
    context.is_closed.return_value = False
    context.pages = [old_page]
    context.new_page = AsyncMock(return_value=new_page)

    browser._context = context
    browser._page = old_page

    await browser.open_url("https://www.youtube.com")
    old_page.is_closed.return_value = True
    await browser.open_url("https://www.google.com")

    context.new_page.assert_awaited_once_with()
    new_page.goto.assert_awaited_once_with(
        "https://www.google.com",
        wait_until="domcontentloaded",
        timeout=30000,
    )
    assert browser._page is new_page


@pytest.mark.asyncio
async def test_closed_window_reuses_persistent_profile(
    browser: BrowserSkill,
    tmp_path,
) -> None:
    # Auch nach einem geschlossenen Fenster bleibt der Profilordner gleich.
    old_context = MagicMock()
    old_context.is_closed.return_value = True
    browser._context = old_context

    new_context = MagicMock()
    playwright = MagicMock()
    playwright.chromium.launch_persistent_context = AsyncMock(return_value=new_context)
    browser._playwright = playwright

    result = await browser._get_context()

    assert result is new_context
    options = playwright.chromium.launch_persistent_context.await_args.kwargs
    assert options["user_data_dir"] == str(tmp_path / "Jarvis" / "BrowserProfile")
    assert options["channel"] == "chrome"
    assert options["ignore_default_args"] == ["--disable-extensions"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("command", "method", "arguments"),
    [
        (
            "search youtube for C418 Sweden",
            "search",
            ("youtube", "C418 Sweden"),
        ),
        (
            "search google for C418 Sweden",
            "search",
            ("google", "C418 Sweden"),
        ),
        (
            "search github for C418 Sweden",
            "search",
            ("github", "C418 Sweden"),
        ),
        (
            "play C418 Sweden on youtube",
            "play_youtube",
            ("C418 Sweden",),
        ),
    ],
)
async def test_cli_routes_browser_commands(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    command: str,
    method: str,
    arguments: tuple[str, ...],
) -> None:
    # main.py wird ausgeführt, aber Browser und Spotify sind nur Attrappen.
    fake_browser = MagicMock()
    fake_browser.search = AsyncMock()
    fake_browser.play_youtube = AsyncMock(return_value="Sweden - C418")
    fake_browser.close = AsyncMock()

    monkeypatch.setattr(jarvis_cli, "BrowserSkill", lambda: fake_browser)
    monkeypatch.setattr(jarvis_cli, "SpotifySkill", lambda: object())

    inputs = iter([command, "exit"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))

    await jarvis_cli.main()

    getattr(fake_browser, method).assert_awaited_once_with(*arguments)
    fake_browser.close.assert_awaited_once_with()

    output = capsys.readouterr().out
    assert "Press Strg+W to close the browser tab" in output

    if method == "search":
        fake_browser.play_youtube.assert_not_awaited()
        assert "Playing on YouTube:" not in output
    else:
        fake_browser.search.assert_not_awaited()
        assert "Playing on YouTube: Sweden - C418" in output
