import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import time

# --- Spotify API credentials (hardcoded) ---
SPOTIFY_CLIENT_ID = "your_spotify_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret_here"

def clean_artist_name(artist_raw):
    artist_name = artist_raw.lower()
    for separator in [' featuring ', ' feat. ', ' ft. ', ' with ', ', ', ' & ']:
        if separator in artist_name:
            artist_name = artist_name.split(separator)[0]
            break
    return artist_name.strip().title()

def fetch_genres(df):
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_spotify_genre(artist_name):
        try:
            results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
            items = results['artists']['items']
            if items and items[0].get("genres"):
                return ", ".join(items[0]["genres"])
        except Exception as e:
            print(f"❌ Spotify error for '{artist_name}': {e}")
        return None

    def get_itunes_genre(artist_name):
        try:
            response = requests.get("https://itunes.apple.com/search", params={
                "term": artist_name,
                "entity": "musicArtist",
                "limit": 1
            })
            data = response.json()
            if data["resultCount"] > 0:
                return data["results"][0].get("primaryGenreName")
        except Exception as e:
            print(f"❌ iTunes error for '{artist_name}': {e}")
        return None

    genres_list = []

    for i, row in df.iterrows():
        artist_raw = row['artist']
        artist_cleaned = clean_artist_name(artist_raw)

        # 1. Spotify with raw artist
        genre = get_spotify_genre(artist_raw)
        if genre:
            print(f"✅ Spotify (raw): {artist_raw} — {genre}")
            genres_list.append(genre)
            continue

        # 2. iTunes with raw artist
        genre = get_itunes_genre(artist_raw)
        if genre:
            print(f"✅ iTunes (raw): {artist_raw} — {genre}")
            genres_list.append(genre)
            continue

        # 3. Spotify with cleaned artist
        genre = get_spotify_genre(artist_cleaned)
        if genre:
            print(f"✅ Spotify (clean): {artist_cleaned} — {genre}")
            genres_list.append(genre)
            continue

        # 4. iTunes with cleaned artist
        genre = get_itunes_genre(artist_cleaned)
        if genre:
            print(f"✅ iTunes (clean): {artist_cleaned} — {genre}")
        else:
            print(f"⚠️ No genre found for {artist_raw}")
        genres_list.append(genre)

        time.sleep(0.2)  # Respect API rate limits

    df['genre'] = genres_list
    return df

def main():
    parser = argparse.ArgumentParser(description="Fetch genres from Spotify and iTunes")
    parser.add_argument("--input", type=str, required=True, help="Input CSV path")
    parser.add_argument("--output", type=str, required=True, help="Output CSV path")

    args = parser.parse_args()

    df = pd.read_csv(args.input)
    enriched_df = fetch_genres(df)
    enriched_df.to_csv(args.output, index=False)
    print(f"💾 Enriched data saved to {args.output}")

if __name__ == "__main__":
    main()