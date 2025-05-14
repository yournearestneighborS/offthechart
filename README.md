
# Billboard Hot 100 Scraper and Sentiment Analysis Pipeline**

This project automates the extraction, enrichment, and sentiment analysis of the Billboard's Hot 100 songs across selected years using a multi-stage pipeline integrating **Billboard scraping**, **Spotify genre tagging**, **Genius lyrics extraction**, and **NLP sentiment analysis**.

---

## 📦 Requirements
- Python 3.x
- Install required libraries:
  ```bash
  pip install billboard.py spotipy lyricsgenius pandas nltk matplotlib textblob beautifulsoup4 lxml
  ```
- Ensure you have valid API credentials for:
  - **Spotify** (Client ID & Secret)
  - **Genius** (Access Token)

---

## ⚙️ Pipeline Overview

### 1. `scraper.py`
Scrapes the Billboard Hot 100 chart using a spoofed user-agent to avoid blocking.
- **Outputs**: CSV file with song `rank`, `title`, and `artist`

**Usage:**
```bash
python scraper.py --date YYYY-MM-DD --save <output.csv>
```

---

### 2. `genre_finder.py`
Enhances Billboard data with **Spotify** and fallback **iTunes** genre labels. Also handles featured artist name cleanup.
- **Inputs**: Billboard CSV
- **Outputs**: CSV with `genre`

**Usage:**
```bash
python genre_finder.py --input <hot100.csv> --output <with_genres.csv>
```

---

### 3. `genius_lyrics.py`
Uses Genius API to fetch song lyrics for each `title`/`artist` pair, then cleans and stores them.
- **Inputs**: Billboard data + genres
- **Outputs**: CSV with `lyrics` and `clean_lyrics`

---

### 4. `cleanlyr_simpgenre.py`
Simplifies genres into broader categories (e.g., "Hip-Hop", "Pop", "Rock").
- **Inputs**: `lyrics_with_genres.csv`
- **Outputs**: `cleanlyrics_simplifiedgenre_<year>.csv`

---

### 5. `sentiment_analysis.py`
Performs dual sentiment scoring using **VADER** and **TextBlob**.
- Labels each song as **positive**, **neutral**, or **negative**
- Plots sentiment distribution & average sentiment by genre
- **Outputs**:
  - `lyrics_with_sentiment_<year>.csv`
  - `sentiment_distribution_<year>.png`
  - `sentiment_by_genre_<year>.png`

---

### 6. `compare_sentiments_by_year.py`
Generates a cross-year comparison of sentiment labels.
- **Inputs**: All `lyrics_with_sentiment_<year>.csv`
- **Output**: `sentiment_by_year.png`

---

## 📊 Output Files Summary
- `hot100_<year>.csv` — Raw scraped chart data
- `hot100_<year>_with_genres.csv` — Billboard data with genres
- `lyrics_<year>_data.csv` — Lyrics from Genius
- `cleanlyrics_simplifiedgenre_<year>.csv` — Cleaned lyrics + simplified genre
- `lyrics_with_sentiment_<year>.csv` — Final dataset with sentiment scores
- `sentiment_distribution_<year>.png` — VADER sentiment distribution bar chart
- `sentiment_by_genre_<year>.png` — Genre-level sentiment bar chart
- `sentiment_by_year.png` — Sentiment comparison across all selected years

---

## 📋 Author
**Oluwaseyi Caleb Folorunso**
