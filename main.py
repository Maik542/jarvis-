import asyncio
import os
from urllib.parse import quote

from jarvis.skills.browser.browser_skill import BrowserSkill
from jarvis.skills.spotify.spotify_skill import SpotifySkill


# Aktueller Programmeinstieg: Die Befehle werden hier direkt ausgewertet.
# JarvisAgent in jarvis/core/agent.py ist noch nicht mit dieser CLI verbunden.
def search_spotify(query: str) -> None:
    # Diese URI zeigt nur Suchergebnisse in der Desktop-App; sie startet nichts.
    spotify_uri = f"spotify:search:{quote(query)}"
    os.startfile(spotify_uri)


async def main() -> None:
    print("Jarvis V0.1")

    # Beide Skills bleiben f?r die ganze Eingabeschleife erhalten. So kann
    # ein weiterer Befehl denselben Browser und dieselbe Spotify-Sitzung nutzen.
    browser = BrowserSkill()
    spotify = SpotifySkill()

    # Kurze "open"-Befehle werden hier auf feste Startseiten abgebildet.
    websites = {
        "open youtube": "https://www.youtube.com",
        "open google": "https://www.google.com",
        "open github": "https://www.github.com",
    }

    try:
        while True:
            try:
                # input() ist blockierend; im Thread bleibt die asyncio-Schleife frei.
                raw_input = await asyncio.to_thread(input, "you < ")
            except EOFError:
                break

            raw_input = raw_input.strip()
            # Nur zum Vergleichen kleinschreiben: Suchtexte behalten ihre Schreibweise.
            command = raw_input.lower()

            if command == "exit":
                # Verl?sst die Schleife; finally r?umt danach den Browser auf.
                print("Jarvis > Goodbye sir.")
                break

            if not command:
                continue

            try:
                # Jede erkannte Aktion beendet nur diesen Durchlauf per continue;
                # die n?chste Eingabe folgt ohne Neustart von Jarvis.
                if command in websites:
                    await browser.open_url(websites[command])
                    print(f"Jarvis > Opening {websites[command]}")
                    print("Jarvis > Press Strg+W to close the browser tab. Jarvis stays open.")
                    continue

                if command == "open spotify":
                    # URI-Schema von Windows: die installierte Spotify-App ?ffnen.
                    os.startfile("spotify:")
                    print("Jarvis > Opening Spotify")
                    continue

                if command == "pause spotify":
                    # Spotipy ist synchron; to_thread h?lt die Eingabe-Schleife frei.
                    result = await asyncio.to_thread(spotify.pause)
                    print(f"Jarvis > {result}")
                    continue

                youtube_play_suffix = " on youtube"

                # "play" startet ein Video; "search" weiter unten zeigt nur Treffer.
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

                # Die Spotify-Web-API arbeitet synchron und l?uft deshalb im Thread.
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

                # Derselbe Syntaxaufbau f?r alle Suchdienste. Nur Spotify nutzt
                # eine Desktop-URI; die anderen Ziele laufen ?ber BrowserSkill.
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
                # Ein fehlgeschlagener Befehl darf die CLI nicht beenden.
                print(f"Jarvis > Error: {error}")

    finally:
        # Nur den von Jarvis gestarteten Browser schlie?en, nicht die Spotify-App.
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
