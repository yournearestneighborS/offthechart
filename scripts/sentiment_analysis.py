import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt

# ========== SETUP ==========
nltk.download("vader_lexicon")
vader = SentimentIntensityAnalyzer()

year = 1965  # INPUT!!! Change this to the desired year

# ========== LOAD LYRICS DATA ==========
df = pd.read_csv(f"cleanlyrics_simplifiedgenre_{year}.csv")

# ========== SENTIMENT FUNCTIONS ==========
def get_vader_sentiment(text):
    if isinstance(text, str):
        return vader.polarity_scores(text)["compound"]
    return 0.0

def get_textblob_sentiment(text):
    if isinstance(text, str):
        return TextBlob(text).sentiment.polarity
    return 0.0

def label_sentiment(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

# ========== APPLY SENTIMENT ==========
df["vader_sentiment"] = df["clean_lyrics"].apply(get_vader_sentiment)
df["textblob_sentiment"] = df["clean_lyrics"].apply(get_textblob_sentiment)
df["sentiment_label"] = df["vader_sentiment"].apply(label_sentiment)

# ========== SAVE (Only selected columns) ==========
output_cols = ["song_title", "artist", "simplified_genre", "vader_sentiment", "textblob_sentiment", "sentiment_label"]
df[output_cols].to_csv(f"lyrics_with_sentiment_{year}.csv", index=False)
print(f"✅ Sentiment analysis complete. Output saved to 'lyrics_with_sentiment_{year}.csv'")

# ========== PLOT 1: Sentiment Distribution ==========
sentiment_counts = df["sentiment_label"].value_counts()
colors = ['blue' if label == 'positive' else 'red' for label in sentiment_counts.index]

plt.figure(figsize=(12, 6))
bars = plt.bar(sentiment_counts.index, sentiment_counts.values, color=colors)
plt.title("Sentiment Distribution of Lyrics")
plt.xlabel("Sentiment")
plt.ylabel("Number of Songs")

# Add bar labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 1, int(height), ha='center', va='bottom')

plt.savefig(f"sentiment_distribution_{year}.png")
plt.show()

# ========== PLOT 2: Average VADER Sentiment by Genre ==========
genre_sentiment = df.groupby("simplified_genre").agg(
    avg_sentiment=("vader_sentiment", "mean"),
    song_count=("vader_sentiment", "count")
).sort_values("avg_sentiment", ascending=False)

colors = ['blue' if score >= 0 else 'red' for score in genre_sentiment["avg_sentiment"]]

plt.figure(figsize=(12, 6))
bars = plt.bar(genre_sentiment.index, genre_sentiment["avg_sentiment"], color=colors)
plt.axhline(0, color='black', linestyle='--', linewidth=1)  # horizontal line at y=0
plt.title("Average VADER Sentiment Score by Genre")
plt.xlabel("Genre")
plt.ylabel("Average Sentiment (Compound Score)")
plt.xticks(rotation=45, ha="right")

# Add count labels
for bar, count in zip(bars, genre_sentiment["song_count"]):
    height = bar.get_height()
    offset = 0.02 if height >= 0 else -0.05
    va = 'bottom' if height >= 0 else 'top'
    plt.text(bar.get_x() + bar.get_width() / 2, height + offset, str(count), ha='center', va=va)

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='blue', label='Positive'), Patch(facecolor='red', label='Negative')]
plt.legend(handles=legend_elements, title="Sentiment Polarity")

plt.tight_layout()
plt.savefig(f"sentiment_by_genre_{year}.png")
plt.show()