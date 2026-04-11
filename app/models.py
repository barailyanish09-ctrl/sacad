from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

ATTACK_TYPES   = ["phishing","ransomware","malware","defacement","ddos","data_breach","scam","social_engineering","supply_chain","other"]
ATTACK_VECTORS = ["email","sms","phone","web","usb","supply_chain","insider","unknown"]
SEVERITIES     = ["low","medium","high","critical"]
SECTORS        = ["government","banking","telecom","healthcare","education","ecommerce","military","ngo","individual","other"]
COUNTRIES      = ["Nepal","India","Bangladesh","Pakistan","Sri Lanka","Bhutan","Myanmar","Regional"]
STATUSES       = ["pending","verified","rejected"]

class Attack(Base):
    __tablename__ = "attacks"

    id                  = Column(Integer, primary_key=True, index=True)
    title               = Column(String(255), nullable=False)
    description         = Column(Text, nullable=True)

    attack_type         = Column(String(50), nullable=False)
    attack_vector       = Column(String(50), nullable=False)
    severity            = Column(String(20), nullable=False, default="medium")

    country             = Column(String(50), nullable=False)
    region              = Column(String(100), nullable=True)

    target_sector       = Column(String(50), nullable=False)
    target_org          = Column(String(255), nullable=True)

    ioc_urls            = Column(Text, nullable=True)
    ioc_ips             = Column(Text, nullable=True)
    ioc_hashes          = Column(Text, nullable=True)
    malware_family      = Column(String(100), nullable=True)

    threat_actor        = Column(String(255), nullable=True)
    campaign_name       = Column(String(255), nullable=True)

    source_url          = Column(String(500), nullable=True)
    source_name         = Column(String(255), nullable=True)

    status              = Column(String(20), default="pending")
    verified_by         = Column(String(255), nullable=True)
    verification_notes  = Column(Text, nullable=True)
    confidence_score    = Column(Float, nullable=True)

    verified            = Column(String(10), default="no")

    incident_date       = Column(DateTime, nullable=True)
    reported_date       = Column(DateTime, nullable=True)
    created_at          = Column(DateTime, default=datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Attack {self.id}: {self.title} [{self.country}]>"