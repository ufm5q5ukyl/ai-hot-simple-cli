import argparse
import xml.etree.ElementTree as ET
import urllib.request
from datetime import datetime

def fetch_headlines(rss_url, limit=5):
    """Fetch recent headlines from an RSS feed."""
    try:
        with urllib.request.urlopen(rss_url, timeout=10) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        items = root.findall('.//item')[:limit]
        return [item.findtext('title', '').strip() for item in items if item.findtext('title')]
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def summarize_with_llm(headlines, provider='mock'):
    """Summarize headlines using LLM (mock returns simple concatenation)."""
    if provider == 'mock':
        return "Today's hot topics: " + "; ".join(headlines)
    # In real implementation, call OpenAI/Claude API here
    return "LLM summary placeholder"

def main():
    parser = argparse.ArgumentParser(description='Generate daily AI hot list from RSS')
    parser.add_argument('--rss', default='https://hnrss.org/frontpage', help='RSS feed URL')
    parser.add_argument('--limit', type=int, default=5, help='Number of headlines to fetch')
    parser.add_argument('--provider', default='mock', choices=['mock', 'openai'], help='LLM provider')
    args = parser.parse_args()

    headlines = fetch_headlines(args.rss, args.limit)
    if headlines:
        digest = summarize_with_llm(headlines, args.provider)
        print(f"\n=== AI Hot Daily Digest ({datetime.now().date()}) ===\n")
        print(digest)
    else:
        print("No headlines fetched. Check RSS URL or network.")

if __name__ == "__main__":
    main()
