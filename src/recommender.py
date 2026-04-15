from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


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


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []  # This will hold all song dictionaries

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)  # Reads each row as a dictionary

        for row in reader:
            # Convert numeric fields to the correct types
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores each song against user preferences and returns the top k.
    Returns a list of (song_dict, score, explanation) tuples.
    """
    scored = []

    for song in songs:
        score = 0.0
        reasons = []

        # Score each numeric feature if it appears in user_prefs
        for feature in ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]:
            if feature not in user_prefs:
                continue

            prefs = user_prefs[feature]
            value = song[feature]
            low, high = prefs["range"]
            ideal = prefs["ideal"]
            weight = prefs.get("weight", 1.0)

            if low <= value <= high:
                # Closer to ideal = higher score (max 1.0 per feature)
                distance = abs(value - ideal) / max(high - low, 0.001)
                feature_score = (1.0 - distance) * weight
                score += feature_score
                reasons.append(f"{feature}={value:.2f} (ideal {ideal})")

        # Bonus for preferred genre
        genre_prefs = user_prefs.get("genre", {})
        preferred_genres = genre_prefs.get("preferred", {})
        avoided_genres = genre_prefs.get("avoid", {})

        if song["genre"] in preferred_genres:
            score += preferred_genres[song["genre"]]
            reasons.append(f"genre '{song['genre']}' preferred")
        elif song["genre"] in avoided_genres:
            score -= avoided_genres[song["genre"]]

        explanation = ", ".join(reasons) if reasons else "general match"
        scored.append((song, score, explanation))

    # Sorting feature: highest score first
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return top-k
    return scored[:k]