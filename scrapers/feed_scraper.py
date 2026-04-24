import sys, os, re, hashlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.database import SessionLocal, init_db
from app.models import Attack

FEEDS = [
    {"name": "CERT-NP", "url": "https://www.cert.gov.np/feed", "country": "Nepal"},
    {"name": "CERT-In", "url": "https://www.cert-in.org.in/RSS/Advisories.xml", "country": "India"},
    {"name": "Kathmandu Post Tech", "url": "https://kathmandupost.com/tech/feed", "country": "Nepal"},
    {"name": "Economic Times Cyber", "url": "https://economictimes.indiatimes.com/news/cybersecurity/rssfeeds/99842241.cms", "country": "India"},
]

ATTACK_KEYWORDS = ["phishing","malware","ransomware","hacked","cyber attack","data breach","scam","fraud","trojan","ddos","spyware","vulnerability","exploit","botnet"]

KEYWORD_TYPE_MAP = {"phishing":"phishing","ransomware":"ransomware","malware":"malware","trojan":"malware","ddos":"ddos","data breach":"data_breach","scam":"scam","fraud":"scam"}

SECTOR_KEYWORD_MAP = {"bank":"banking","finance":"banking","hospital":"healthcare","health":"healthcare","government":"government","ministry":"government","university":"education","school":"education","telecom":"telecom"}

def is_attack_related(text):
    return any(kw in text.lower() for kw in ATTACK_KEYWORDS)

def detect_attack_type(text):
    text_lower = text.lower()
    for kw, atype in KEYWORD_TYPE_MAP.items():
        if kw in text_lower:
            return atype
    return "other"

def detect_sector(text):
    text_lower = text.lower()
    for kw, sector in SECTOR_KEYWORD_MAP.items():
        if kw in text_lower:
            return sector
    return "other"

def dedupe_hash(title, url):
    return hashlib.md5(f"{title.lower().strip()}{url}".encode()).hexdigest()

def parse_date(entry):
    for attr in ["published_parsed","updated_parsed"]:
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6])
            except:
                pass
    return datetime.utcnow()

def scrape_feed(feed_config, db):
    name = feed_config["name"]
    url = feed_config["url"]
    country = feed_config["country"]
    print(f"Scraping: {name}")
    try:
        parsed = feedparser.parse(url)
    except Exception as e:
        print(f"Failed: {e}")
        return 0
    new_count = 0
    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        description = entry.get("summary", "").strip()
        source_url = entry.get("link", "")
        description = BeautifulSoup(description, "html.parser").get_text(separator=" ").strip()
        full_text = f"{title} {description}"
        if not is_attack_related(full_text):
            continue
        fingerprint = dedupe_hash(title, source_url)
        existing = db.query(Attack).filter(Attack.campaign_name == fingerprint).first()
        if existing:
            continue
        attack = Attack(
            title=title[:255],
            description=description[:2000],
            attack_type=detect_attack_type(full_text),
            attack_vector="unknown",
            severity="medium",
            country=country,
            target_sector=detect_sector(full_text),
            source_name=name,
            source_url=source_url[:500],
            status="pending",
            verified="no",
            incident_date=parse_date(entry),
            reported_date=datetime.utcnow(),
            campaign_name=fingerprint,
        )
        db.add(attack)
        new_count += 1
        print(f"  Added: {title[:60]}...")
    db.commit()
    return new_count

def run_all():
    init_db()
    db = SessionLocal()
    total_new = 0
    print(f"SACAD Scraper started at {datetime.utcnow().isoformat()}")
    for feed in FEEDS:
        try:
            count = scrape_feed(feed, db)
            total_new += count
        except Exception as e:
            print(f"Error on {feed['name']}: {e}")
    db.close()
    print(f"Done. Total new records: {total_new}")

if __name__ == "__main__":
    run_all()