from extract_spotify import get_recently_played
from transform import transform_recently_played
from load import load_to_db

def run_pipeline():

    print("fetching recently played tracks...")
    items = get_recently_played(limit=50)

    print("transforming data...")
    plays_df, tracks_df, artists_df = transform_recently_played(items)

    #print("debug print", plays_df)

    print("loading data...")
    load_to_db(plays_df, tracks_df, artists_df)

    print("finished! ")
    print(f"   Plays: {len(plays_df)}")
    print(f"   Tracks: {len(tracks_df)}")
    print(f" Arists: {len(artists_df)}")

if __name__ == "__main__":
    run_pipeline()