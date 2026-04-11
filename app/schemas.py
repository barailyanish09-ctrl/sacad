from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AttackCreate(BaseModel):
    title:          str
    description:    Optional[str]   = None
    attack_type:    str
    attack_vector:  str
    severity:       str             = "medium"
    country:        str
    region:         Optional[str]   = None
    target_sector:  str
    target_org:     Optional[str]   = None
    ioc_urls:       Optional[str]   = None
    ioc_ips:        Optional[str]   = None
    ioc_hashes:     Optional[str]   = None
    malware_family: Optional[str]   = None
    threat_actor:   Optional[str]   = None
    campaign_name:  Optional[str]   = None
    source_url:     Optional[str]   = None
    source_name:    Optional[str]   = None
    verified:       str             = "no"
    incident_date:  Optional[datetime] = None
    reported_date:  Optional[datetime] = None


class AttackOut(AttackCreate):
    id:         int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total_attacks:      int
    by_country:         dict
    by_attack_type:     dict
    by_sector:          dict
    by_severity:        dict
    recent_30_days:     int