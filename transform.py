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

    # watch indentation smh
    return plays_df, tracks_df, artists_df