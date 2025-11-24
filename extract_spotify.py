from spotify_client import get_spotify_client;

scope = "user-read-recently-played"

def get_recently_played(limit=50):
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=limit)
    return results["items"]

if __name__ == "__main__":
    items = get_recently_played()
    print(f"Fetched {len(items)} plays")

    # Printing items for debugging
    for item in items[:5]:
        played_at = item["played_at"]
        track = item["track"]
        artist = track["artists"][0]["name"]
        print(played_at, "--", track["name"], "written by", artist)