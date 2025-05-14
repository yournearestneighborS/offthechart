import pandas as pd
import lyricsgenius
import time
import re
import string

# ========== SETUP ==========

# Replace with your actual token
genius = lyricsgenius.Genius(
    "your_Genius_token_here",
    skip_non_songs=True,
    remove_section_headers=True,
    retries=3,
    timeout=15
)

year = None  # INPUT!!! Change this to the desired year if needed

# Load your Billboard chart data
df = pd.read_csv(f"hot100_{year}.csv")  # Base file with title/artist
genre_df = pd.read_csv(f"hot100_{year}_with_genres.csv")  # Must include 'title', 'artist', 'genre'

# Merge on title and artist (exact match)
df = pd.merge(df, genre_df[["title", "artist", "genre"]], on=["title", "artist"], how="left")

# ========== CLEANING FUNCTIONS ==========

def clean_lyrics(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\[.*?\]", "", text)  # Remove [Verse], [Chorus], etc.
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = text.lower()  # Lowercase
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace
    return text

def clean_artist_name(artist_raw):
    artist_name = artist_raw.lower()
    for separator in [' featuring ', ' feat. ', ' ft. ', ' with ', ', ', ' & ', ' x ', ' and ']:
        if separator in artist_name:
            artist_name = artist_name.split(separator)[0]
            break
    return artist_name.strip().title()

# ========== FETCH LOOP ==========

lyrics_data = []

for idx, row in df.iterrows():
    title = row["title"]
    raw_artist = row["artist"]
    genre = row.get("genre", None)

    try:
        cleaned_artist = clean_artist_name(raw_artist)

        # Try cleaned artist first
        song = genius.search_song(title, cleaned_artist)
        if not song or not song.lyrics:
            # Fallback to raw artist
            song = genius.search_song(title, raw_artist)

    except Exception as e:
        print(f"⚠️ Error searching Genius for {title}: {e}")
        song = None

    if song and song.lyrics:
        raw_lyrics = song.lyrics

        # --- Start: Clean pre- and post-lyric junk ---

        # Remove everything before the first real lyric line (skip intro text)
        lines = raw_lyrics.splitlines()
        lyrics_start = 0

        for i, line in enumerate(lines):
            # Look for the first non-empty line that doesn't contain common junk
            if line.strip() and not any(keyword in line.lower() for keyword in [
                "you might", "embed", "translations", "contributors", "more on genius"
            ]):
                lyrics_start = i
                break

        raw_lyrics = "\n".join(lines[lyrics_start:])

        # Remove post-song content like contributor info or recommendations
        for marker in ["You might also like", "Embed", "Translations", "Contributors", "More on Genius"]:
            if marker in raw_lyrics:
                raw_lyrics = raw_lyrics.split(marker)[0].strip()

        # --- End Clean ---

        lyrics_data.append({
            "song_title": title,
            "artist": raw_artist,
            "genre": genre,
            "lyrics": raw_lyrics,
            "clean_lyrics": clean_lyrics(raw_lyrics)
        })
        print(f"✅ Fetched: {title} by {raw_artist}")
    else:
        print(f"❌ Not found: {title} by {raw_artist}")

    time.sleep(1)

# ========== SAVE TO CSV ==========

lyrics_df = pd.DataFrame(lyrics_data)
lyrics_df.to_csv(f"lyrics_{year}_data.csv", index=False)
print(f"✅ Lyrics with genres saved to 'lyrics_{year}_data.csv'")