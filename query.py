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

df_tracks = pd.read_sql(query_tracks, engine)
print("Top 10 Tracks: ")
print(df_tracks)

query_days = """
SELECT DATE(played_at) as day, COUNT(*) as plays
FROM plays
GROUP BY day
ORDER BY day DESC;
"""

df_days = pd.read_sql(query_days, engine)
print("\nPlays per day:")
print(df_days)
