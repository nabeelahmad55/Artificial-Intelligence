import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://quotes.toscrape.com"


def get_page_quotes(url):
    """Scrape all quotes from a single page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    for quote in soup.find_all("div", class_="quote"):
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        quotes.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags)
        })
    return quotes


def scrape_all_quotes():
    """Scrape all pages of the website."""
    page = 1
    all_quotes = []
    while True:
        url = f"{BASE_URL}/page/{page}/"
        print(f"Scraping page {page}...")
        quotes = get_page_quotes(url)
        if not quotes:
            break
        all_quotes.extend(quotes)
        page += 1
    return all_quotes


def save_to_csv(quotes, filename="quotes.csv"):
    """Save scraped quotes to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(quotes)
    print(f"\n✅ Saved {len(quotes)} quotes to {filename}")


def main():
    quotes = scrape_all_quotes()
    save_to_csv(quotes)


if __name__ == "__main__":
    main()
