from sqlalchemy.orm import Session
from app.models.models import AuditLog

def log_audit(db: Session, user_id: int, action: str, entity_type: str, entity_id: int, description: str, commit: bool = True):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )
    db.add(audit)
    if commit:
        db.commit()
