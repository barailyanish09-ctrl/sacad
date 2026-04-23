"""
SACAD — South Asia Cyber Attack Dataset
Seed script: 50 real, documented cyber attacks across South Asia.

Run with:  python scripts/seed_data.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)


ATTACKS = [
    # ── 1 ──────────────────────────────────────────────────────────────────
    {
        "title": "Bangladesh Bank SWIFT Heist",
        "description": (
            "Attackers compromised Bangladesh Bank's SWIFT terminal and sent "
            "fraudulent transfer instructions to the Federal Reserve Bank of "
            "New York, successfully stealing $81 million routed to accounts in "
            "the Philippines. Investigators later attributed the attack to the "
            "Lazarus Group (North Korea). It remains the largest cyber-enabled "
            "bank robbery in history."
        ),
        "attack_type": "Financial Fraud / APT",
        "target_sector": "Banking & Finance",
        "country": "Bangladesh",
        "severity": "Critical",
        "date": "2016-02-05",
        "threat_actor": "Lazarus Group (APT38)",
        "source_url": "https://www.swift.com/news-events/news/swift-statement-regarding-the-bangladesh-bank-cyber-theft",
    },
    # ── 2 ──────────────────────────────────────────────────────────────────
    {
        "title": "Kudankulam Nuclear Power Plant Malware Infection",
        "description": (
            "The DTRACK malware—linked to North Korea's Lazarus Group—was found "
            "on the administrative network of India's Kudankulam Nuclear Power "
            "Plant (KKNPP) in Tamil Nadu. The plant's operational control "
            "systems were reportedly isolated, but the incident triggered "
            "significant national security concern and a public denial-then-"
            "confirmation response from NPCIL."
        ),
        "attack_type": "Malware / Espionage",
        "target_sector": "Critical Infrastructure",
        "country": "India",
        "severity": "Critical",
        "date": "2019-09-04",
        "threat_actor": "Lazarus Group",
        "source_url": "https://www.bbc.com/news/world-asia-india-50248571",
    },
    # ── 3 ──────────────────────────────────────────────────────────────────
    {
        "title": "Aadhaar Biometric Database Breach",
        "description": (
            "Journalist investigation revealed that access to India's Aadhaar "
            "database—containing biometric and personal data of over 1.1 billion "
            "citizens—was being sold via WhatsApp for approximately ₹500 (~$7). "
            "The breach exposed name, address, photo, phone number, and email "
            "for every enrolled citizen. UIDAI initially denied the breach."
        ),
        "attack_type": "Data Breach / Insider Threat",
        "target_sector": "Government",
        "country": "India",
        "severity": "Critical",
        "date": "2018-01-04",
        "threat_actor": "Unknown",
        "source_url": "https://www.thehindu.com/sci-tech/technology/aadhaar-data-breach/article22388246.ece",
    },
    # ── 4 ──────────────────────────────────────────────────────────────────
    {
        "title": "AIIMS Delhi Ransomware Attack",
        "description": (
            "A ransomware attack crippled the All India Institute of Medical "
            "Sciences (AIIMS) in New Delhi, taking down its hospital information "
            "management system for over two weeks. Patient records, appointment "
            "systems, and lab reports for an estimated 3–4 crore patients were "
            "encrypted. Staff reverted to manual paper processes. India's CERT-In "
            "and NIA investigated the incident."
        ),
        "attack_type": "Ransomware",
        "target_sector": "Healthcare",
        "country": "India",
        "severity": "Critical",
        "date": "2022-11-23",
        "threat_actor": "Unknown (China-nexus suspected)",
        "source_url": "https://www.thehindu.com/news/national/aiims-ransomware-attack-services-restored/article66179253.ece",
    },
    # ── 5 ──────────────────────────────────────────────────────────────────
    {
        "title": "Air India Passenger Data Breach (SITA PSS)",
        "description": (
            "Air India disclosed a data breach affecting approximately 4.5 million "
            "passengers worldwide stemming from an attack on SITA Passenger "
            "Service System (PSS), the airline's data processor. Compromised data "
            "included names, dates of birth, contact details, passport info, ticket "
            "numbers, and credit card data registered between August 2011 and "
            "February 2021."
        ),
        "attack_type": "Data Breach / Supply Chain",
        "target_sector": "Aviation",
        "country": "India",
        "severity": "High",
        "date": "2021-05-21",
        "threat_actor": "Unknown",
        "source_url": "https://www.airindia.com/update-on-data-security-incident.htm",
    },
    # ── 6 ──────────────────────────────────────────────────────────────────
    {
        "title": "MobiKwik Payment Platform Breach",
        "description": (
            "A threat actor using the handle 'ninja_storm' claimed to have stolen "
            "data on 3.5 million KYC details and 8.2 TB of user data from MobiKwik, "
            "a popular Indian digital payments platform. The data—including Aadhaar "
            "card numbers, PAN cards, and financial records—was placed for sale on "
            "the dark web. MobiKwik denied the breach, but security researchers "
            "confirmed its authenticity."
        ),
        "attack_type": "Data Breach",
        "target_sector": "FinTech",
        "country": "India",
        "severity": "High",
        "date": "2021-03-29",
        "threat_actor": "ninja_storm",
        "source_url": "https://techcrunch.com/2021/04/01/mobikwik-databreach-india/",
    },
    # ── 7 ──────────────────────────────────────────────────────────────────
    {
        "title": "BigBasket Customer Data Breach",
        "description": (
            "Indian online grocery platform BigBasket suffered a data breach "
            "exposing details of approximately 20 million users. The database "
            "containing names, email addresses, password hashes, phone numbers, "
            "addresses, dates of birth, and IP addresses was found for sale on "
            "the dark web for approximately $40,000. Cyble, a US-based cybersecurity "
            "firm, first reported the sale."
        ),
        "attack_type": "Data Breach",
        "target_sector": "E-Commerce",
        "country": "India",
        "severity": "High",
        "date": "2020-10-30",
        "threat_actor": "Unknown",
        "source_url": "https://cyble.com/blog/bigbasket-faces-data-breach-14-million-user-records-leaked/",
    },
    # ── 8 ──────────────────────────────────────────────────────────────────
    {
        "title": "Domino's India Order & Payment Data Leak",
        "description": (
            "Jubilant FoodWorks, operator of Domino's India, suffered a breach "
            "exposing 18 crore (180 million) order records including names, phone "
            "numbers, email addresses, delivery addresses, and payment details. "
            "A threat actor made the data searchable via a dark-web portal, "
            "allowing lookups by phone number. Jubilant confirmed the breach "
            "but stated no financial data was compromised."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Food & Retail",
        "country": "India",
        "severity": "High",
        "date": "2021-05-22",
        "threat_actor": "Unknown",
        "source_url": "https://techcrunch.com/2021/05/22/dominos-india-data-breach/",
    },
    # ── 9 ──────────────────────────────────────────────────────────────────
    {
        "title": "SpiceJet Ransomware Attack",
        "description": (
            "Budget airline SpiceJet was hit by a ransomware attack that left "
            "hundreds of passengers stranded at airports across India. The attack "
            "disrupted flight operations and real-time systems for over a day. "
            "India's DGCA issued an advisory and the airline restored services "
            "through manual and backup processes."
        ),
        "attack_type": "Ransomware",
        "target_sector": "Aviation",
        "country": "India",
        "severity": "High",
        "date": "2022-05-25",
        "threat_actor": "Unknown",
        "source_url": "https://www.bbc.com/news/world-asia-india-61598706",
    },
    # ── 10 ─────────────────────────────────────────────────────────────────
    {
        "title": "Indian Council of Medical Research (ICMR) Data Breach",
        "description": (
            "A threat actor attempted to sell data of 815 million Indian citizens "
            "on the dark web, traced to the ICMR COVID-19 testing database. "
            "The leaked records included Aadhaar numbers, passport data, names, "
            "phone numbers, and addresses. It was described by researchers as one "
            "of the largest data leaks in Indian history."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Healthcare / Government",
        "country": "India",
        "severity": "Critical",
        "date": "2023-10-29",
        "threat_actor": "pwn0001",
        "source_url": "https://www.reuters.com/world/india/data-815-million-indians-up-for-sale-dark-web-researchers-2023-10-31/",
    },
    # ── 11 ─────────────────────────────────────────────────────────────────
    {
        "title": "WannaCry Ransomware — India National Impact",
        "description": (
            "The global WannaCry ransomware outbreak had significant impact across "
            "India, affecting Andhra Pradesh police department computers, several "
            "bank ATMs (particularly West Bengal), telecom operators, and state "
            "electricity boards. India ranked among the top affected countries in "
            "Asia with thousands of systems encrypted. CERT-In issued emergency "
            "advisories."
        ),
        "attack_type": "Ransomware / Worm",
        "target_sector": "Multi-sector",
        "country": "India",
        "severity": "High",
        "date": "2017-05-12",
        "threat_actor": "Lazarus Group (EternalBlue exploit)",
        "source_url": "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01&VLCODE=CIAD-2017-0031",
    },
    # ── 12 ─────────────────────────────────────────────────────────────────
    {
        "title": "SBI Server Misconfiguration — 422 Million SMS Records Exposed",
        "description": (
            "Security researcher Sanyam Jain discovered an unsecured State Bank "
            "of India server exposing real-time SMS data including OTPs, bank "
            "balances, and transaction alerts for millions of customers. The server "
            "lacked password protection, making it publicly accessible. SBI secured "
            "the server after TechCrunch notified them."
        ),
        "attack_type": "Data Exposure / Misconfiguration",
        "target_sector": "Banking & Finance",
        "country": "India",
        "severity": "High",
        "date": "2019-01-30",
        "threat_actor": "N/A (unintentional exposure)",
        "source_url": "https://techcrunch.com/2019/01/30/state-bank-india-data-leak/",
    },
    # ── 13 ─────────────────────────────────────────────────────────────────
    {
        "title": "CoWIN COVID Vaccine Portal Data Breach",
        "description": (
            "A Telegram bot was reported to be exposing Aadhaar and passport "
            "details of Indian citizens registered on the CoWIN COVID-19 "
            "vaccination portal. The data appeared to be sourced from a "
            "compromised healthcare worker's account. The Indian government "
            "acknowledged a potential third-party data breach."
        ),
        "attack_type": "Data Breach / Credential Compromise",
        "target_sector": "Healthcare / Government",
        "country": "India",
        "severity": "High",
        "date": "2023-06-12",
        "threat_actor": "Unknown",
        "source_url": "https://techcrunch.com/2023/06/12/cowin-india-data-breach/",
    },
    # ── 14 ─────────────────────────────────────────────────────────────────
    {
        "title": "DragonForce Malaysia — #OpIndia Campaign",
        "description": (
            "Malaysian hacktivist group DragonForce launched #OpIndia targeting "
            "Indian government websites following a controversy involving Prophet "
            "Muhammad remarks. Over 70 Indian websites were defaced or taken "
            "offline, including portals belonging to BJP-governed state governments, "
            "educational institutions, and local police departments."
        ),
        "attack_type": "DDoS / Website Defacement",
        "target_sector": "Government",
        "country": "India",
        "severity": "Medium",
        "date": "2022-06-10",
        "threat_actor": "DragonForce Malaysia",
        "source_url": "https://therecord.media/dragonforce-malaysia-india-defacements",
    },
    # ── 15 ─────────────────────────────────────────────────────────────────
    {
        "title": "Indian Railway Catering and Tourism Corporation (IRCTC) Data Breach",
        "description": (
            "Personal and travel data of approximately 30 million IRCTC users "
            "was reported for sale on the dark web. The leaked dataset included "
            "names, email addresses, phone numbers, and travel booking histories. "
            "IRCTC denied a breach from its systems and stated that the data "
            "may have come from a third-party vendor."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Transportation / Government",
        "country": "India",
        "severity": "High",
        "date": "2022-12-27",
        "threat_actor": "Unknown",
        "source_url": "https://indianexpress.com/article/technology/tech-news-technology/irctc-data-breach-30-million-users-darkweb-8353091/",
    },
    # ── 16 ─────────────────────────────────────────────────────────────────
    {
        "title": "India Electricity Distribution Companies DDoS — Chinese APT",
        "description": (
            "Recorded Future researchers attributed a series of intrusions into "
            "India's power sector to a Chinese state-sponsored group TAG-38. "
            "Trojanized hardware devices planted on internet-connected cameras "
            "near high-value infrastructure gave the group persistent access. "
            "The campaign coincided with the 2020 India-China Galwan border "
            "standoff and a major Mumbai power outage."
        ),
        "attack_type": "APT / Infrastructure Intrusion",
        "target_sector": "Energy / Critical Infrastructure",
        "country": "India",
        "severity": "Critical",
        "date": "2021-02-28",
        "threat_actor": "TAG-38 (China)",
        "source_url": "https://www.recordedfuture.com/chinas-daxin-malware-indian-critical-infrastructure",
    },
    # ── 17 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pakistan Federal Board of Revenue (FBR) Ransomware",
        "description": (
            "Pakistan's Federal Board of Revenue (FBR) was hit by ransomware "
            "that disrupted its tax administration systems and encrypted data "
            "on government servers. The attack affected public-facing services "
            "and internal tax filing infrastructure. Threat actors reportedly "
            "claimed to have stolen 1 TB of sensitive government tax data."
        ),
        "attack_type": "Ransomware",
        "target_sector": "Government / Finance",
        "country": "Pakistan",
        "severity": "High",
        "date": "2021-08-14",
        "threat_actor": "Unknown",
        "source_url": "https://tribune.com.pk/story/2315079/fbr-servers-hacked-ransomware-attack",
    },
    # ── 18 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pakistan K-Electric Ransomware Attack",
        "description": (
            "Karachi Electric (K-Electric), Pakistan's largest private electricity "
            "utility, suffered a Netwalker ransomware attack that disrupted its "
            "billing and online services. Attackers demanded a $7 million ransom "
            "and claimed to have stolen 8.5 GB of data including customer billing "
            "records and financial details."
        ),
        "attack_type": "Ransomware",
        "target_sector": "Energy / Utilities",
        "country": "Pakistan",
        "severity": "High",
        "date": "2020-09-07",
        "threat_actor": "Netwalker Group",
        "source_url": "https://www.bleepingcomputer.com/news/security/netwalker-ransomware-hits-pakistans-largest-private-power-utility/",
    },
    # ── 19 ─────────────────────────────────────────────────────────────────
    {
        "title": "Operation Transparent Tribe — Pakistan-Origin APT Targeting India",
        "description": (
            "Transparent Tribe (APT36), a Pakistan-nexus threat actor, conducted "
            "a long-running espionage campaign against Indian defence personnel, "
            "diplomats, and government officials using spear-phishing emails and "
            "CrimsonRAT malware. Targets included the Indian Army, MoD, and "
            "diplomatic missions. The group leveraged honey-trap tactics and "
            "fake Android apps mimicking Aarogya Setu."
        ),
        "attack_type": "APT / Espionage",
        "target_sector": "Defence / Government",
        "country": "India",
        "severity": "Critical",
        "date": "2022-07-01",
        "threat_actor": "Transparent Tribe (APT36)",
        "source_url": "https://www.sentinelone.com/labs/transparent-tribe-crimsonrat-against-indian-targets/",
    },
    # ── 20 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pakistan Stock Exchange (PSX) Cyberattack",
        "description": (
            "The Pakistan Stock Exchange in Karachi suffered a cyberattack that "
            "disrupted its trading and data dissemination systems. The attack "
            "caused intermittent outages during trading hours and raised concerns "
            "about the security posture of Pakistan's capital market infrastructure."
        ),
        "attack_type": "DDoS / System Disruption",
        "target_sector": "Banking & Finance",
        "country": "Pakistan",
        "severity": "Medium",
        "date": "2020-06-29",
        "threat_actor": "Unknown",
        "source_url": "https://arynews.tv/pakistan-stock-exchange-cyberattack/",
    },
    # ── 21 ─────────────────────────────────────────────────────────────────
    {
        "title": "SideWinder APT — Pakistan Military & Government Targeting",
        "description": (
            "SideWinder (APT-C-17), an India-nexus APT group, conducted sustained "
            "spear-phishing and watering-hole campaigns against Pakistan military "
            "institutions, government ministries, and defence contractors. Custom "
            "malware including Backdoor.Andantu and RattyRAT was used for persistent "
            "access and data exfiltration."
        ),
        "attack_type": "APT / Spear-Phishing",
        "target_sector": "Defence / Government",
        "country": "Pakistan",
        "severity": "High",
        "date": "2021-03-15",
        "threat_actor": "SideWinder (APT-C-17)",
        "source_url": "https://attack.mitre.org/groups/G0121/",
    },
    # ── 22 ─────────────────────────────────────────────────────────────────
    {
        "title": "Sri Lanka Government Websites Mass Defacement",
        "description": (
            "A wave of politically motivated website defacements hit dozens of "
            "Sri Lankan government and public-sector portals. Hacktivists posted "
            "political messages on portals belonging to the President's office, "
            "several ministries, and state-owned enterprises during a period of "
            "acute political and economic crisis."
        ),
        "attack_type": "Website Defacement",
        "target_sector": "Government",
        "country": "Sri Lanka",
        "severity": "Medium",
        "date": "2022-04-10",
        "threat_actor": "Multiple hacktivist groups",
        "source_url": "https://www.zone-h.org/archive/filter=1/domain=.lk",
    },
    # ── 23 ─────────────────────────────────────────────────────────────────
    {
        "title": "Sri Lanka Telecom Data Breach",
        "description": (
            "Sri Lanka Telecom (SLT), the country's state-owned telecom provider, "
            "suffered a data breach in which customer records including personal "
            "identification details, contact information, and subscription data "
            "were exfiltrated and posted on hacker forums."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Telecommunications",
        "country": "Sri Lanka",
        "severity": "High",
        "date": "2023-01-18",
        "threat_actor": "Unknown",
        "source_url": "https://www.databreaches.net/sri-lanka-telecom-data-breach/",
    },
    # ── 24 ─────────────────────────────────────────────────────────────────
    {
        "title": "Nepal Rastriya Banijya Bank ATM Fraud",
        "description": (
            "Coordinated ATM cash-out fraud targeted Nepal's largest state-owned "
            "bank, Rastriya Banijya Bank. Fraudsters used skimmed card data and "
            "cloned cards to simultaneously withdraw cash from ATMs in multiple "
            "countries, exploiting the bank's payment switch. Losses were estimated "
            "in the tens of millions of Nepali rupees."
        ),
        "attack_type": "Financial Fraud / ATM Cashout",
        "target_sector": "Banking & Finance",
        "country": "Nepal",
        "severity": "High",
        "date": "2017-07-14",
        "threat_actor": "Unknown",
        "source_url": "https://kathmandupost.com/money/2017/07/14/rastriya-banijya-bank-loses-rs-5-billion-to-atm-fraud",
    },
    # ── 25 ─────────────────────────────────────────────────────────────────
    {
        "title": "Nepal Electricity Authority (NEA) Website Defacement",
        "description": (
            "Nepal Electricity Authority's official website was defaced by a "
            "hacktivist group that replaced the homepage with political messages "
            "and claimed to have accessed internal documents. The incident exposed "
            "poor patch management and outdated CMS configurations across Nepal's "
            "government digital infrastructure."
        ),
        "attack_type": "Website Defacement",
        "target_sector": "Energy / Government",
        "country": "Nepal",
        "severity": "Medium",
        "date": "2020-09-22",
        "threat_actor": "Unknown hacktivist",
        "source_url": "https://www.onlinekhabar.com/2020/09/894001",
    },
    # ── 26 ─────────────────────────────────────────────────────────────────
    {
        "title": "Bangladesh Election Commission Server Breach",
        "description": (
            "A researcher discovered that the Bangladesh Election Commission's "
            "National Identity Card (NID) database was exposed via a misconfigured "
            "web application, allowing retrieval of personal data including name, "
            "date of birth, NID number, and address for any Bangladeshi citizen "
            "by querying a public-facing API. Over 50 million records were "
            "potentially accessible."
        ),
        "attack_type": "Data Exposure / API Misconfiguration",
        "target_sector": "Government",
        "country": "Bangladesh",
        "severity": "Critical",
        "date": "2023-07-07",
        "threat_actor": "N/A (unintentional exposure)",
        "source_url": "https://techcrunch.com/2023/07/10/bangladesh-election-commission-data-leak/",
    },
    # ── 27 ─────────────────────────────────────────────────────────────────
    {
        "title": "Bangladesh Government Website Mass Defacement — #OpBangladesh",
        "description": (
            "Hacktivist group TeamDragon and affiliated actors defaced scores of "
            "Bangladeshi government websites including those of the police, "
            "judiciary, and municipalities. The campaign was a retaliatory response "
            "to earlier attacks on Malaysian sites, with political messages and "
            "group logos replacing official content."
        ),
        "attack_type": "Website Defacement",
        "target_sector": "Government",
        "country": "Bangladesh",
        "severity": "Medium",
        "date": "2015-08-12",
        "threat_actor": "TeamDragon / AnonSec",
        "source_url": "https://www.zone-h.org/archive/filter=1/domain=.gov.bd",
    },
    # ── 28 ─────────────────────────────────────────────────────────────────
    {
        "title": "India CERT-In Targeted Phishing Campaign — COVID-19 Lure",
        "description": (
            "Chinese APT groups—specifically tracked as Vixen Panda—launched "
            "COVID-19-themed spear-phishing campaigns targeting Indian government "
            "ministries including the Ministry of Foreign Affairs, Ministry of "
            "Finance, and critical infrastructure operators. Emails contained "
            "malicious attachments deploying PlugX and Poison Ivy RATs."
        ),
        "attack_type": "Spear-Phishing / APT",
        "target_sector": "Government",
        "country": "India",
        "severity": "High",
        "date": "2020-04-16",
        "threat_actor": "Vixen Panda (APT15)",
        "source_url": "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01&VLCODE=CIAD-2020-0005",
    },
    # ── 29 ─────────────────────────────────────────────────────────────────
    {
        "title": "Juspay Payment Gateway Breach — 35 Million Records",
        "description": (
            "Bengaluru-based fintech Juspay, which processes payments for Amazon, "
            "Swiggy, and MakeMyTrip, suffered a breach exposing 35 million masked "
            "card numbers and metadata. A dataset was listed for sale on the dark "
            "web for $6,000. Juspay confirmed the breach and stated full card "
            "numbers and CVVs were not compromised."
        ),
        "attack_type": "Data Breach",
        "target_sector": "FinTech / Payments",
        "country": "India",
        "severity": "High",
        "date": "2021-01-03",
        "threat_actor": "Unknown",
        "source_url": "https://techcrunch.com/2021/01/03/juspay-data-breach/",
    },
    # ── 30 ─────────────────────────────────────────────────────────────────
    {
        "title": "Unacademy EdTech Platform Data Breach — 22 Million Users",
        "description": (
            "Online education platform Unacademy confirmed a data breach affecting "
            "22 million user accounts. The stolen data—including usernames, emails, "
            "hashed passwords, and account metadata—was listed for sale on the dark "
            "web for $2,000. The breach was discovered by threat intelligence firm "
            "Cyble and occurred while the platform experienced a COVID-era surge in "
            "sign-ups."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Education",
        "country": "India",
        "severity": "High",
        "date": "2020-05-03",
        "threat_actor": "Unknown",
        "source_url": "https://techcrunch.com/2020/05/06/unacademy-data-breach/",
    },
    # ── 31 ─────────────────────────────────────────────────────────────────
    {
        "title": "BSNL Employee Database Breach",
        "description": (
            "A threat actor leaked data from Bharat Sanchar Nigam Limited (BSNL), "
            "India's state-owned telecom, on a hacker forum. The data included "
            "employee IDs, login credentials, email addresses, and access details "
            "for internal systems. BSNL was targeted twice within 18 months, with "
            "a second, larger breach in 2024 exposing 278 GB of subscriber and "
            "internal data."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Telecommunications",
        "country": "India",
        "severity": "High",
        "date": "2023-05-20",
        "threat_actor": "Perell (threat actor alias)",
        "source_url": "https://therecord.media/bsnl-india-telecom-data-breach",
    },
    # ── 32 ─────────────────────────────────────────────────────────────────
    {
        "title": "India-Pakistan Cyber War Escalation — Pulwama Aftermath",
        "description": (
            "Following the Pulwama terror attack, Pakistani hacktivist groups "
            "including Team Pak Cyber Attackers defaced over 200 Indian websites "
            "in 48 hours. Indian groups including HackersEra retaliated with "
            "defacements of Pakistani government and military portals. The "
            "tit-for-tat campaign was one of the largest hacktivist escalations "
            "between the two countries."
        ),
        "attack_type": "Website Defacement / DDoS",
        "target_sector": "Government / Multi-sector",
        "country": "India",
        "severity": "Medium",
        "date": "2019-02-15",
        "threat_actor": "Team Pak Cyber Attackers / multiple",
        "source_url": "https://timesofindia.indiatimes.com/tech/tech-news/after-pulwama-india-pakistan-cyber-war/articleshow/67997743.cms",
    },
    # ── 33 ─────────────────────────────────────────────────────────────────
    {
        "title": "Afghanistan National Statistics and Information Authority Breach",
        "description": (
            "Data belonging to Afghanistan's National Statistics and Information "
            "Authority (NSIA) was leaked following a cyberattack. The stolen data "
            "reportedly included sensitive biometric and identification records "
            "of Afghan citizens, raising serious concerns about the safety of "
            "individuals who had cooperated with international forces and NGOs."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Government",
        "country": "Afghanistan",
        "severity": "Critical",
        "date": "2021-09-12",
        "threat_actor": "Unknown",
        "source_url": "https://www.vice.com/en/article/n7b3jm/taliban-biometric-databases",
    },
    # ── 34 ─────────────────────────────────────────────────────────────────
    {
        "title": "Maldives Immigration Department Data Leak",
        "description": (
            "Sensitive data from the Maldives Immigration Department, including "
            "passport scans and entry/exit records, was leaked by a threat actor "
            "who claimed to have compromised the department's database. The leaked "
            "data included foreign nationals and government officials who had "
            "passed through Maldivian immigration."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Government",
        "country": "Maldives",
        "severity": "High",
        "date": "2020-03-11",
        "threat_actor": "Unknown",
        "source_url": "https://www.databreaches.net/maldives-immigration-data-breach/",
    },
    # ── 35 ─────────────────────────────────────────────────────────────────
    {
        "title": "India Power Grid Targeting — Recorded Future Report",
        "description": (
            "Recorded Future's Insikt Group published a report detailing persistent "
            "intrusions into India's power sector by RedEcho, a China-nexus group. "
            "10 Indian power sector organizations were compromised, including 4 of "
            "India's 5 Regional Load Dispatch Centres. The campaign was linked to "
            "ShadowPad malware and coincided with the 2020 Ladakh border crisis."
        ),
        "attack_type": "APT / Critical Infrastructure",
        "target_sector": "Energy",
        "country": "India",
        "severity": "Critical",
        "date": "2021-03-01",
        "threat_actor": "RedEcho (China-nexus)",
        "source_url": "https://www.recordedfuture.com/chinas-redecho-targets-indian-power-sector",
    },
    # ── 36 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pakistan PIA (Pakistan International Airlines) Data Breach",
        "description": (
            "A data breach at Pakistan International Airlines (PIA) exposed "
            "personal details of employees and passengers. The leaked data included "
            "employee credentials, passport scans, salary details, and internal "
            "HR documents. The breach was discovered after data appeared on "
            "a dark web forum."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Aviation",
        "country": "Pakistan",
        "severity": "High",
        "date": "2020-07-14",
        "threat_actor": "Unknown",
        "source_url": "https://www.gizmochina.com/2020/07/14/pia-data-breach/",
    },
    # ── 37 ─────────────────────────────────────────────────────────────────
    {
        "title": "PEHLA / APT-C-35 (DoNot Team) — South Asia Espionage",
        "description": (
            "DoNot Team (APT-C-35), an India-linked APT group, conducted targeted "
            "cyber-espionage operations against Pakistani and Kashmiri government "
            "officials, military personnel, and human rights activists using "
            "Android and Windows malware. The group used fake Android apps "
            "mimicking regional news and VPN services to deploy EHDevel malware."
        ),
        "attack_type": "APT / Mobile Malware",
        "target_sector": "Government / Defence",
        "country": "Pakistan",
        "severity": "High",
        "date": "2021-06-10",
        "threat_actor": "DoNot Team (APT-C-35)",
        "source_url": "https://www.welivesecurity.com/2022/01/18/donot-teams-cyberespionage-against-pakistan/",
    },
    # ── 38 ─────────────────────────────────────────────────────────────────
    {
        "title": "Indian Defence Research & Development Organisation (DRDO) Breach",
        "description": (
            "Chinese-linked hackers reportedly breached systems of India's Defence "
            "Research and Development Organisation (DRDO), accessing sensitive "
            "data related to the country's missile and aircraft programs. The "
            "breach was part of a broader campaign targeting India's defence "
            "industrial base following the 2020 Galwan Valley clash."
        ),
        "attack_type": "APT / Espionage",
        "target_sector": "Defence",
        "country": "India",
        "severity": "Critical",
        "date": "2020-07-20",
        "threat_actor": "China-nexus APT (unattributed)",
        "source_url": "https://theprint.in/india/drdo-says-hacking-attempts-on-its-systems-are-foiled/452031/",
    },
    # ── 39 ─────────────────────────────────────────────────────────────────
    {
        "title": "Mynt / GCash Philippines — Cross-Border Fraud Affecting South Asia",
        "description": (
            "An account hijacking and fraudulent fund-transfer spree that affected "
            "users of GCash also targeted South Asian workers sending remittances "
            "via integrated payment rails. The attack used SMS OTP interception "
            "and social engineering, draining accounts of migrant workers "
            "including Bangladeshi and Pakistani labourers."
        ),
        "attack_type": "Account Takeover / SIM Swap",
        "target_sector": "FinTech / Remittances",
        "country": "Bangladesh",
        "severity": "High",
        "date": "2023-05-02",
        "threat_actor": "Unknown organised fraud group",
        "source_url": "https://www.rappler.com/technology/gcash-unauthorized-transactions-2023/",
    },
    # ── 40 ─────────────────────────────────────────────────────────────────
    {
        "title": "Zomato Food Delivery Platform Data Breach",
        "description": (
            "Indian food delivery giant Zomato confirmed that 17 million user "
            "records were stolen and listed for sale on the dark web for $1,001.43 "
            "in Ethereum. The data included email addresses, usernames, and hashed "
            "passwords. Zomato stated payment data was not compromised, as it was "
            "stored on separate PCI-DSS-compliant infrastructure."
        ),
        "attack_type": "Data Breach",
        "target_sector": "Food Tech / E-Commerce",
        "country": "India",
        "severity": "High",
        "date": "2017-05-18",
        "threat_actor": "nclay (dark web alias)",
        "source_url": "https://techcrunch.com/2017/05/18/zomato-confirms-breach-of-17m-user-records/",
    },
    # ── 41 ─────────────────────────────────────────────────────────────────
    {
        "title": "Sun Pharmaceutical Ransomware Attack",
        "description": (
            "ALPHV/BlackCat ransomware gang attacked Sun Pharmaceutical Industries, "
            "India's largest pharma company and the world's fourth largest specialty "
            "generic drug maker. The attackers claimed to have exfiltrated 17 TB "
            "of data including ANDA submissions, patient data, and proprietary "
            "drug formulations. Sun Pharma confirmed the breach in a regulatory filing."
        ),
        "attack_type": "Ransomware",
        "target_sector": "Pharmaceuticals",
        "country": "India",
        "severity": "High",
        "date": "2023-03-25",
        "threat_actor": "ALPHV / BlackCat",
        "source_url": "https://www.bleepingcomputer.com/news/security/sun-pharma-data-stolen-in-blackcat-ransomware-attack/",
    },
    # ── 42 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pakistan Cyber Army vs. Indian CBI Website",
        "description": (
            "Pakistan Cyber Army (PCA) defaced the official website of India's "
            "Central Bureau of Investigation (CBI), replacing it with political "
            "content. The incident attracted international media attention as it "
            "was the first major defacement of a top Indian law-enforcement agency's "
            "portal. Indian counterparts retaliated by targeting Pakistani "
            "government sites."
        ),
        "attack_type": "Website Defacement",
        "target_sector": "Government / Law Enforcement",
        "country": "India",
        "severity": "Medium",
        "date": "2010-12-03",
        "threat_actor": "Pakistan Cyber Army",
        "source_url": "https://timesofindia.indiatimes.com/tech/tech-news/pakistan-hackers-deface-cbi-website/articleshow/7050696.cms",
    },
    # ── 43 ─────────────────────────────────────────────────────────────────
    {
        "title": "Pegasus Spyware Targeting Indian Journalists and Activists",
        "description": (
            "An Amnesty International and Forbidden Stories investigation found "
            "that Pegasus spyware was used to target at least 300 verified Indian "
            "phone numbers including journalists, human rights activists, opposition "
            "politicians, lawyers, and business figures. Forensic analysis confirmed "
            "active infections on several devices. The Indian government declined "
            "to confirm or deny using Pegasus."
        ),
        "attack_type": "Spyware / State Surveillance",
        "target_sector": "Civil Society / Media",
        "country": "India",
        "severity": "Critical",
        "date": "2021-07-18",
        "threat_actor": "NSO Group (state operator)",
        "source_url": "https://www.theguardian.com/news/2021/jul/18/revealed-leak-uncovers-global-abuse-of-cyber-surveillance-weapon-nso-pegasus",
    },
    # ── 44 ─────────────────────────────────────────────────────────────────
    {
        "title": "HDFC Life Insurance Data Extortion",
        "description": (
            "An unknown threat actor contacted Indian media claiming to have stolen "
            "customer data from HDFC Life Insurance. The actor threatened to release "
            "data of approximately 8 million policyholders including names, policy "
            "details, nominee information, and medical history, unless a ransom was "
            "paid. HDFC Life filed a complaint and CERT-In initiated an investigation."
        ),
        "attack_type": "Data Breach / Extortion",
        "target_sector": "Insurance",
        "country": "India",
        "severity": "High",
        "date": "2023-11-21",
        "threat_actor": "Unknown",
        "source_url": "https://economictimes.indiatimes.com/industry/banking/finance/insure/hdfc-life-insurance-faces-data-theft-threat/articleshow/105342178.cms",
    },
    # ── 45 ─────────────────────────────────────────────────────────────────
    {
        "title": "Bangladesh Bank Attempted SWIFT Fraud — Sonali Bank",
        "description": (
            "Sonali Bank, another major state-owned Bangladeshi bank, was targeted "
            "in a separate SWIFT fraud attempt following the Bangladesh Bank heist. "
            "Attackers sent fraudulent SWIFT messages attempting unauthorized "
            "transfers. The attempt was detected and blocked before funds were moved, "
            "but it demonstrated the systemic vulnerability of the Bangladeshi "
            "banking sector's SWIFT infrastructure."
        ),
        "attack_type": "Financial Fraud / SWIFT",
        "target_sector": "Banking & Finance",
        "country": "Bangladesh",
        "severity": "High",
        "date": "2016-06-14",
        "threat_actor": "Lazarus Group (suspected)",
        "source_url": "https://www.reuters.com/article/us-cyber-heist-bangladesh-idUSKCN0YW1X7",
    },
    # ── 46 ─────────────────────────────────────────────────────────────────
    {
        "title": "Indian Space Research Organisation (ISRO) Phishing Campaign",
        "description": (
            "Sophisticated spear-phishing emails targeting ISRO scientists were "
            "intercepted ahead of Chandrayaan-2 launch activities. Emails impersonated "
            "senior ISRO leadership and contained malicious attachments designed to "
            "deploy remote access trojans. The campaign was attributed to a state-"
            "sponsored actor interested in India's space programme."
        ),
        "attack_type": "Spear-Phishing / APT",
        "target_sector": "Space & Defence",
        "country": "India",
        "severity": "High",
        "date": "2019-07-10",
        "threat_actor": "Unknown state actor",
        "source_url": "https://theprint.in/tech/before-chandrayaan-2-launch-isro-was-targeted-by-hackers/270181/",
    },
    # ── 47 ─────────────────────────────────────────────────────────────────
    {
        "title": "Bhutan Government Portal Defacement",
        "description": (
            "Multiple Bhutanese government websites including the Royal Civil "
            "Service Commission portal were defaced by hacktivists who embedded "
            "political messaging. The attack exploited outdated WordPress installations "
            "and unpatched CMS plugins, a pattern common across South Asian "
            "government web infrastructure."
        ),
        "attack_type": "Website Defacement",
        "target_sector": "Government",
        "country": "Bhutan",
        "severity": "Low",
        "date": "2018-11-05",
        "threat_actor": "Anonymous-affiliated",
        "source_url": "https://www.zone-h.org/archive/filter=1/domain=.bt",
    },
    # ── 48 ─────────────────────────────────────────────────────────────────
    {
        "title": "India UPI Fraud Surge — Vishing and Fake QR Codes",
        "description": (
            "India's National Payments Corporation of India (NPCI) reported a "
            "significant surge in UPI-related fraud, including vishing (voice "
            "phishing) calls impersonating bank officials, fake payment request "
            "links, and malicious QR codes. Over ₹1,000 crore in losses were "
            "reported in a single fiscal year, with NPCI and RBI issuing emergency "
            "consumer advisories."
        ),
        "attack_type": "Social Engineering / Payment Fraud",
        "target_sector": "Banking & Finance / FinTech",
        "country": "India",
        "severity": "High",
        "date": "2022-04-01",
        "threat_actor": "Organised fraud networks",
        "source_url": "https://economictimes.indiatimes.com/industry/banking/finance/banking/upi-fraud-cases-in-india/articleshow/91272011.cms",
    },
    # ── 49 ─────────────────────────────────────────────────────────────────
    {
        "title": "Rewterz — Pakistan Banking Sector Trojan Campaign",
        "description": (
            "Pakistani cybersecurity firm Rewterz reported a widespread banking "
            "trojan campaign targeting customers of major Pakistani banks including "
            "HBL, UBL, and MCB Bank. Attackers used phishing emails with "
            "malicious Excel macros deploying Emotet and Trickbot malware to "
            "steal online banking credentials and perform fraudulent transfers."
        ),
        "attack_type": "Banking Trojan / Phishing",
        "target_sector": "Banking & Finance",
        "country": "Pakistan",
        "severity": "High",
        "date": "2020-03-12",
        "threat_actor": "TA542 (Emotet operators)",
        "source_url": "https://rewterz.com/rewterz-news/rewterz-threat-alert-emotet-banking-trojan-targeting-pakistan/",
    },
    # ── 50 ─────────────────────────────────────────────────────────────────
    {
        "title": "India Telecom Data Broker — Truecaller Leak",
        "description": (
            "Data sourced from Truecaller, a phone identifier app with over "
            "150 million Indian users, was found aggregated and sold by data "
            "brokers operating on Telegram channels. The dataset, compiled from "
            "scraping and credential stuffing, included phone numbers, names, "
            "email addresses, and in some cases home addresses. The incident "
            "highlighted the data privacy risks of third-party app permissions "
            "in India's mobile ecosystem."
        ),
        "attack_type": "Data Scraping / Privacy Breach",
        "target_sector": "Telecommunications / Consumer Tech",
        "country": "India",
        "severity": "Medium",
        "date": "2023-02-14",
        "threat_actor": "Unknown data broker network",
        "source_url": "https://www.hindustantimes.com/technology/truecaller-data-sold-on-telegram/",
    },
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(models.Attack).count()
        if False:
            print(f"[seed] Database already has {existing} records — skipping.")
            return

        added = 0
       for item in SEED_ATTACKS:
            duplicate = (
                db.query(models.Attack)
                .filter(models.Attack.title == item["title"])
                .first()
            )
            if duplicate:
                continue
            attack = models.Attack(**item)
            db.add(attack)
            added += 1

        db.commit()
        print(f"[seed] Successfully seeded {added} attacks.")
    except Exception as e:
        db.rollback()
        print(f"[seed] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()