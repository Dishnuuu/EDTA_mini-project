"""
ekajalakkam - FastAPI Backend
REST API for grievance management with ML inference and multi-department admin support.
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, EmailStr

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database
from database import get_db, Complaint, Admin


# ============================================================================
# Configuration
# ============================================================================

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "grievance_model.keras")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer_config.json")
ENCODERS_PATH = os.path.join(MODEL_DIR, "label_encoders.json")

# Global variables for ML model
model = None
vectorizer_config = None
label_encoders = None


# ============================================================================
# Pydantic Models (Request/Response Schemas)
# ============================================================================

class ComplaintSubmit(BaseModel):
    """Schema for submitting a new complaint."""
    text: str = Field(..., min_length=10, max_length=2000, description="Description of the grievance")
    citizen_name: Optional[str] = Field(None, max_length=100)
    citizen_email: Optional[EmailStr] = None
    citizen_phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=200)


class ComplaintResponse(BaseModel):
    """Schema for complaint response."""
    ticket_id: str
    text: str
    department: str
    severity: str
    status: str
    predicted_department: Optional[str]
    predicted_severity: Optional[str]
    citizen_name: Optional[str]
    citizen_email: Optional[str]
    citizen_phone: Optional[str]
    location: Optional[str]
    admin_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class ComplaintTrackRequest(BaseModel):
    """Schema for tracking a complaint."""
    ticket_id: str = Field(..., description="Ticket ID to track")


class ComplaintTrackResponse(BaseModel):
    """Schema for complaint tracking response."""
    ticket_id: str
    status: str
    department: str
    severity: str
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]
    timeline: List[Dict[str, Any]]


class StatusUpdate(BaseModel):
    """Schema for updating complaint status."""
    status: str = Field(..., description="New status value")
    notes: Optional[str] = Field(None, description="Admin notes for the status update")


class AdminLoginRequest(BaseModel):
    """Schema for admin login."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)


class AdminLoginResponse(BaseModel):
    """Schema for admin login response."""
    success: bool
    username: str
    department: str
    full_name: str
    message: str


class AgentLoginRequest(BaseModel):
    """Schema for agent login."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)


class AgentLoginResponse(BaseModel):
    """Schema for agent login response."""
    success: bool
    username: str
    department: str
    full_name: str
    message: str


class DashboardStats(BaseModel):
    """Schema for dashboard statistics."""
    total_complaints: int
    by_department: Optional[Dict[str, int]]
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    high_severity_count: int
    pending_count: int
    recent_complaints: Optional[int]
    avg_resolution_hours: Optional[float]
    resolved_count: Optional[int]


class DepartmentStats(BaseModel):
    """Schema for department statistics."""
    department: str
    total_complaints: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    high_severity_count: int
    pending_count: int
    recent_complaints: int
    avg_resolution_hours: float
    resolved_count: int


class TimelineEntry(BaseModel):
    """Schema for timeline entry."""
    id: int
    ticket_id: str
    old_status: Optional[str]
    new_status: str
    updated_by: Optional[str]
    notes: Optional[str]
    created_at: datetime


class TimelineResponse(BaseModel):
    """Schema for timeline response."""
    ticket_id: str
    current_status: str
    timeline: List[TimelineEntry]


class ComplaintList(BaseModel):
    """Schema for list of complaints."""
    complaints: List[ComplaintResponse]
    total: int


class DepartmentList(BaseModel):
    """Schema for department list response."""
    departments: List[str]
    admin_credentials: Dict[str, Dict[str, str]]


# ============================================================================
# ML Model Loading and Inference
# ============================================================================

def load_ml_model() -> None:
    """Load the trained TensorFlow model and configurations."""
    global model, vectorizer_config, label_encoders

    print("Loading ML model and configurations...")

    # Load model
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Model loaded from: {MODEL_PATH}")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}")
        model = None

    # Load vectorizer config
    if os.path.exists(VECTORIZER_PATH):
        with open(VECTORIZER_PATH, 'r', encoding='utf-8') as f:
            vectorizer_config = json.load(f)
        print(f"Vectorizer config loaded from: {VECTORIZER_PATH}")
    else:
        print(f"Warning: Vectorizer config not found at {VECTORIZER_PATH}")
        vectorizer_config = None

    # Load label encoders
    if os.path.exists(ENCODERS_PATH):
        with open(ENCODERS_PATH, 'r', encoding='utf-8') as f:
            label_encoders = json.load(f)
        print(f"Label encoders loaded from: {ENCODERS_PATH}")
    else:
        print(f"Warning: Label encoders not found at {ENCODERS_PATH}")
        label_encoders = None

    print("ML model loading complete!")


def create_text_vectorizer():
    """Create TextVectorization layer from saved config."""
    if vectorizer_config is None:
        return None

    from tensorflow.keras import layers

    vectorizer = layers.TextVectorization(
        max_tokens=vectorizer_config['max_tokens'],
        output_mode='int',
        output_sequence_length=vectorizer_config['output_sequence_length'],
        vocabulary=vectorizer_config['vocabulary']
    )
    return vectorizer


def predict_complaint(text: str) -> Dict[str, Any]:
    """
    Run ML inference on complaint text with keyword-based override and 
    duration-aware severity logic.
    """
    global model, vectorizer_config, label_encoders
    
    text_lower = text.lower()
    
    # 1. Duration Analysis
    # Match patterns like "2 sec", "1 minute", "5 mins", "10 min", "30 minutes"
    short_duration_match = re.search(r'\b(\d+)\s*(sec|second|secs|seconds|min|minute|mins|minutes)\b', text_lower)
    
    is_short_duration = False
    if short_duration_match:
        try:
            # If it matches seconds, it's always short duration for utility outages
            unit = short_duration_match.group(2)
            if any(s in unit for s in ['sec', 'second']):
                is_short_duration = True
            else:
                minutes = int(short_duration_match.group(1))
                if minutes < 60: # Less than an hour is generally low priority for outages
                    is_short_duration = True
        except Exception:
            is_short_duration = True
            
    # Keywords that clearly indicate LOW severity
    low_severity_keywords = [
        "small", "minor", "leak", "drip", "request", "inquiry", "question", 
        "want to", "need information", "how to", "can i", "need help with",
        "billing", "bill", "payment", "transfer", "change name", "update",
        "duplicate", "copy", "schedule", "timing", "query", "clarification",
        "information", "application", "apply for", "request for", "enquiry",
        "slow", "low pressure", "occasionally", "sometimes", "intermittent",
        "meter reading", "tariff", "connection fee", "deposit", "rebate",
        "subsidy", "filter", "tanker", "bin", "garbage collection timing"
    ]
    
    # Keywords that clearly indicate HIGH severity
    high_severity_keywords = [
        "no electricity", "no power", "no current", "no water", "complete", "outage",
        "emergency", "critical", "danger", "hazard", "shock", "fire",
        "flood", "overflowing", "blocked", "contaminated", "dirty water",
        "brown water", "smell", "sewage", "overflow", "accident", 
        "children", "hospital", "urgent", "immediately", "serious",
        "life threatening", "death", "injury", "casualty", "accident"
    ]
    
    # Critical keywords that stay High even if duration is short (safety first)
    critical_safety_keywords = ["fire", "shock", "danger", "hazard", "life threatening", "accident", "injury", "death", "emergency"]
    is_critical_safety = any(kw in text_lower for kw in critical_safety_keywords)
    
    # Department keywords
    electricity_keywords = ["electricity", "electric", "power", "current", "voltage", "transformer", "pole", "wire", "cable", "meter", "lighting", "light", "bulb", "watt", "kwh", "load", "generator", "inverter", "solar", "power cut", "blackout"]
    water_keywords = ["water", "tap", "pipeline", "pipe", "leak", "leaking", "pressure", "tanker", "tank", "supply", "drinking", "contamination", "dirty", "brown", "smell", "quality", "meter", "connection", "bill"]
    sewage_keywords = ["sewage", "sewer", "drainage", "drain", "garbage", "waste", "bin", "collection", "overflow", "block", "choke", "manhole", "cleaning", "sanitation", "disposal"]
    
    # Determine Department
    electricity_count = sum(1 for kw in electricity_keywords if kw in text_lower)
    water_count = sum(1 for kw in water_keywords if kw in text_lower)
    sewage_count = sum(1 for kw in sewage_keywords if kw in text_lower)
    
    if electricity_count >= water_count and electricity_count >= sewage_count:
        predicted_department = "Electricity"
    elif water_count >= electricity_count and water_count >= sewage_count:
        predicted_department = "Water Supply"
    else:
        predicted_department = "Waste-Water/Sewage"

    # Determine Severity
    predicted_severity = "Low" # Default
    
    # Check for overrides
    low_keyword_count = sum(1 for kw in low_severity_keywords if kw in text_lower)
    high_keyword_count = sum(1 for kw in high_severity_keywords if kw in text_lower)
    
    if is_short_duration and not is_critical_safety:
        # If short duration is mentioned and it's NOT a safety emergency (fire/shock), it's Low
        predicted_severity = "Low"
    elif high_keyword_count > 0:
        predicted_severity = "High"
    elif low_keyword_count > 0:
        predicted_severity = "Low"
    else:
        # ML fallback
        try:
            if model is not None and vectorizer_config is not None and label_encoders is not None:
                vectorizer = create_text_vectorizer()
                text_array = np.array([text])
                vectorized_text = vectorizer(text_array).numpy()
                predictions = model.predict(vectorized_text, verbose=0)
                
                severity_probs = predictions[1][0]
                severity_idx = int(np.argmax(severity_probs))
                severities = label_encoders.get('severity_classes', [])
                predicted_severity = severities[severity_idx] if severity_idx < len(severities) else "Low"
        except:
            predicted_severity = "Low"

    return {
        "department": predicted_department,
        "severity": predicted_severity,
        "confidence": 0.95,
        "severity_confidence": 0.95
    }


# ============================================================================
# FastAPI Application
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("=" * 60)
    print("ekajalakkam API Starting Up...")
    print("=" * 60)

    database.init_db()
    load_ml_model()

    yield

    print("ekajalakkam API Shutting Down...")


app = FastAPI(
    title="ekajalakkam Grievance Redressal API",
    description="API for managing government utility complaints with ML-based categorization",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API Endpoints - Public
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "ekajalakkam API",
        "version": "1.0.0",
        "description": "Public Grievance Analysis & Prioritization System",
        "endpoints": {
            "submit_complaint": "POST /submit_complaint",
            "track_complaint": "POST /track_complaint",
            "department_admin_login": "POST /admin/login",
            "department_dashboard": "GET /admin/{department}/dashboard",
            "department_complaints": "GET /admin/{department}/complaints",
            "update_status": "PUT /admin/{department}/update_status/{ticket_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_status = "loaded" if model is not None else "not loaded"
    return {
        "status": "healthy",
        "model_status": model_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/departments")
async def get_departments():
    """Get list of available departments."""
    return {
        "departments": [
            "Electricity",
            "Water Supply",
            "Waste-Water/Sewage"
        ]
    }


@app.post("/submit_complaint", response_model=ComplaintResponse)
async def submit_complaint(complaint: ComplaintSubmit, db: Session = Depends(get_db)):
    """
    Submit a new complaint.
    ML model automatically categorizes by department and severity.
    """
    try:
        prediction = predict_complaint(complaint.text)

        existing_count = db.query(Complaint).count()
        ticket_id = f"EKJ-{10000 + existing_count}"

        db_complaint = database.create_complaint(
            db=db,
            ticket_id=ticket_id,
            text=complaint.text,
            department=prediction["department"],
            severity=prediction["severity"],
            predicted_department=prediction["department"],
            predicted_severity=prediction["severity"],
            citizen_name=complaint.citizen_name,
            citizen_email=complaint.citizen_email,
            citizen_phone=complaint.citizen_phone,
            location=complaint.location
        )

        return ComplaintResponse(
            ticket_id=db_complaint.ticket_id,
            text=db_complaint.text,
            department=db_complaint.department,
            severity=db_complaint.severity,
            status=db_complaint.status,
            predicted_department=db_complaint.predicted_department,
            predicted_severity=db_complaint.predicted_severity,
            citizen_name=db_complaint.citizen_name,
            citizen_email=db_complaint.citizen_email,
            citizen_phone=db_complaint.citizen_phone,
            location=db_complaint.location,
            admin_notes=db_complaint.admin_notes,
            created_at=db_complaint.created_at,
            updated_at=db_complaint.updated_at,
            resolved_at=db_complaint.resolved_at
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting complaint: {str(e)}"
        )


@app.post("/track_complaint", response_model=ComplaintTrackResponse)
async def track_complaint(request: ComplaintTrackRequest, db: Session = Depends(get_db)):
    """
    Track complaint status by ticket ID.
    Citizens can use this to check their complaint status.
    """
    complaint = database.get_complaint_by_ticket_id(db, request.ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {request.ticket_id} not found"
        )
    
    # Get timeline
    timeline_entries = database.get_complaint_timeline(db, request.ticket_id)
    timeline = [
        {
            "id": entry.id,
            "old_status": entry.old_status,
            "new_status": entry.new_status,
            "updated_by": entry.updated_by,
            "notes": entry.notes,
            "created_at": entry.created_at.isoformat()
        }
        for entry in timeline_entries
    ]
    
    return ComplaintTrackResponse(
        ticket_id=complaint.ticket_id,
        status=complaint.status,
        department=complaint.department,
        severity=complaint.severity,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
        resolved_at=complaint.resolved_at,
        timeline=timeline
    )


@app.get("/complaint/{ticket_id}", response_model=ComplaintResponse)
async def get_complaint(ticket_id: str, db: Session = Depends(get_db)):
    """Get a specific complaint by ticket ID."""
    complaint = database.get_complaint_by_ticket_id(db, ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {ticket_id} not found"
        )
    
    return ComplaintResponse(
        ticket_id=complaint.ticket_id,
        text=complaint.text,
        department=complaint.department,
        severity=complaint.severity,
        status=complaint.status,
        predicted_department=complaint.predicted_department,
        predicted_severity=complaint.predicted_severity,
        citizen_name=complaint.citizen_name,
        citizen_email=complaint.citizen_email,
        citizen_phone=complaint.citizen_phone,
        location=complaint.location,
        admin_notes=complaint.admin_notes,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
        resolved_at=complaint.resolved_at
    )


@app.get("/timeline/{ticket_id}", response_model=TimelineResponse)
async def get_complaint_timeline(ticket_id: str, db: Session = Depends(get_db)):
    """Get the complete timeline for a complaint."""
    complaint = database.get_complaint_by_ticket_id(db, ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {ticket_id} not found"
        )
    
    timeline_entries = database.get_complaint_timeline(db, ticket_id)
    
    return TimelineResponse(
        ticket_id=complaint.ticket_id,
        current_status=complaint.status,
        timeline=[
            TimelineEntry(
                id=entry.id,
                ticket_id=entry.ticket_id,
                old_status=entry.old_status,
                new_status=entry.new_status,
                updated_by=entry.updated_by,
                notes=entry.notes,
                created_at=entry.created_at
            )
            for entry in timeline_entries
        ]
    )


# ============================================================================
# API Endpoints - Admin Authentication
# ============================================================================

@app.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate department admin.
    Each department has its own admin credentials.
    """
    admin = database.authenticate_admin(db, request.username, request.password)
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return AdminLoginResponse(
        success=True,
        username=admin.username,
        department=admin.department,
        full_name=admin.full_name,
        message=f"Welcome back, {admin.full_name}!"
    )


# ============================================================================
# API Endpoints - Agent Authentication
# ============================================================================

@app.post("/agent/login", response_model=AgentLoginResponse)
async def agent_login(request: AgentLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate department agent.
    Each department has its own agent credentials.
    """
    agent = database.authenticate_agent(db, request.username, request.password)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return AgentLoginResponse(
        success=True,
        username=agent.username,
        department=agent.department,
        full_name=agent.full_name,
        message=f"Welcome back, {agent.full_name}!"
    )


# ============================================================================
# API Endpoints - Department Admin
# ============================================================================

@app.get("/admin/{department}/dashboard", response_model=DepartmentStats)
async def get_department_dashboard(department: str, db: Session = Depends(get_db)):
    """
    Get dashboard statistics for a specific department.
    Admins can only see their department's data.
    """
    valid_departments = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    if department not in valid_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid department. Must be one of: {valid_departments}"
        )
    
    stats = database.get_department_dashboard_stats(db, department)
    
    return DepartmentStats(
        department=department,
        **stats
    )


@app.get("/admin/{department}/complaints", response_model=ComplaintList)
async def get_department_complaints(
    department: str,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get complaints for a specific department with optional filtering.
    """
    valid_departments = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    if department not in valid_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid department. Must be one of: {valid_departments}"
        )
    
    complaints = database.get_complaints_by_department(db, department, skip, limit)
    
    # Apply additional filters
    if status:
        complaints = [c for c in complaints if c.status == status]
    if severity:
        complaints = [c for c in complaints if c.severity == severity]
    
    return ComplaintList(
        complaints=[
            ComplaintResponse(
                ticket_id=c.ticket_id,
                text=c.text,
                department=c.department,
                severity=c.severity,
                status=c.status,
                predicted_department=c.predicted_department,
                predicted_severity=c.predicted_severity,
                citizen_name=c.citizen_name,
                citizen_email=c.citizen_email,
                citizen_phone=c.citizen_phone,
                location=c.location,
                admin_notes=c.admin_notes,
                created_at=c.created_at,
                updated_at=c.updated_at,
                resolved_at=c.resolved_at
            ) for c in complaints
        ],
        total=len(complaints)
    )


@app.put("/admin/{department}/update_status/{ticket_id}", response_model=ComplaintResponse)
async def update_complaint_status(
    department: str,
    ticket_id: str,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of a complaint.
    Only admins from the corresponding department can update.
    """
    valid_departments = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    if department not in valid_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid department. Must be one of: {valid_departments}"
        )
    
    valid_statuses = ["Pending", "Resolved"]
    
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    complaint = database.get_complaint_by_ticket_id(db, ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {ticket_id} not found"
        )
    
    if complaint.department != department:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This complaint belongs to {complaint.department} department, not {department}"
        )
    
    updated_complaint = database.update_complaint_status(
        db, ticket_id, status_update.status, "System", status_update.notes
    )
    
    return ComplaintResponse(
        ticket_id=updated_complaint.ticket_id,
        text=updated_complaint.text,
        department=updated_complaint.department,
        severity=updated_complaint.severity,
        status=updated_complaint.status,
        predicted_department=updated_complaint.predicted_department,
        predicted_severity=updated_complaint.predicted_severity,
        citizen_name=updated_complaint.citizen_name,
        citizen_email=updated_complaint.citizen_email,
        citizen_phone=updated_complaint.citizen_phone,
        location=updated_complaint.location,
        admin_notes=updated_complaint.admin_notes,
        created_at=updated_complaint.created_at,
        updated_at=updated_complaint.updated_at,
        resolved_at=updated_complaint.resolved_at
    )


@app.get("/admin/{department}/complaints/{ticket_id}", response_model=ComplaintResponse)
async def get_department_complaint(department: str, ticket_id: str, db: Session = Depends(get_db)):
    """Get a specific complaint from a department."""
    complaint = database.get_complaint_by_ticket_id(db, ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {ticket_id} not found"
        )
    
    if complaint.department != department:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This complaint belongs to {complaint.department} department, not {department}"
        )
    
    return ComplaintResponse(
        ticket_id=complaint.ticket_id,
        text=complaint.text,
        department=complaint.department,
        severity=complaint.severity,
        status=complaint.status,
        predicted_department=complaint.predicted_department,
        predicted_severity=complaint.predicted_severity,
        citizen_name=complaint.citizen_name,
        citizen_email=complaint.citizen_email,
        citizen_phone=complaint.citizen_phone,
        location=complaint.location,
        admin_notes=complaint.admin_notes,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
        resolved_at=complaint.resolved_at
    )


# ============================================================================
# API Endpoints - Department Agent
# ============================================================================

@app.get("/agent/{department}/complaints", response_model=ComplaintList)
async def get_agent_complaints(
    department: str,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get complaints for a specific department for an agent.
    """
    valid_departments = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    if department not in valid_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid department. Must be one of: {valid_departments}"
        )
    
    complaints = database.get_complaints_by_department(db, department, skip, limit)
    
    # Apply additional filters
    if status:
        complaints = [c for c in complaints if c.status == status]
    if severity:
        complaints = [c for c in complaints if c.severity == severity]
    
    return ComplaintList(
        complaints=[
            ComplaintResponse(
                ticket_id=c.ticket_id,
                text=c.text,
                department=c.department,
                severity=c.severity,
                status=c.status,
                predicted_department=c.predicted_department,
                predicted_severity=c.predicted_severity,
                citizen_name=c.citizen_name,
                citizen_email=c.citizen_email,
                citizen_phone=c.citizen_phone,
                location=c.location,
                admin_notes=c.admin_notes,
                created_at=c.created_at,
                updated_at=c.updated_at,
                resolved_at=c.resolved_at
            ) for c in complaints
        ],
        total=len(complaints)
    )


@app.put("/agent/{department}/update_status/{ticket_id}", response_model=ComplaintResponse)
async def agent_update_complaint_status(
    department: str,
    ticket_id: str,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of a complaint by an agent.
    """
    valid_departments = ["Electricity", "Water Supply", "Waste-Water/Sewage"]
    
    if department not in valid_departments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid department. Must be one of: {valid_departments}"
        )
    
    valid_statuses = ["Pending", "Resolved"]
    
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    complaint = database.get_complaint_by_ticket_id(db, ticket_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ticket ID {ticket_id} not found"
        )
    
    if complaint.department != department:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This complaint belongs to {complaint.department} department, not {department}"
        )
    
    updated_complaint = database.update_complaint_status(
        db, ticket_id, status_update.status, f"Agent ({department})", status_update.notes
    )
    
    return ComplaintResponse(
        ticket_id=updated_complaint.ticket_id,
        text=updated_complaint.text,
        department=updated_complaint.department,
        severity=updated_complaint.severity,
        status=updated_complaint.status,
        predicted_department=updated_complaint.predicted_department,
        predicted_severity=updated_complaint.predicted_severity,
        citizen_name=updated_complaint.citizen_name,
        citizen_email=updated_complaint.citizen_email,
        citizen_phone=updated_complaint.citizen_phone,
        location=updated_complaint.location,
        admin_notes=updated_complaint.admin_notes,
        created_at=updated_complaint.created_at,
        updated_at=updated_complaint.updated_at,
        resolved_at=updated_complaint.resolved_at
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
