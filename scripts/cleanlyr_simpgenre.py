import pandas as pd

# Re-define the file path after kernel reset
year = None # INPUT! Change to desired year
file_path = f"lyrics_{year}_data.csv"
df = pd.read_csv(file_path)

# Simplify genre using the provided function
def simplify_genre(genre_str):
    if not isinstance(genre_str, str):
        return "Unknown"
    
    genre_str = genre_str.lower()
   
    if "christian" in genre_str or "gospel" in genre_str or "worship" in genre_str:
        return "Christian"
    elif "hip hop" in genre_str or "rap" in genre_str or "trap" in genre_str:
        return "Hip-Hop"
    elif "pop" in genre_str or "contemporary" in genre_str or "synthpop" in genre_str or "dance pop" in genre_str or "doo-wop" in genre_str:
        return "Pop"
    elif "rock" in genre_str or "punk" in genre_str or "grunge" in genre_str or "post-grunge" in genre_str or "post-rock" in genre_str:
        return "Rock"
    elif "r&b" in genre_str or "new jack swing" in genre_str:
        return "R&B"
    elif "soul" in genre_str:
        return "Soul"
    elif "country" in genre_str:
        return "Country"
    elif "dance" in genre_str or "electronic" in genre_str or "edm" in genre_str or "house" in genre_str or "trance" in genre_str:
        return "Dance"
    elif "latin" in genre_str or "reggaeton" in genre_str:
        return "Latin"
    elif "folk" in genre_str:
        return "Folk"
    elif "metal" in genre_str:
        return "Metal"
    elif "jazz" in genre_str:
        return "Jazz"
    elif "blues" in genre_str:
        return "Blues"
    elif "alternative" in genre_str:
        return "Alternative"
    elif "latino" in genre_str or "reggaeton" in genre_str or "latin" in genre_str:
        return "Reggaeton"
    elif "k-pop" in genre_str or "korean pop" in genre_str:
        return "K-Pop"
    elif "christmas" in genre_str or "holiday" in genre_str:
        return "Holiday"
    elif "disco" in genre_str:
        return "Disco"
    else:
        return "Other"

# Apply simplification
df["simplified_genre"] = df["genre"].apply(simplify_genre)

# Extract desired columns
result_df = df[["song_title", "artist", "simplified_genre", "clean_lyrics"]]

# Save the result

output_path = f"cleanlyrics_simplifiedgenre_{year}.csv"
result_df.to_csv(output_path, index=False)