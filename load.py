from sqlalchemy import create_engine
import pandas as pd

def get_engine(db_path="spotify.db"):
    return create_engine(f"sqlite:///{db_path}")

def load_to_db(plays_df, tracks_df, artists_df, db_path="spotify.db"):
    
    engine = get_engine(db_path)


    # deduplication logic to only add new records to the database
    try:
        existing_plays = pd.read_sql("SELECT played_at, track_id, artist_id FROM plays", engine)
        plays_df = plays_df.merge(
            existing_plays,
            on=["played_at", "track_id", "artist_id"],
            how="left",
            indicator=True
        )
        plays_df = plays_df[plays_df["_merge"] == "left_only"].drop(columns=["_merge"])
    except:
        pass

    try:
        existing_tracks = pd.read_sql("SELECT track_id FROM tracks", engine)
        tracks_df = tracks_df.merge(existing_tracks, on="track_id", how="left", indicator=True)
        tracks_df = tracks_df[tracks_df["_merge"] == "left_only"].drop(columns=["_merge"])
    except:
        pass

    try:
        existing_artists = pd.read_sql("SELECT artist_id FROM artists", engine)
        artists_df = artists_df.merge(existing_artists, on="artist_id", how="left", indicator=True)
        artists_df = artists_df[artists_df["_merge"] == "left_only"].drop(columns=["_merge"])
    except:
        pass


    plays_df.to_sql("plays", engine, if_exists="append", index=False)
    tracks_df.to_sql("tracks", engine, if_exists="append", index=False)
    artists_df.to_sql("artists", engine, if_exists="append", index=False)
