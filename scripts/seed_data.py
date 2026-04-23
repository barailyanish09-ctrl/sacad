import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal, engine
from app import models
models.Base.metadata.create_all(bind=engine)

ATTACKS = []

def seed():
    db = SessionLocal()
    try:
        added = 0
        for item in ATTACKS:
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
