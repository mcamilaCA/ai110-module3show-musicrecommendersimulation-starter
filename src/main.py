"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate

from recommender import UserProfile, load_songs, recommend_songs


MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    # user_prefs = {"genre": "pop ", "mood": "happy", "energy": 0.8, "acousticness": True}
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": True}
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": float("nan"), "acousticness": 0.3}
    # user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": True, "danceability": 1.0}
    # user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": 0.8, "wants_instrumental": True, "preferred_decade": "1990s", "clean_only": True}
    user_prefs = {
        "genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2,
        "preferred_decade": "2020s", "wants_instrumental": False,
        "clean_only": True, "prefer_popular": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 70)
    print("🎵  YOUR TOP SONG RECOMMENDATIONS  🎵")
    print("=" * 70)
    print(f"👤 Profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']} | acousticness={user_prefs['acousticness']}")
    print(
        f"   decade={user_prefs.get('preferred_decade', 'any')} | "
        f"wants_instrumental={user_prefs.get('wants_instrumental', 'no preference')} | "
        f"clean_only={user_prefs.get('clean_only', False)} | "
        f"prefer_popular={user_prefs.get('prefer_popular', False)}"
    )
    print("=" * 70)
    print()

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        medal = MEDALS.get(rank, "🎶")
        why = "\n".join(line.strip() for line in explanation.strip().split("\n"))
        rows.append([f"{medal} #{rank}", song["title"], song["artist"], f"{score:.1f}/100", why])

    print(tabulate(rows, headers=["Rank", "Song", "Artist", "Score", "Why"], tablefmt="fancy_grid"))
    print("\n🎧 Enjoy the music!\n")


if __name__ == "__main__":
    main()
