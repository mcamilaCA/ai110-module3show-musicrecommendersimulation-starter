"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "accousticness": 0.2}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 70)
    print("🎵  YOUR TOP SONG RECOMMENDATIONS  🎵")
    print("=" * 70)
    print(f"👤 Profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']} | accousticness={user_prefs['accousticness']}")
    print("=" * 70)
    print()

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        medal = MEDALS.get(rank, "🎶")
        print(f"{medal} #{rank}  {song['title']} — {song['artist']}")
        print(f"   ⭐ Score: {score:.1f}/100")
        print(explanation)
        print("-" * 70)

    print("\n🎧 Enjoy the music!\n")


if __name__ == "__main__":
    main()
