from spotify_client import get_spotify_client

scope = "user-read-recently-played"

sp = get_spotify_client()

result = sp.current_user_recently_played(limit = 5)
for item in result["items"]:
    track = item["track"]
    print(track["name"], "-", track["artists"][0]["name"])