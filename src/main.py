"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    
    user_prefs = {
    "genre": {
        "preferred": {
            "lofi": 1.0,
            "jazz": 0.6,
            "ambient": 0.5,
            "acoustic": 0.4
        },
        "avoid": {
            "rock": 1.0,
            "metal": 1.0
        }
    },
    "mood": {
        "preferred": {
            "chill": 1.0,
            "calm": 0.8,
            "focus": 0.7,
            "relaxed": 0.7
        },
        "avoid": {
            "aggressive": 1.0,
            "intense": 0.9
        }
    },
    "energy": {
        "range": [0.2, 0.5],
        "ideal": 0.35,
        "weight": 1.0
    },
    "tempo_bpm": {
        "range": [65, 95],
        "ideal": 78,
        "weight": 0.9
    },
    "valence": {
        "range": [0.45, 0.75],
        "ideal": 0.6,
        "weight": 0.6
    },
    "danceability": {
        "range": [0.45, 0.7],
        "ideal": 0.58,
        "weight": 0.5
    },
    "acousticness": {
        "range": [0.55, 0.95],
        "ideal": 0.8,
        "weight": 0.8
    }
}
    

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        print("\n" + "="*60)
        print("TOP MUSIC RECOMMENDATIONS FOR YOU")
        print("="*60 + "\n")

        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"{i}. {song['title']}")
            print(f"   Score: {score:.2f}/10.0")
            print(f"   Why: {explanation}")
            print()

        print("="*60)
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
