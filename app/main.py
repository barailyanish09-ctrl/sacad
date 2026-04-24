from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime, timedelta

from app.database import get_db, init_db
from app.models import Attack, ATTACK_TYPES, ATTACK_VECTORS, SEVERITIES, SECTORS, COUNTRIES
from app.schemas import AttackCreate, AttackOut, StatsOut
from app.admin import router as admin_router

app = FastAPI(
    title="SACAD — South Asia Cyber Attack Dataset",
    description="The open cyber attack graph for South Asia: a live dataset + API + stats on real incidents, IoCs, and targets in the region.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)

@app.on_event("startup")
def on_startup():
    init_db()


# ── / ── Dataset info
@app.get("/", tags=["Info"])
def root(db: Session = Depends(get_db)):
    total = db.query(Attack).count()
    last  = db.query(Attack.created_at).order_by(Attack.created_at.desc()).first()
    return {
        "name":          "SACAD — South Asia Cyber Attack Dataset",
        "version":       "1.0.0",
        "description":   "The open cyber attack graph for South Asia.",
        "total_records": total,
        "last_updated":  last[0].isoformat() if last else None,
        "docs":          "https://sacad-api.onrender.com/docs",
        "github":        "https://github.com/barailyanish09-ctrl/sacad",
        "enums": {
            "attack_types":   ATTACK_TYPES,
            "attack_vectors": ATTACK_VECTORS,
            "severities":     SEVERITIES,
            "sectors":        SECTORS,
            "countries":      COUNTRIES,
        }
    }


# ── /attacks ── List & Filter
@app.get("/attacks", response_model=List[AttackOut], tags=["Attacks"])
def list_attacks(
    country:       Optional[str] = Query(None),
    attack_type:   Optional[str] = Query(None),
    attack_vector: Optional[str] = Query(None),
    sector:        Optional[str] = Query(None),
    severity:      Optional[str] = Query(None),
    status:        Optional[str] = Query(None),
    from_date:     Optional[datetime] = Query(None),
    to_date:       Optional[datetime] = Query(None),
    limit:         int = Query(50, le=500),
    offset:        int = Query(0),
    db:            Session = Depends(get_db),
):
    q = db.query(Attack)
    if country:       q = q.filter(Attack.country.ilike(f"%{country}%"))
    if attack_type:   q = q.filter(Attack.attack_type == attack_type)
    if attack_vector: q = q.filter(Attack.attack_vector == attack_vector)
    if sector:        q = q.filter(Attack.target_sector == sector)
    if severity:      q = q.filter(Attack.severity == severity)
    if status:        q = q.filter(Attack.status == status)
    if from_date:     q = q.filter(Attack.incident_date >= from_date)
    if to_date:       q = q.filter(Attack.incident_date <= to_date)
    return q.order_by(Attack.incident_date.desc()).offset(offset).limit(limit).all()


# ── /attacks/recent ── Last 10 attacks
@app.get("/attacks/recent", response_model=List[AttackOut], tags=["Attacks"])
def recent_attacks(limit: int = 10, db: Session = Depends(get_db)):
    return (
        db.query(Attack)
        .order_by(Attack.created_at.desc())
        .limit(limit)
        .all()
    )


# ── /attacks/by-country ── Group by country
@app.get("/attacks/by-country", tags=["Attacks"])
def attacks_by_country(db: Session = Depends(get_db)):
    rows = (
        db.query(Attack.country, func.count(Attack.id))
        .group_by(Attack.country)
        .order_by(func.count(Attack.id).desc())
        .all()
    )
    return [{"country": r[0], "count": r[1]} for r in rows]


# ── /attacks/{id} ── Single record
@app.get("/attacks/{attack_id}", response_model=AttackOut, tags=["Attacks"])
def get_attack(attack_id: int, db: Session = Depends(get_db)):
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    return attack


# ── POST /attacks ── Submit
@app.post("/attacks", response_model=AttackOut, status_code=201, tags=["Attacks"])
def create_attack(payload: AttackCreate, db: Session = Depends(get_db)):
    attack = Attack(**payload.dict())
    attack.status   = "pending"
    attack.verified = "no"
    db.add(attack)
    db.commit()
    db.refresh(attack)
    return attack


# ── /stats ── Aggregated stats
@app.get("/stats", response_model=StatsOut, tags=["Dashboard"])
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Attack).count()
    def count_by(field):
        rows = db.query(field, func.count(field)).group_by(field).all()
        return {row[0]: row[1] for row in rows if row[0]}
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent = db.query(Attack).filter(Attack.created_at >= thirty_days_ago).count()
    return StatsOut(
        total_attacks=total,
        by_country=count_by(Attack.country),
        by_attack_type=count_by(Attack.attack_type),
        by_sector=count_by(Attack.target_sector),
        by_severity=count_by(Attack.severity),
        recent_30_days=recent,
    )


# ── /ioc/search ── Search by IP or URL
@app.get("/ioc/search", tags=["IOC"])
def ioc_search(
    ip:  Optional[str] = Query(None, description="Search by IP address"),
    url: Optional[str] = Query(None, description="Search by URL"),
    h:   Optional[str] = Query(None, description="Search by file hash"),
    db:  Session = Depends(get_db),
):
    if not any([ip, url, h]):
        raise HTTPException(status_code=400, detail="Provide at least one of: ip, url, h")
    q = db.query(Attack)
    if ip:  q = q.filter(Attack.ioc_ips.ilike(f"%{ip}%"))
    if url: q = q.filter(Attack.ioc_urls.ilike(f"%{url}%"))
    if h:   q = q.filter(Attack.ioc_hashes.ilike(f"%{h}%"))
    results = q.all()
    return {
        "query": {"ip": ip, "url": url, "hash": h},
        "total": len(results),
        "matches": [{"id": a.id, "title": a.title, "country": a.country,
                     "attack_type": a.attack_type, "severity": a.severity,
                     "ioc_ips": a.ioc_ips, "ioc_urls": a.ioc_urls} for a in results]
    }

# ── /attacks/timeline ── Group by month
@app.get("/attacks/timeline", tags=["Attacks"])
def attacks_timeline(db: Session = Depends(get_db)):
    attacks = db.query(Attack).filter(Attack.incident_date.isnot(None)).all()
    timeline = {}
    for a in attacks:
        key = a.incident_date.strftime("%Y-%m")
        timeline[key] = timeline.get(key, 0) + 1
    return [{"month": k, "count": v} for k, v in sorted(timeline.items())]


# ── /attacks/by-sector ── Group by sector
@app.get("/attacks/by-sector", tags=["Attacks"])
def attacks_by_sector(db: Session = Depends(get_db)):
    rows = (
        db.query(Attack.target_sector, func.count(Attack.id))
        .group_by(Attack.target_sector)
        .order_by(func.count(Attack.id).desc())
        .all()
    )
    return [{"sector": r[0], "count": r[1]} for r in rows]


# ── /attacks/threat-actors ── Top threat actors
@app.get("/attacks/threat-actors", tags=["Attacks"])
def top_threat_actors(db: Session = Depends(get_db)):
    rows = (
        db.query(Attack.threat_actor, func.count(Attack.id))
        .filter(Attack.threat_actor.isnot(None))
        .group_by(Attack.threat_actor)
        .order_by(func.count(Attack.id).desc())
        .limit(10)
        .all()
    )
    return [{"actor": r[0], "count": r[1]} for r in rows]


# ── /attacks/mitre ── MITRE ATT&CK breakdown
@app.get("/attacks/mitre", tags=["Attacks"])
def mitre_breakdown(db: Session = Depends(get_db)):
    rows = (
        db.query(Attack.mitre_tactic, func.count(Attack.id))
        .filter(Attack.mitre_tactic.isnot(None))
        .group_by(Attack.mitre_tactic)
        .order_by(func.count(Attack.id).desc())
        .all()
    )
    return [{"tactic": r[0], "count": r[1]} for r in rows]
# ── /search ── Keyword search
@app.get("/search", response_model=List[AttackOut], tags=["Attacks"])
def search_attacks(
    q:     str = Query(..., min_length=2),
    db:    Session = Depends(get_db),
    limit: int = 20,
):
    return (
        db.query(Attack)
        .filter(
            Attack.title.ilike(f"%{q}%") |
            Attack.description.ilike(f"%{q}%") |
            Attack.threat_actor.ilike(f"%{q}%") |
            Attack.campaign_name.ilike(f"%{q}%")
        )
        .limit(limit)
        .all()
    )