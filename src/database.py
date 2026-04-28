"""
ekajalakkam - Database Configuration
SQLAlchemy ORM setup for complaint management with multi-department admin support.
"""

from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import hashlib

# Database configuration
DATABASE_URL = "sqlite:///./ekajalakkam.db"

# Create engine with SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# ============================================================================
# Database Models
# ============================================================================

class Complaint(Base):
    """
    SQLAlchemy ORM model for storing complaints.
    """
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), unique=True, index=True, nullable=False)
    text = Column(Text, nullable=False)
    department = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(50), default="Pending")
    predicted_department = Column(String(100), nullable=True)
    predicted_severity = Column(String(20), nullable=True)
    citizen_name = Column(String(100), nullable=True)
    citizen_email = Column(String(100), nullable=True)
    citizen_phone = Column(String(20), nullable=True)
    location = Column(String(200), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Complaint(ticket_id='{self.ticket_id}', department='{self.department}', severity='{self.severity}')>"


class Admin(Base):
    """
    SQLAlchemy ORM model for department administrators.
    """
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Admin(username='{self.username}', department='{self.department}')>"


class Agent(Base):
    """
    SQLAlchemy ORM model for field agents.
    """
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Agent(username='{self.username}', department='{self.department}')>"


class ComplaintTimeline(Base):
    """
    SQLAlchemy ORM model for tracking complaint status changes.
    """
    __tablename__ = "complaint_timeline"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), index=True, nullable=False)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    updated_by = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ComplaintTimeline(ticket_id='{self.ticket_id}', status='{self.new_status}')>"


# ============================================================================
# Session Management
# ============================================================================

def get_db() -> Session:
    """
    Dependency to get database session.
    Yields database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Database Initialization
# ============================================================================

def create_tables() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def init_db() -> None:
    """Initialize database by creating tables and default admin/agent users."""
    create_tables()
    
    # Create default admin users for each department
    db = SessionLocal()
    try:
        # Default Admins
        default_admins = [
            {"username": "electricity_admin", "password": "admin123", "department": "Electricity", "full_name": "Electricity Department Admin"},
            {"username": "water_admin", "password": "admin123", "department": "Water Supply", "full_name": "Water Supply Department Admin"},
            {"username": "sewage_admin", "password": "admin123", "department": "Waste-Water/Sewage", "full_name": "Sewage Department Admin"},
        ]
        
        for admin_data in default_admins:
            existing = db.query(Admin).filter(Admin.username == admin_data["username"]).first()
            if not existing:
                admin = Admin(
                    username=admin_data["username"],
                    password_hash=hash_password(admin_data["password"]),
                    department=admin_data["department"],
                    full_name=admin_data["full_name"],
                    is_active=True
                )
                db.add(admin)

        # Default Agents
        default_agents = [
            {"username": "electricity_agent", "password": "agent123", "department": "Electricity", "full_name": "Electricity Field Agent"},
            {"username": "water_agent", "password": "agent123", "department": "Water Supply", "full_name": "Water Supply Field Agent"},
            {"username": "sewage_agent", "password": "agent123", "department": "Waste-Water/Sewage", "full_name": "Sewage Field Agent"},
        ]
        
        for agent_data in default_agents:
            existing = db.query(Agent).filter(Agent.username == agent_data["username"]).first()
            if not existing:
                agent = Agent(
                    username=agent_data["username"],
                    password_hash=hash_password(agent_data["password"]),
                    department=agent_data["department"],
                    full_name=agent_data["full_name"],
                    is_active=True
                )
                db.add(agent)
        
        db.commit()
        print("Database initialized successfully with default admin and agent users!")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


# ============================================================================
# Helper Functions
# ============================================================================

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


# ============================================================================
# User Authentication
# ============================================================================

def authenticate_admin(db: Session, username: str, password: str) -> Optional[Admin]:
    """
    Authenticate an admin user.
    
    Args:
        db: Database session
        username: Admin username
        password: Admin password
        
    Returns:
        Admin object if authenticated, None otherwise
    """
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin and verify_password(password, admin.password_hash) and admin.is_active:
        # Update last login
        admin.last_login = datetime.utcnow()
        db.commit()
        db.refresh(admin)
        return admin
    return None


def authenticate_agent(db: Session, username: str, password: str) -> Optional[Agent]:
    """
    Authenticate an agent user.
    
    Args:
        db: Database session
        username: Agent username
        password: Agent password
        
    Returns:
        Agent object if authenticated, None otherwise
    """
    agent = db.query(Agent).filter(Agent.username == username).first()
    if agent and verify_password(password, agent.password_hash) and agent.is_active:
        # Update last login
        agent.last_login = datetime.utcnow()
        db.commit()
        db.refresh(agent)
        return agent
    return None


def get_admin_by_username(db: Session, username: str) -> Optional[Admin]:
    """Get admin by username."""
    return db.query(Admin).filter(Admin.username == username).first()


def get_admin_by_department(db: Session, department: str) -> Optional[Admin]:
    """Get admin by department."""
    return db.query(Admin).filter(Admin.department == department).first()


def update_admin_last_login(db: Session, username: str) -> None:
    """Update admin's last login timestamp."""
    admin = get_admin_by_username(db, username)
    if admin:
        admin.last_login = datetime.utcnow()
        db.commit()


# ============================================================================
# Complaint Operations
# ============================================================================

def create_complaint(
    db: Session,
    ticket_id: str,
    text: str,
    department: str,
    severity: str,
    predicted_department: Optional[str] = None,
    predicted_severity: Optional[str] = None,
    citizen_name: Optional[str] = None,
    citizen_email: Optional[str] = None,
    citizen_phone: Optional[str] = None,
    location: Optional[str] = None
) -> Complaint:
    """Create a new complaint record."""
    db_complaint = Complaint(
        ticket_id=ticket_id,
        text=text,
        department=department,
        severity=severity,
        predicted_department=predicted_department or department,
        predicted_severity=predicted_severity or severity,
        citizen_name=citizen_name,
        citizen_email=citizen_email,
        citizen_phone=citizen_phone,
        location=location
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    # Add timeline entry
    add_timeline_entry(db, ticket_id, None, "Pending", "System")
    
    return db_complaint


def get_complaint_by_ticket_id(db: Session, ticket_id: str) -> Optional[Complaint]:
    """Get complaint by ticket ID."""
    return db.query(Complaint).filter(Complaint.ticket_id == ticket_id).first()


def get_all_complaints(db: Session, skip: int = 0, limit: int = 100) -> List[Complaint]:
    """Get all complaints with pagination."""
    return db.query(Complaint).order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()


def get_complaints_by_department(db: Session, department: str, skip: int = 0, limit: int = 100) -> List[Complaint]:
    """Get complaints filtered by department."""
    return db.query(Complaint).filter(
        Complaint.department == department
    ).order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()


def get_complaints_by_status(db: Session, status: str, department: Optional[str] = None) -> List[Complaint]:
    """Get complaints filtered by status and optionally by department."""
    query = db.query(Complaint).filter(Complaint.status == status)
    if department:
        query = query.filter(Complaint.department == department)
    return query.order_by(Complaint.created_at.desc()).all()


def update_complaint_status(db: Session, ticket_id: str, new_status: str, updated_by: Optional[str] = None, notes: Optional[str] = None) -> Optional[Complaint]:
    """Update complaint status and add timeline entry."""
    db_complaint = get_complaint_by_ticket_id(db, ticket_id)
    if db_complaint:
        old_status = db_complaint.status
        db_complaint.status = new_status
        db_complaint.updated_at = datetime.utcnow()
        
        if new_status in ["Resolved", "Closed"]:
            db_complaint.resolved_at = datetime.utcnow()
        
        if notes:
            db_complaint.admin_notes = notes
        
        db.commit()
        db.refresh(db_complaint)
        
        # Add timeline entry
        add_timeline_entry(db, ticket_id, old_status, new_status, updated_by, notes)
        
    return db_complaint


def get_complaint_timeline(db: Session, ticket_id: str) -> List[ComplaintTimeline]:
    """Get timeline entries for a complaint."""
    return db.query(ComplaintTimeline).filter(
        ComplaintTimeline.ticket_id == ticket_id
    ).order_by(ComplaintTimeline.created_at.asc()).all()


def add_timeline_entry(db: Session, ticket_id: str, old_status: Optional[str], new_status: str, updated_by: Optional[str] = None, notes: Optional[str] = None) -> None:
    """Add a timeline entry for a complaint."""
    timeline = ComplaintTimeline(
        ticket_id=ticket_id,
        old_status=old_status,
        new_status=new_status,
        updated_by=updated_by,
        notes=notes
    )
    db.add(timeline)
    db.commit()


# ============================================================================
# Dashboard Statistics
# ============================================================================

def get_dashboard_stats(db: Session) -> dict:
    """Get aggregated statistics for admin dashboard (all departments)."""
    total_complaints = db.query(Complaint).count()

    # Count by department
    departments = db.query(Complaint.department).distinct().all()
    by_department = {}
    for dept in departments:
        count = db.query(Complaint).filter(Complaint.department == dept[0]).count()
        by_department[dept[0]] = count

    # Count by severity
    high_severity = db.query(Complaint).filter(Complaint.severity == "High").count()
    low_severity = db.query(Complaint).filter(Complaint.severity == "Low").count()

    # Count by status
    pending = db.query(Complaint).filter(Complaint.status == "Pending").count()
    in_progress = db.query(Complaint).filter(Complaint.status == "In Progress").count()
    resolved = db.query(Complaint).filter(Complaint.status == "Resolved").count()
    closed = db.query(Complaint).filter(Complaint.status == "Closed").count()

    return {
        "total_complaints": total_complaints,
        "by_department": by_department,
        "by_severity": {
            "High": high_severity,
            "Low": low_severity
        },
        "by_status": {
            "Pending": pending,
            "In Progress": in_progress,
            "Resolved": resolved,
            "Closed": closed
        },
        "high_severity_count": high_severity,
        "pending_count": pending
    }


def get_department_dashboard_stats(db: Session, department: str) -> dict:
    """Get aggregated statistics for a specific department dashboard."""
    total_complaints = db.query(Complaint).filter(Complaint.department == department).count()

    # Count by severity
    high_severity = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.severity == "High"
    ).count()
    low_severity = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.severity == "Low"
    ).count()

    # Count by status
    pending = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.status == "Pending"
    ).count()
    in_progress = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.status == "In Progress"
    ).count()
    resolved = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.status == "Resolved"
    ).count()
    closed = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.status == "Closed"
    ).count()

    # Recent complaints (last 7 days)
    from datetime import timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_complaints = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.created_at >= seven_days_ago
    ).count()

    # Average resolution time (for resolved/closed complaints)
    resolved_complaints = db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.resolved_at.isnot(None)
    ).all()
    
    avg_resolution_hours = 0
    if resolved_complaints:
        total_hours = 0
        count = 0
        for complaint in resolved_complaints:
            if complaint.resolved_at and complaint.created_at:
                delta = complaint.resolved_at - complaint.created_at
                total_hours += delta.total_seconds() / 3600
                count += 1
        if count > 0:
            avg_resolution_hours = round(total_hours / count, 1)

    return {
        "total_complaints": total_complaints,
        "by_severity": {
            "High": high_severity,
            "Low": low_severity
        },
        "by_status": {
            "Pending": pending,
            "In Progress": in_progress,
            "Resolved": resolved,
            "Closed": closed
        },
        "high_severity_count": high_severity,
        "pending_count": pending,
        "recent_complaints": recent_complaints,
        "avg_resolution_hours": avg_resolution_hours,
        "resolved_count": resolved + closed
    }


def get_complaint_count_by_department(db: Session, department: str) -> int:
    """Get total complaint count for a department."""
    return db.query(Complaint).filter(Complaint.department == department).count()


def get_pending_count_by_department(db: Session, department: str) -> int:
    """Get pending complaint count for a department."""
    return db.query(Complaint).filter(
        Complaint.department == department,
        Complaint.status == "Pending"
    ).count()
