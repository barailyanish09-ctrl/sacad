from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Attack(Base):
    __tablename__ = "attacks"

    id              = Column(Integer, primary_key=True, index=True)
    title           = Column(String(255), nullable=False)
    description     = Column(Text, nullable=True)
    attack_type     = Column(String(50), nullable=False)
    attack_vector   = Column(String(50), nullable=False)
    severity        = Column(String(20), default="medium")
    country         = Column(String(50), nullable=False)
    region          = Column(String(100), nullable=True)
    target_sector   = Column(String(50), nullable=False)
    target_org      = Column(String(255), nullable=True)
    ioc_urls        = Column(Text, nullable=True)
    ioc_ips         = Column(Text, nullable=True)
    ioc_hashes      = Column(Text, nullable=True)
    malware_family  = Column(String(100), nullable=True)
    threat_actor    = Column(String(255), nullable=True)
    campaign_name   = Column(String(255), nullable=True)
    source_url      = Column(String(500), nullable=True)
    source_name     = Column(String(255), nullable=True)
    verified        = Column(String(10), default="no")
    incident_date   = Column(DateTime, nullable=True)
    reported_date   = Column(DateTime, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Attack {self.id}: {self.title} [{self.country}]>"