import feedparser
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

def combine_rss_feeds(feed_urls, output_filename="combined_feed.xml"):
    combined_root = Element("rss", version="2.0")
    channel = SubElement(combined_root, "channel")
    
    SubElement(channel, "title").text = "My Combined RSS Feed"
    SubElement(channel, "link").text = "https://github.com/inga7eleven/rss-aggregator"
    SubElement(channel, "description").text = "An aggregated feed from multiple sources"
    SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    all_entries = []
    
    for url in feed_urls:
        try:
            print(f"Fetching {url}...")
            feed = feedparser.parse(url)
            all_entries.extend(feed.entries)
            print(f"Added {len(feed.entries)} entries from {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    # Sort entries by publication date
    all_entries.sort(
        key=lambda x: x.published_parsed if hasattr(x, 'published_parsed') and x.published_parsed else (0,0,0,0,0,0,0,0,0), 
        reverse=True
    )
    
    for entry in all_entries:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = entry.title if hasattr(entry, 'title') else "No Title"
        SubElement(item, "link").text = entry.link if hasattr(entry, 'link') else ""
        SubElement(item, "description").text = entry.summary if hasattr(entry, 'summary') else ""
        
        if hasattr(entry, 'published'):
            SubElement(item, "pubDate").text = entry.published
    
    with open(output_filename, "wb") as f:
        f.write(tostring(combined_root, encoding="utf-8", xml_declaration=True))
    
    print(f"Combined feed created: {output_filename} with {len(all_entries)} total entries")

if __name__ == "__main__":
    # Replace these with your actual RSS feeds
    feed_urls_to_combine = [
        "https://rss.app/feeds/GTI6rk8f1Qs3z8pe.xml",  # CSP Daily News
        "https://rss.app/feeds/v1.1/VuTSl52lAn3dm65S.json",  # Retail Dive
        "https://rss.app/feeds/v1.1/6wjwjlayBPlzMD3h.json",  # Convenience Store News
        "https://rss.app/feeds/v1.1/IoeJ4fVQlMKJfsPM.json",  # C-Store Decisions
        "https://rss.app/feeds/v1.1/VIf6dPsZ8Kbo58JY.json",  # Business Insider
        "https://rss.app/feeds/v1.1/wTT1hpGeR4MbXeLg.json",  # Modern Retail
        "https://rss.app/feeds/v1.1/SZSDocrCsqJYbPUl.json",  # Retail Touchpoints
    ]
    
    combine_rss_feeds(feed_urls_to_combine)
