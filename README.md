# Spotify Data Pipeline

This project implements a simple end‑to‑end ETL pipeline that retrieves your recently played Spotify tracks, transforms them into structured tables, and loads them into a SQLite database for analysis.

---

## Project Overview

The goal of this pipeline is to:

* Authenticate with the Spotify Web API
* Extract the 50 most recent tracks you listened to
* Transform Spotify's JSON into three relational tables: `plays`, `tracks`, and `artists`
* Load the results into a SQLite database (`spotify.db`)
* Query the database to analyze listening patterns

This project is lightweight and uses Python, Spotipy, pandas, and SQLAlchemy.

---

## Current Project Structure

```
spotify-data-pipeline/
│
├── config.py
├── spotify_client.py
├── extract_spotify.py
├── transform.py
├── load.py
├── run_pipeline.py
├── query.py
├── auth_test.py
└── spotify.db (generated after running pipeline)
```

---

## Setup Requirements

* Python 3.10+
* A Spotify Developer account
* Libraries:

  * spotipy
  * pandas
  * sqlalchemy

Installation:

```bash
pip install spotipy pandas sqlalchemy
```

---

## Spotify Developer Setup

1. Go to the Spotify Developer Dashboard.
2. Create a new application.
3. Add this redirect URI:

   ```
   http://127.0.0.1:8080/callback
   ```
4. Copy your **Client ID** and **Client Secret** into `config.py`.

---

## Configuration

`config.py` contains your app credentials:

```python
SPOTIFY_CLIENT_ID = "your-client-id"
SPOTIFY_CLIENT_SECRET = "your-client-secret"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8080/callback"
USERNAME = "your-spotify-username"
```

---

## Authentication

`spotify_client.py` is responsible for authenticating with Spotify:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

scope = "user-read-recently-played"

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        cache_path=".cache"
    ))
```

This function returns an authenticated Spotipy client used by the extraction step.

---

## Extraction

`extract_spotify.py` retrieves the 50 most recent plays:

```python
from spotify_client import get_spotify_client;

scope = "user-read-recently-played"

def get_recently_played(limit=50):
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=limit)
    return results["items"]

if __name__ == "__main__":
    items = get_recently_played()
    print(f"Fetched {len(items)} plays")

    for item in items[:5]:
        played_at = item["played_at"]
        track = item["track"]
        artist = track["artists"][0]["name"]
        print(played_at, "--", track["name"], " by", artist)
```

This module prints a preview when run directly.

---

## Transformation

`transform.py` turns each Spotify item into structured dictionaries:

```python
import pandas as pd

def transform_recently_played(items):

    plays, tracks, artists = [], [], []

    for item in items:
        played_at = item["played_at"]
        track = item["track"]
        artist = track["artists"][0]

        plays.append({
            "played_at": played_at,
            "track_id": track["id"], 
            "artist_id": artist["id"]        
        })

        tracks.append({
            "track_id": track["id"],
            "track_name": track["name"], 
            "album_name": track["album"]["name"],
            "duration_ms": track["duration_ms"]
        })

        artists.append({
            "artist_id": artist["id"], 
            "artist_name": artist["name"]
        })

        plays_df = pd.DataFrame(plays)
        tracks_df = pd.DataFrame(tracks).drop_duplicates(subset=["track_id"])
        artists_df = pd.DataFrame(artists).drop_duplicates(subset=["artist_id"])

    return plays_df, tracks_df, artists_df
```

---

## Loading

`load.py` loads the transformed data into SQLite:

```python
from sqlalchemy import create_engine

def get_engine(db_path="spotify.db"):
    return create_engine(f"sqlite:///{db_path}")

def load_to_db(plays_df, tracks_df, artists_df, db_path="spotify.db"):
    engine = get_engine(db_path)

    plays_df.to_sql("plays", engine, if_exists="append", index=False)
    tracks_df.to_sql("tracks", engine, if_exists="append", index=False)
    artists_df.to_sql("artists", engine, if_exists="append", index=False)
```

---

## Running the Full Pipeline

`run_pipeline.py` orchestrates extraction, transformation, and loading:

```python
from extract_spotify import get_recently_played
from transform import transform_recently_played
from load import load_to_db

def run_pipeline():

    print("fetching recently played tracks...")
    items = get_recently_played(limit=50)

    print("transforming data...")
    plays_df, tracks_df, artists_df = transform_recently_played(items)

    print("loading data...")
    load_to_db(plays_df, tracks_df, artists_df)

    print("finished! ")
    print(f"   Plays: {len(plays_df)}")
    print(f"   Tracks: {len(tracks_df)}")
    print(f" Arists: {len(artists_df)}")

if __name__ == "__main__":
    run_pipeline()
```

---

## Querying the Data

`query.py` contains example analytical queries:

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///spotify.db")

# top 10 tracks
query_tracks = """
SELECT t.track_name, a.artist_name, COUNT(*) AS play_count
FROM plays p
JOIN tracks t ON p.track_id = t.track_id
JOIN artists a ON p.artist_id = a.artist_id
GROUP BY p.track_id
ORDER BY play_count DESC
LIMIT 10;
"""

print("Top 10 Tracks: ")
df_tracks = pd.read_sql(query_tracks, engine)
print(df_tracks)

query_days = """
SELECT DATE(played_at) as day, COUNT(*) as plays
FROM plays
GROUP BY day
ORDER BY day DESC;
"""

df_days = pd.read_sql(query_days, engine)
print("
Plays per day:")
print(df_days)
```

---

## Potential Future Additions

* Correcting the indentation in `transform.py` so DataFrames are built after the loop
* Adding deduplication logic to `load.py` to avoid repeated inserts
* Adding error handling for extraction failures
* Improving the extraction function with safer `.get()` lookups
* Adding logging for better observability
* Automating pipeline execution via cron or Task Scheduler
* Transitioning from SQLite to PostgreSQL

---

## License

This project is provided under the MIT License.


## ATTRIBUTION
ChatGPT assisted me with the generation of this README.
