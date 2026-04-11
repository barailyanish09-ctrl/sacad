import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal, init_db
from app.models import Attack
from datetime import datetime

init_db()
db = SessionLocal()

SEED_ATTACKS = [
    {
        "title": "Nepal Telecom Customer Data Phishing Campaign",
        "description": "Mass phishing SMS campaign impersonating Nepal Telecom, luring users to fake login pages to harvest credentials.",
        "attack_type": "phishing",
        "attack_vector": "sms",
        "severity": "high",
        "country": "Nepal",
        "region": "Nationwide",
        "target_sector": "telecom",
        "source_name": "CERT-NP",
        "verified": "yes",
        "incident_date": datetime(2023, 8, 14),
        "reported_date": datetime(2023, 8, 20),
    },
    {
        "title": "Indian Banking Trojan — Drinik Malware",
        "description": "Android banking trojan targeting 18 Indian banks including SBI, ICICI, and HDFC.",
        "attack_type": "malware",
        "attack_vector": "web",
        "severity": "critical",
        "country": "India",
        "region": "Multiple states",
        "target_sector": "banking",
        "malware_family": "Drinik",
        "source_name": "CERT-In",
        "verified": "yes",
        "incident_date": datetime(2022, 9, 1),
        "reported_date": datetime(2022, 9, 15),
    },
    {
        "title": "Bangladesh Bank SWIFT Heist",
        "description": "Attackers compromised Bangladesh Bank SWIFT terminal. $81M successfully stolen.",
        "attack_type": "data_breach",
        "attack_vector": "unknown",
        "severity": "critical",
        "country": "Bangladesh",
        "target_sector": "banking",
        "target_org": "Bangladesh Bank",
        "threat_actor": "Lazarus Group",
        "source_name": "Reuters",
        "verified": "yes",
        "incident_date": datetime(2016, 2, 4),
        "reported_date": datetime(2016, 3, 10),
    },
    {
        "title": "AIIMS Delhi Ransomware Attack",
        "description": "Ransomware paralysed AIIMS Delhi for 15+ days. 1.3 crore patient records at risk.",
        "attack_type": "ransomware",
        "attack_vector": "unknown",
        "severity": "critical",
        "country": "India",
        "region": "New Delhi",
        "target_sector": "healthcare",
        "target_org": "AIIMS Delhi",
        "source_name": "CERT-In",
        "verified": "yes",
        "incident_date": datetime(2022, 11, 23),
        "reported_date": datetime(2022, 11, 25),
    },
    {
        "title": "Nepal Government Portal Defacement",
        "description": "Coordinated defacement of several Nepal government subdomains with political messaging.",
        "attack_type": "other",
        "attack_vector": "web",
        "severity": "medium",
        "country": "Nepal",
        "region": "Kathmandu",
        "target_sector": "government",
        "source_name": "CERT-NP",
        "verified": "partial",
        "incident_date": datetime(2023, 3, 12),
        "reported_date": datetime(2023, 3, 14),
    },
    {
        "title": "CoWIN Vaccine Data Leak — India",
        "description": "Telegram bot exposed personal data of millions of Indians including Aadhaar numbers.",
        "attack_type": "data_breach",
        "attack_vector": "web",
        "severity": "high",
        "country": "India",
        "target_sector": "healthcare",
        "target_org": "CoWIN / Ministry of Health",
        "source_name": "CERT-In",
        "verified": "yes",
        "incident_date": datetime(2023, 6, 12),
        "reported_date": datetime(2023, 6, 12),
    },
]

def seed():
    existing = db.query(Attack).count()
    if existing > 0:
        print(f"Database already has {existing} records. Skipping seed.")
        return
    for data in SEED_ATTACKS:
        attack = Attack(**data)
        db.add(attack)
    db.commit()
    print(f"✅ Seeded {len(SEED_ATTACKS)} attack records successfully.")

if __name__ == "__main__":
    seed()
    db.close()