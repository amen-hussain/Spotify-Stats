import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import matplotlib.pyplot as plt

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="184ae6921cae495a907c27d3eea38b08",
    client_secret="1e02df59bcee4b2d803098e15045b82f",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read"
))

# Fetch your top tracks
top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')

if not top_tracks or 'items' not in top_tracks:
    print("Failed to fetch top tracks. Check your credentials or scopes.")
else:
    artist_ids = []
    for track in top_tracks['items']:
        for artist in track['artists']:
            artist_ids.append(artist['id'])

    # Fetch genres
    genres = []
    for artist_id in set(artist_ids):
        artist = sp.artist(artist_id)
        genres.extend(artist['genres'])

    # Count genres
    genre_counter = Counter(genres)
    top_genres = genre_counter.most_common(10)

    print("\nTop Genres:")
    for genre, count in top_genres:
        print(f"{genre}: {count}")

    # Prepare data for plotting
    genre_names = [genre for genre, count in top_genres]
    genre_counts = [count for genre, count in top_genres]

    # --- Create Pie Chart with Exploded Top 3 ---
    plt.figure(figsize=(8, 8))

    # Explode settings: explode first 3 slices slightly (0.1 offset), others stay at 0
    explode = [0.1 if i < 3 else 0 for i in range(len(genre_names))]

    wedges, texts, autotexts = plt.pie(
        genre_counts,
        labels=genre_names,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors,
        explode=explode
    )

    # Styling text inside pie slices
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)

    # Nice personalized title
    plt.title("Amen Hussain's Top Spotify Genres (2024)", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()

    # Save the pie chart
    plt.savefig('/Users/amenhussain/Python_Projects/top_genres_pie_chart_only.png', dpi=300)
    plt.show()
