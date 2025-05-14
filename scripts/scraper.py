import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_chart(date=None):
    if date:
        url = f"https://www.billboard.com/charts/hot-100/{date}"
    else:
        url = "https://www.billboard.com/charts/hot-100" 

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" # Use a common user agent to avoid blocking
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch chart: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "lxml")  # Use faster parser if installed

    chart_items = soup.find_all("li", class_="o-chart-results-list__item")
    chart_data = []

    forbidden_labels = {"NEW", "RE-ENTRY", "HOT SHOT DEBUT"} # Set of labels to filter out unwanted entries
    
    for item in chart_items:
        title_tag = item.find("h3", id="title-of-a-story")
        title = title_tag.get_text(strip=True) if title_tag else None

        # Find the first valid artist inside span.c-label
        artist = None
        for span in item.find_all("span", class_="c-label"):
            text = span.get_text(strip=True)
            words = text.split()
            if (
                text 
                and not text.isdigit() 
                and text not in forbidden_labels
                and not (text.isupper() and len(words) >= 2)
            ): # Filter out unwanted labels
                artist = text
                break

        if title and artist:
            chart_data.append({
                "rank": len(chart_data) + 1,
                "title": title,
                "artist": artist
            })

    return chart_data

def main():
    parser = argparse.ArgumentParser(description="Scrape Billboard Hot 100 chart data")
    parser.add_argument("--scrape", type=int, help="Number of top entries to scrape")
    parser.add_argument("--save", type=str, help="Path to save scraped dataset as CSV")
    parser.add_argument("--date", type=str, help="Chart date in YYYY-MM-DD format (optional; defaults to latest)")

    args = parser.parse_args()

    data = fetch_chart(args.date)

    df = pd.DataFrame(data)

    if df.empty:
        print("No data to display or save. Exiting.")
        return

    if args.scrape:
        df = df.head(args.scrape)

    if args.save:
        df.to_csv(args.save, index=False)
        print(f"💾 Saved data to {args.save}")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()