from app.db.database import engine, Base, SessionLocal
from app.models.models import User
from app.core.security import get_password_hash
from app.core.config import get_settings

settings = get_settings()

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have users
    if db.query(User).first() is None:
        default_password = settings.DEFAULT_DEMO_PASSWORD
        hashed_password = get_password_hash(default_password)
        
        manager = User(
            name="Manager One",
            email="manager1@example.com",
            password_hash=hashed_password,
            role="MANAGER",
            department="Engineering"
        )
        db.add(manager)
        db.commit()
        db.refresh(manager)
        
        emp1 = User(
            name="Employee One",
            email="employee1@example.com",
            password_hash=hashed_password,
            role="EMPLOYEE",
            department="Engineering",
            manager_id=manager.id
        )
        emp2 = User(
            name="Employee Two",
            email="employee2@example.com",
            password_hash=hashed_password,
            role="EMPLOYEE",
            department="Engineering",
            manager_id=manager.id
        )
        
        admin = User(
            name="IT Admin",
            email="itadmin@example.com",
            password_hash=hashed_password,
            role="IT_ADMIN",
            department="IT"
        )
        
        db.add_all([emp1, emp2, admin])
        db.commit()

    db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized.")
