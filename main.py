import asyncio
import os
from urllib.parse import quote

from jarvis.skills.browser.browser_skill import BrowserSkill
from jarvis.skills.spotify.spotify_skill import SpotifySkill


def search_spotify(query: str) -> None:
    spotify_uri = f"spotify:search:{quote(query)}"
    os.startfile(spotify_uri)


async def main() -> None:
    print("Jarvis V0.1")

    browser = BrowserSkill()
    spotify = SpotifySkill()

    websites = {
        "open youtube": "https://www.youtube.com",
        "open google": "https://www.google.com",
        "open github": "https://www.github.com",
    }

    try:
        while True:
            try:
                raw_input = await asyncio.to_thread(input, "you < ")
            except EOFError:
                break

            raw_input = raw_input.strip()
            command = raw_input.lower()

            if command == "exit":
                print("Jarvis > Goodbye sir.")
                break

            if not command:
                continue

            try:
                if command in websites:
                    await browser.open_url(websites[command])
                    print(f"Jarvis > Opening {websites[command]}")
                    print("Jarvis > Press Strg+W to close the browser tab. Jarvis stays open.")
                    continue

                if command == "open spotify":
                    os.startfile("spotify:")
                    print("Jarvis > Opening Spotify")
                    continue

                if command == "pause spotify":
                    result = await asyncio.to_thread(spotify.pause)
                    print(f"Jarvis > {result}")
                    continue

                youtube_play_suffix = " on youtube"

                if command.startswith("play ") and command.endswith(youtube_play_suffix):
                    query = raw_input[5 : -len(youtube_play_suffix)].strip()

                    if not query:
                        print("Jarvis > What should I play?")
                        continue

                    title = await browser.play_youtube(query)
                    print(f"Jarvis > Playing on YouTube: {title}")
                    print("Jarvis > Press Strg+W to close the browser tab. Jarvis stays open.")
                    continue

                spotify_play_suffix = " on spotify"

                if command.startswith("play ") and command.endswith(spotify_play_suffix):
                    query = raw_input[5 : -len(spotify_play_suffix)].strip()

                    if not query:
                        print("Jarvis > What should I play?")
                        continue

                    print(f"Jarvis > Searching Spotify for '{query}'...")
                    result = await asyncio.to_thread(
                        spotify.play_track,
                        query,
                    )
                    print(f"Jarvis > {result}")
                    continue

                search_handled = False

                for service in ("youtube", "google", "github", "spotify"):
                    prefix = f"search {service} for "

                    if not command.startswith(prefix):
                        continue

                    query = raw_input[len(prefix) :].strip()

                    if not query:
                        print("Jarvis > What should I search for?")
                    elif service == "spotify":
                        search_spotify(query)
                        print(f"Jarvis > Searching Spotify for '{query}'")
                    else:
                        await browser.search(service, query)
                        print(f"Jarvis > Searching {service} for '{query}'")
                        print("Jarvis > Press Strg+W to close the browser tab. Jarvis stays open.")

                    search_handled = True
                    break

                if search_handled:
                    continue

                print(f"Jarvis > Sorry sir, I don't understand '{raw_input}'")

            except Exception as error:
                print(f"Jarvis > Error: {error}")

    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
