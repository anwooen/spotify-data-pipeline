from sqlalchemy import create_engine

def get_engine(db_path="spotify.db"):
    return create_engine(f"sqlite:///{db_path}")

def load_to_db(plays_df, tracks_df, artists_df, db_path="spotify.db"):
    
    engine = get_engine(db_path)

    plays_df.to_sql("plays", engine, if_exists="append", index=False)
    tracks_df.to_sql("tracks", engine, if_exists="append", index=False)
    artists_df.to_sql("artists", engine, if_exists="append", index=False)
