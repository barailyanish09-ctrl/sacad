from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime, timedelta

from app.database import get_db, init_db
from app.models import Attack
from app.schemas import AttackCreate, AttackOut, StatsOut
from app.admin import router as admin_router

app = FastAPI(
    title="SACAD — South Asia Cyber Attack Dataset",
    description="An open dataset and API of cyber attacks targeting South Asia.",
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

@app.get("/", tags=["Info"])
def root():
    return {"name": "SACAD API", "version": "1.0.0", "docs": "/docs"}

@app.get("/attacks", response_model=List[AttackOut], tags=["Attacks"])
def list_attacks(
    country:        Optional[str] = Query(None),
    attack_type:    Optional[str] = Query(None),
    attack_vector:  Optional[str] = Query(None),
    sector:         Optional[str] = Query(None),
    severity:       Optional[str] = Query(None),
    verified:       Optional[str] = Query(None),
    from_date:      Optional[datetime] = Query(None),
    to_date:        Optional[datetime] = Query(None),
    limit:          int = Query(50, le=500),
    offset:         int = Query(0),
    db:             Session = Depends(get_db),
):
    q = db.query(Attack)
    if country:       q = q.filter(Attack.country.ilike(f"%{country}%"))
    if attack_type:   q = q.filter(Attack.attack_type == attack_type)
    if attack_vector: q = q.filter(Attack.attack_vector == attack_vector)
    if sector:        q = q.filter(Attack.target_sector == sector)
    if severity:      q = q.filter(Attack.severity == severity)
    if verified:      q = q.filter(Attack.verified == verified)
    if from_date:     q = q.filter(Attack.incident_date >= from_date)
    if to_date:       q = q.filter(Attack.incident_date <= to_date)
    return q.order_by(Attack.incident_date.desc()).offset(offset).limit(limit).all()

@app.get("/attacks/{attack_id}", response_model=AttackOut, tags=["Attacks"])
def get_attack(attack_id: int, db: Session = Depends(get_db)):
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    