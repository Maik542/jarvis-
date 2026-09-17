from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote_plus

from playwright.async_api import (
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from playwright.async_api import (
    TimeoutError as PlaywrightTimeoutError,
)


class BrowserSkill:
    """Controls Jarvis's Chrome with its own persistent profile."""

    def __init__(self) -> None:
        local_app_data = Path(os.environ["LOCALAPPDATA"])
        # Das Profil liegt au?erhalb des Repos: Cookies und Erweiterungen bleiben
        # auch ohne Chrome-Anmeldung nach einem Jarvis-Neustart erhalten.
        self._profile_directory = local_app_data / "Jarvis" / "BrowserProfile"

        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def _get_context(self) -> BrowserContext:
        # Nach dem Schlie?en des Browserfensters beim n?chsten Befehl neu starten.
        if self._context is not None and not self._context.is_closed():
            return self._context

        self._context = None
        self._page = None

        if self._playwright is None:
            # Playwright nur einmal starten; den Browserkontext bei Bedarf neu.
            self._playwright = await async_playwright().start()

        self._context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self._profile_directory),
            channel="chrome",
            headless=False,
            # Playwright deaktiviert Erweiterungen sonst standardm??ig.
            ignore_default_args=["--disable-extensions"],
            chromium_sandbox=True,
        )

        return self._context

    async def _get_page(self) -> Page:
        context = await self._get_context()

        # Eine noch offene Registerkarte f?r den n?chsten Befehl weiterverwenden.
        if self._page is not None and not self._page.is_closed():
            return self._page

        # Falls der Nutzer nur diese Registerkarte geschlossen hat, zuerst
        # andere offene Tabs im selben Browserprofil pr?fen.
        for page in context.pages:
            if not page.is_closed():
                self._page = page
                return page

        # Nach Strg+W eine neue Registerkarte ?ffnen, ohne Jarvis zur?ckzusetzen.
        self._page = await context.new_page()
        return self._page

    async def open_url(self, url: str) -> Page:
        page = await self._get_page()

        # DOM bereit gen?gt; Bilder und Werbung m?ssen nicht vollst?ndig laden.
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        return page

    async def _reject_youtube_cookies(self, page: Page) -> None:
        # Der Dialog kann fehlen (z. B. dank gespeicherter Cookie-Einstellung).
        reject_button = page.get_by_text(
            re.compile(r"^(Alle ablehnen|Reject all)$", re.IGNORECASE)
        ).first

        try:
            await reject_button.click(timeout=5000)
        except PlaywrightTimeoutError:
            pass

    async def search(self, service: str, query: str) -> Page:
        # Nur Ergebnislisten ?ffnen; ein Treffer wird hier nicht angeklickt.
        encoded_query = quote_plus(query)

        search_urls = {
            "youtube": (f"https://www.youtube.com/results?search_query={encoded_query}"),
            "google": f"https://www.google.com/search?q={encoded_query}",
            "github": f"https://github.com/search?q={encoded_query}",
        }

        if service not in search_urls:
            # Spotify-Suche geh?rt absichtlich nicht zu diesem Browser-Skill.
            raise ValueError(f"Unknown browser search service: {service}")

        page = await self.open_url(search_urls[service])

        if service == "youtube":
            await self._reject_youtube_cookies(page)

        return page

    async def play_youtube(self, query: str) -> str:
        # Wiedergabe ist getrennt von search(): erst hier den ersten Treffer ?ffnen.
        page = await self.search("youtube", query)

        first_video = page.locator("ytd-video-renderer a#video-title").first

        # Ohne sichtbaren Treffer keine falsche "Playing"-R?ckmeldung ausgeben.
        await first_video.wait_for(
            state="visible",
            timeout=15000,
        )

        title = await first_video.get_attribute("title")

        if not title:
            title = await first_video.inner_text()

        await first_video.click(timeout=15000)

        # Erst nach Wechsel auf /watch gilt das Video als ge?ffnet.
        await page.wait_for_url(
            "**/watch?*",
            timeout=15000,
        )

        return title.strip()

    async def close(self) -> None:
        # Schlie?t den Prozess, l?scht aber das persistente Browserprofil nicht.
        if self._context is not None and not self._context.is_closed():
            await self._context.close()

        self._context = None
        self._page = None

        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None
