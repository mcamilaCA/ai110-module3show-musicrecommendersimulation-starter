import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Point-weighting strategy (must sum to 1.0).
# Genre and mood are categorical (all-or-nothing match), so they carry more
# weight than the continuous, self-correcting energy/acousticness distances.
# See README "How The System Works" for the reasoning behind this ordering.
WEIGHT_GENRE = 0.35
WEIGHT_MOOD = 0.30
WEIGHT_ENERGY = 0.20
WEIGHT_ACOUSTICNESS = 0.15

# Target acousticness anchors for a boolean "likes acoustic" preference.
# 0.85/0.15 rather than 1.0/0.0 so the most extreme catalog outliers don't
# swallow all the credit relative to songs that are still clearly acoustic/electronic.
ACOUSTIC_TARGET_LIKED = 0.85
ACOUSTIC_TARGET_DISLIKED = 0.15


def acoustic_target(likes_acoustic: bool) -> float:
    return ACOUSTIC_TARGET_LIKED if likes_acoustic else ACOUSTIC_TARGET_DISLIKED


def _score_core(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    target_acousticness: float,
) -> Tuple[float, List[str]]:
    """
    Shared scoring formula used by both the OOP (Recommender) and functional
    (score_song) APIs, so the two paths can never drift out of sync.
    Returns a 0-100 score plus a human-readable reason per feature.
    """
    genre_match = 1.0 if genre == favorite_genre else 0.0
    mood_match = 1.0 if mood == favorite_mood else 0.0
    energy_similarity = 1.0 - abs(energy - target_energy)
    acoustic_similarity = 1.0 - abs(acousticness - target_acousticness)

    score = 100 * (
        WEIGHT_GENRE * genre_match
        + WEIGHT_MOOD * mood_match
        + WEIGHT_ENERGY * energy_similarity
        + WEIGHT_ACOUSTICNESS * acoustic_similarity
    )

    reasons = [
        f"Genre {'matches' if genre_match else 'does not match'} "
        f"({genre} vs {favorite_genre}) -> +{WEIGHT_GENRE * genre_match * 100:.1f} pts",
        f"Mood {'matches' if mood_match else 'does not match'} "
        f"({mood} vs {favorite_mood}) -> +{WEIGHT_MOOD * mood_match * 100:.1f} pts",
        f"Energy similarity {energy_similarity:.2f} "
        f"(song={energy:.2f}, target={target_energy:.2f}) -> +{WEIGHT_ENERGY * energy_similarity * 100:.1f} pts",
        f"Acousticness similarity {acoustic_similarity:.2f} "
        f"(song={acousticness:.2f}, target={target_acousticness:.2f}) -> +{WEIGHT_ACOUSTICNESS * acoustic_similarity * 100:.1f} pts",
    ]
    return score, reasons


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Optional: only used as a tie-breaker, so callers that don't care about
    # danceability (like the starter tests) aren't forced to supply it.
    preferred_danceability: float = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        target_acousticness = acoustic_target(user.likes_acoustic)

        def sort_key(song: Song) -> Tuple[float, float]:
            score, _ = _score_core(
                song.genre, song.mood, song.energy, song.acousticness,
                user.favorite_genre, user.favorite_mood, user.target_energy, target_acousticness,
            )
            # Tie-breaker only: closer danceability wins when scores are equal.
            tie_break = -abs(song.danceability - user.preferred_danceability)
            return (score, tie_break)

        ranked = sorted(self.songs, key=sort_key, reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        target_acousticness = acoustic_target(user.likes_acoustic)
        score, reasons = _score_core(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood, user.target_energy, target_acousticness,
        )
        lines = [f"{song.title} scored {score:.1f}/100:"]
        lines.extend(f"  - {reason}" for reason in reasons)
        return "\n".join(lines)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    numeric_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    user_prefs supports: genre, mood, energy, likes_acoustic (optional).
    likes_acoustic is optional so callers (like the starter main.py profile)
    that don't specify it still get a sensible neutral score instead of a crash.
    """
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is None:
        target_acousticness = 0.5
    else:
        target_acousticness = acoustic_target(likes_acoustic)

    return _score_core(
        song.get("genre"),
        song.get("mood"),
        float(song.get("energy", 0.0)),
        float(song.get("acousticness", 0.0)),
        user_prefs.get("genre"),
        user_prefs.get("mood"),
        float(user_prefs.get("energy", 0.5)),
        target_acousticness,
    )

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    preferred_danceability = user_prefs.get("danceability")

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        if preferred_danceability is None:
            tie_break = 0.0
        else:
            tie_break = -abs(float(song.get("danceability", 0.0)) - preferred_danceability)
        scored.append((song, score, reasons, tie_break))

    scored.sort(key=lambda item: (item[1], item[3]), reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons, _ in scored[:k]]
