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
        "description": "Mass phishing SMS campaign impersonating Nepal Telecom (NTC). Victims received messages claiming their SIM would be deactivated, redirecting to hxxp://ntc-verify[.]com/login — a credential harvesting page mimicking NTC's portal. Over 2,000 reported victims in Kathmandu Valley alone.",
        "attack_type": "phishing",
        "attack_vector": "sms",
        "severity": "high",
        "country": "Nepal",
        "region": "Kathmandu Valley",
        "target_sector": "telecom",
        "target_org": "Nepal Telecom customers",
        "ioc_urls": "hxxp://ntc-verify[.]com/login,hxxp://ntc-account[.]info/verify",
        "ioc_ips": "185.220.101[.]45,194.165.16[.]78",
        "source_name": "CERT-NP",
        "source_url": "https://www.cert.gov.np",
        "status": "verified",
        "verified_by": "CERT-NP",
        "confidence_score": 0.95,
        "verified": "yes",
        "incident_date": datetime(2023, 8, 14),
        "reported_date": datetime(2023, 8, 20),
    },
    {
        "title": "Drinik Android Banking Trojan — Indian Banks",
        "description": "Drinik v3 Android trojan distributed via fake IT Department APK (IncomeTaxIndia_v2.3.apk). Targeted customers of SBI, ICICI, HDFC, Axis, and 14 other Indian banks. Malware used accessibility services to overlay fake login screens and exfiltrate credentials to C2 at 91.219.213[.]44. Over 50,000 devices estimated infected.",
        "attack_type": "malware",
        "attack_vector": "web",
        "severity": "critical",
        "country": "India",
        "region": "Pan-India",
        "target_sector": "banking",
        "target_org": "SBI, ICICI, HDFC, Axis Bank customers",
        "ioc_ips": "91.219.213[.]44,185.234.219[.]128",
        "ioc_hashes": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4,f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3",
        "malware_family": "Drinik",
        "source_name": "CERT-In",
        "source_url": "https://www.cert-in.org.in",
        "status": "verified",
        "verified_by": "CERT-In",
        "confidence_score": 0.97,
        "verified": "yes",
        "incident_date": datetime(2022, 9, 1),
        "reported_date": datetime(2022, 9, 15),
    },
    {
        "title": "Bangladesh Bank SWIFT Heist",
        "description": "Lazarus Group compromised Bangladesh Bank's SWIFT terminal via spear-phishing. Fraudulent transfer requests totalling $951M sent to Federal Reserve New York. $81M successfully laundered through Philippine casino accounts. Attack exploited weak network segmentation between SWIFT terminal and internal systems.",
        "attack_type": "data_breach",
        "attack_vector": "email",
        "severity": "critical",
        "country": "Bangladesh",
        "region": "Dhaka",
        "target_sector": "banking",
        "target_org": "Bangladesh Bank",
        "threat_actor": "Lazarus Group",
        "campaign_name": "Bangladesh Bank Heist",
        "source_name": "Reuters / SWIFT Advisory",
        "source_url": "https://www.reuters.com/article/us-cyber-heist-bangladesh",
        "status": "verified",
        "verified_by": "SWIFT, FBI",
        "verification_notes": "Attributed to Lazarus Group by multiple intelligence agencies including BAE Systems and Symantec.",
        "confidence_score": 0.99,
        "verified": "yes",
        "incident_date": datetime(2016, 2, 4),
        "reported_date": datetime(2016, 3, 10),
    },
    {
        "title": "AIIMS Delhi Ransomware Attack",
        "description": "Ransomware attack paralysed All India Institute of Medical Sciences Delhi for 15+ days. Five servers compromised, approximately 1.3 crore patient records encrypted. Hospital reverted to manual operations for appointments, billing, and lab reports. Attackers demanded cryptocurrency ransom. NIC and CERT-In deployed response teams.",
        "attack_type": "ransomware",
        "attack_vector": "unknown",
        "severity": "critical",
        "country": "India",
        "region": "New Delhi",
        "target_sector": "healthcare",
        "target_org": "AIIMS New Delhi",
        "source_name": "CERT-In / Indian Express",
        "source_url": "https://indianexpress.com/article/india/aiims-cyber-attack",
        "status": "verified",
        "verified_by": "CERT-In",
        "confidence_score": 0.98,
        "verified": "yes",
        "incident_date": datetime(2022, 11, 23),
        "reported_date": datetime(2022, 11, 25),
    },
    {
        "title": "Nepal Government Portal Defacement Campaign",
        "description": "Coordinated defacement of 12+ Nepal government subdomains including moha.gov.np and dofe.gov.np. Attackers replaced homepages with political messaging and claimed affiliation with hacktivist group. NIC Asia ATM network also disrupted around the same period. Vulnerabilities exploited: outdated CMS and unpatched Apache servers.",
        "attack_type": "defacement",
        "attack_vector": "web",
        "severity": "medium",
        "country": "Nepal",
        "region": "Kathmandu",
        "target_sector": "government",
        "target_org": "Nepal Government (moha.gov.np, dofe.gov.np)",
        "source_name": "CERT-NP / Khabarhub",
        "status": "verified",
        "verified_by": "CERT-NP",
        "confidence_score": 0.88,
        "verified": "partial",
        "incident_date": datetime(2023, 3, 12),
        "reported_date": datetime(2023, 3, 14),
    },
    {
        "title": "CoWIN Vaccine Registration Data Leak",
        "description": "Telegram bot exposed personal data of millions of Indians registered on India's CoWIN vaccination portal. Data included full names, Aadhaar numbers, phone numbers, date of birth, and vaccination centre details. Government initially denied breach. Later confirmed partial exposure via third-party access.",
        "attack_type": "data_breach",
        "attack_vector": "web",
        "severity": "high",
        "country": "India",
        "region": "Pan-India",
        "target_sector": "healthcare",
        "target_org": "CoWIN / Ministry of Health and Family Welfare",
        "source_name": "CERT-In / The Hindu",
        "source_url": "https://www.thehindu.com/sci-tech/technology/cowin-data-leak",
        "status": "verified",
        "verified_by": "CERT-In",
        "confidence_score": 0.91,
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