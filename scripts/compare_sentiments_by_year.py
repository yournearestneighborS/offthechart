import pandas as pd
import matplotlib.pyplot as plt

# ========== SETUP ==========

years = [None] #INPUT!!! Change to to the desired years
sentiment_counts_by_year = {}

# ========== LOAD AND COUNT SENTIMENTS ==========

for year in years:
    df = pd.read_csv(f"lyrics_with_sentiment_{year}.csv")
    counts = df["sentiment_label"].value_counts()
    sentiment_counts_by_year[year] = {
        "positive": counts.get("positive", 0),
        "neutral": counts.get("neutral", 0),
        "negative": counts.get("negative", 0)
    }

# ========== PREP FOR PLOTTING ==========

import numpy as np

labels = ["positive", "neutral", "negative"]
x = np.arange(len(labels))  # label positions
width = 0.2  # bar width

fig, ax = plt.subplots(figsize=(10, 6))

for idx, year in enumerate(years):
    offsets = x + (idx - len(years)/2) * width + width/2
    values = [sentiment_counts_by_year[year][label] for label in labels]
    ax.bar(offsets, values, width=width, label=str(year))

# ========== LABELING ==========

ax.set_ylabel("Number of Songs")
ax.set_title("Sentiment Distribution by Year")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(title="Year")
plt.tight_layout()
plt.savefig("sentiment_by_year.png")
plt.show()