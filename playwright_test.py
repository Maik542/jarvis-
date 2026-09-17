import asyncio
import os
import re
from pathlib import Path
from urllib.parse import quote_plus

from playwright.async_api import (
    Page,
    Playwright,
    async_playwright,
)
from playwright.async_api import (
    TimeoutError as PlaywrightTimeoutError,
)


async def handle_cookie_window(page: Page) -> None:
    reject_text = page.get_by_text(
        re.compile(
            r"^(Alle ablehnen|Reject all)$",
            re.IGNORECASE,
        )
    ).first

    try:
        await reject_text.wait_for(
            state="attached",
            timeout=10000,
        )

        print("Jarvis > Cookie window detected.")

        await reject_text.click(
            timeout=10000,
        )

        await reject_text.wait_for(
            state="hidden",
            timeout=10000,
        )

        print("Jarvis > Optional cookies rejected.")

    except PlaywrightTimeoutError:
        print("Jarvis > No cookie window detected.")


async def search_youtube(
    playwright: Playwright,
    profile_directory: Path,
    query: str,
) -> None:
    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"

    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(profile_directory),
        channel="chrome",
        headless=False,
        ignore_default_args=["--disable-extensions"],
        chromium_sandbox=True,
    )

    try:
        if context.pages:
            page = context.pages[0]
        else:
            page = await context.new_page()

        print("Jarvis > Starting persistent browser.")

        await page.goto(
            search_url,
            wait_until="domcontentloaded",
        )

        await handle_cookie_window(page)

        print("Jarvis > Searching for the first video.")

        try:
            first_video = page.locator("ytd-video-renderer").locator("a#video-title").first

            await first_video.wait_for(
                state="visible",
                timeout=15000,
            )

            video_title = await first_video.get_attribute("title")

            print(f"Jarvis > Opening: {video_title}")

            await first_video.click(
                timeout=15000,
            )

            await page.wait_for_url(
                "**/watch?*",
                timeout=15000,
            )

            current_url = page.url
            current_title = await page.title()

            print(f"Jarvis > Video page opened: {current_title}")
            print(f"Jarvis > Current URL: {current_url}")

        except PlaywrightTimeoutError:
            print("Jarvis > I could not find or open a video.")

        await asyncio.to_thread(
            input,
            "Jarvis > Press Enter to close the browser.",
        )

    finally:
        await context.close()

    print("Jarvis > Browser closed. Ready for another search.")


async def main() -> None:
    local_app_data = os.environ["LOCALAPPDATA"]

    profile_directory = Path(local_app_data) / "Jarvis" / "BrowserProfile"

    async with async_playwright() as playwright:
        while True:
            raw_query = await asyncio.to_thread(
                input,
                "YouTube search > ",
            )

            query = raw_query.strip()

            if query.lower() == "exit":
                print("Jarvis > Goodbye sir.")
                break

            if not query:
                print("Jarvis > Please enter a search term.")
                continue

            await search_youtube(
                playwright,
                profile_directory,
                query,
            )


if __name__ == "__main__":
    asyncio.run(main())
