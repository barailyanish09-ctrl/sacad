from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import os

from app.database import get_db
from app.models import Attack
from app.schemas import AttackOut

router = APIRouter(prefix="/admin", tags=["Admin"])

ADMIN_KEY = os.getenv("ADMIN_KEY", "change-this-secret-key")

def require_admin(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True

@router.get("/queue", response_model=List[AttackOut])
def get_verification_queue(
    limit: int = 50,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    return (
        db.query(Attack)
        .filter(Attack.verified == "no")
        .order_by(Attack.created_at.desc())
        .limit(limit)
        .all()
    )

@router.patch("/verify/{attack_id}", response_model=AttackOut)
def verify_attack(
    attack_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    attack.verified   = "yes"
    attack.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(attack)
    return attack

@router.delete("/reject/{attack_id}")
def reject_attack(
    attack_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    attack = db.query(Attack).filter(Attack.id == attack_id).first()
    if not attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    db.delete(attack)
    db.commit()
    return {"detail": f"Attack {attack_id} deleted"}

@router.get("/stats/detailed")
def detailed_stats(
    db: Session = Depends(get_db),
    _: bool = Depends(require_admin),
):
    total      = db.query(Attack).count()
    verified   = db.query(Attack).filter(Attack.verified == "yes").count()
    partial    = db.query(Attack).filter(Attack.verified == "partial").count()
    unverified = db.query(Attack).filter(Attack.verified == "no").count()
    return {
        "total":      total,
        "verified":   verified,
        "partial":    partial,
        "unverified": unverified,
    }