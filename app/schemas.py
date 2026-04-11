from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models import ATTACK_TYPES, ATTACK_VECTORS, SEVERITIES, SECTORS, COUNTRIES, STATUSES


class AttackCreate(BaseModel):
    title:              str
    description:        Optional[str]      = None
    attack_type:        str
    attack_vector:      str
    severity:           str                = "medium"
    country:            str
    region:             Optional[str]      = None
    target_sector:      str
    target_org:         Optional[str]      = None
    ioc_urls:           Optional[str]      = None
    ioc_ips:            Optional[str]      = None
    ioc_hashes:         Optional[str]      = None
    malware_family:     Optional[str]      = None
    threat_actor:       Optional[str]      = None
    campaign_name:      Optional[str]      = None
    source_url:         Optional[str]      = None
    source_name:        Optional[str]      = None
    status:             str                = "pending"
    verified_by:        Optional[str]      = None
    verification_notes: Optional[str]      = None
    confidence_score:   Optional[float]    = None
    verified:           str                = "no"
    incident_date:      Optional[datetime] = None
    reported_date:      Optional[datetime] = None

    @field_validator("attack_type")
    def validate_attack_type(cls, v):
        if v not in ATTACK_TYPES:
            raise ValueError(f"attack_type must be one of: {ATTACK_TYPES}")
        return v

    @field_validator("severity")
    def validate_severity(cls, v):
        if v not in SEVERITIES:
            raise ValueError(f"severity must be one of: {SEVERITIES}")
        return v

    @field_validator("target_sector")
    def validate_sector(cls, v):
        if v not in SECTORS:
            raise ValueError(f"target_sector must be one of: {SECTORS}")
        return v

    @field_validator("country")
    def validate_country(cls, v):
        if v not in COUNTRIES:
            raise ValueError(f"country must be one of: {COUNTRIES}")
        return v

    @field_validator("status")
    def validate_status(cls, v):
        if v not in STATUSES:
            raise ValueError(f"status must be one of: {STATUSES}")
        return v

    @field_validator("confidence_score")
    def validate_confidence(cls, v):
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("confidence_score must be between 0.0 and 1.0")
        return v


class AttackOut(AttackCreate):
    id:         int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total_attacks:    int
    by_country:       dict
    by_attack_type:   dict
    by_sector:        dict
    by_severity:      dict
    recent_30_days:   int