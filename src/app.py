"""
ekajalakkam - Streamlit Frontend
Citizen Portal and Multi-Department Admin Dashboard for grievance management.
"""

import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = "http://localhost:8000"
DEFAULT_PASSWORD = "admin123"

st.set_page_config(
    page_title="ekajalakkam - Grievance Redressal System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# ============================================================================
# Helper Functions
# ============================================================================

def check_api_health() -> bool:
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def submit_complaint(data: dict) -> dict:
    """Submit a new complaint via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/submit_complaint",
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}


def track_complaint(ticket_id: str) -> dict:
    """Track complaint by ticket ID."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/track_complaint",
            json={"ticket_id": ticket_id},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}


def admin_login(username: str, password: str) -> dict:
    """Admin login."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Invalid credentials")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}


def get_department_dashboard(department: str) -> dict:
    """Get dashboard statistics for a department."""
    try:
        response = requests.get(f"{API_BASE_URL}/admin/{department}/dashboard", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except requests.exceptions.RequestException:
        return {}


def get_department_complaints(department: str, status: str = None, severity: str = None) -> dict:
    """Get complaints for a department."""
    try:
        params = {}
        if status:
            params["status"] = status
        if severity:
            params["severity"] = severity

        response = requests.get(
            f"{API_BASE_URL}/admin/{department}/complaints",
            params=params,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return {"complaints": [], "total": 0}
    except requests.exceptions.RequestException:
        return {"complaints": [], "total": 0}


def update_complaint_status(department: str, ticket_id: str, new_status: str, notes: str = None) -> dict:
    """Update complaint status."""
    try:
        payload = {"status": new_status}
        if notes:
            payload["notes"] = notes
            
        response = requests.put(
            f"{API_BASE_URL}/admin/{department}/update_status/{ticket_id}",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}


def get_complaint_timeline(ticket_id: str) -> dict:
    """Get timeline for a complaint."""
    try:
        response = requests.get(f"{API_BASE_URL}/timeline/{ticket_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}


def get_departments() -> list:
    """Get list of departments."""
    try:
        response = requests.get(f"{API_BASE_URL}/departments", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("departments", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_admin_credentials() -> dict:
    """Get default admin credentials."""
    try:
        response = requests.get(f"{API_BASE_URL}/admin/credentials", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except requests.exceptions.RequestException:
        return {}


def get_department_emoji(department: str) -> str:
    """Get emoji for department."""
    emojis = {
        "Electricity": "⚡",
        "Water Supply": "💧",
        "Waste-Water/Sewage": "🚽",
        "Billing & Accounts": "📄",
        "General": "📋"
    }
    return emojis.get(department, "📋")


def get_status_color(status: str) -> str:
    """Get color for status badge."""
    colors = {
        "Pending": "#fbbf24",
        "In Progress": "#60a5fa",
        "Resolved": "#6ee7b7",
        "Closed": "#d1d5db"
    }
    return colors.get(status, "#d1d5db")


# ============================================================================
# Professional Government Theme CSS
# ============================================================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    .stApp > header {display: none;}

    .stApp {
        background: #000000;
        min-height: 100vh;
        padding-top: 0.5rem !important;
    }

    .block-container {
        padding-top: 1rem !important;
    }

    .main-header {
        font-family: 'Playfair Display', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 0.25rem;
        letter-spacing: 2px;
    }

    .sub-header {
        font-family: 'Cormorant Garamond', sans-serif !important;
        font-size: 1.15rem;
        color: #e5e7eb;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .card {
        background: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #404040;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .section-header {
        font-family: 'Playfair Display', sans-serif !important;
        font-size: 1.35rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #404040;
    }

    .kpi-card {
        background: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #404040;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #06b6d4;
    }

    .kpi-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
        color: #06b6d4;
    }

    .kpi-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.7rem;
        color: #e5e7eb;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button {
        background: #06b6d4;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.5rem;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .stButton > button:hover {
        background: #0891b2;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: #1a1a1a;
        border: 1px solid #404040;
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #06b6d4;
        box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.3);
        outline: none;
        background: #1a1a1a;
    }

    label[data-testid*="stTextInput"],
    label[data-testid*="stTextArea"] {
        font-family: 'Inter', sans-serif !important;
        color: #e5e7eb;
    }

    .success-box {
        background: #164e63;
        border: 1px solid #06b6d4;
        border-radius: 8px;
        padding: 1rem;
        color: #67e8f9;
        margin: 1rem 0;
    }

    .error-box {
        background: #7f1d1d;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        color: #fca5a5;
        margin: 1rem 0;
    }

    .info-box {
        background: #1e3a5f;
        border: 1px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        color: #93c5fd;
        margin: 1rem 0;
    }

    .status-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-pending {
        background: #92400e;
        color: #fbbf24;
        border: 1px solid #f59e0b;
    }

    .status-in-progress {
        background: #1e40af;
        color: #60a5fa;
        border: 1px solid #3b82f6;
    }

    .status-resolved {
        background: #064e3b;
        color: #6ee7b7;
        border: 1px solid #10b981;
    }

    .status-closed {
        background: #374151;
        color: #d1d5db;
        border: 1px solid #6b7280;
    }

    .severity-high {
        background: #7f1d1d;
        color: #fca5a5;
        border: 1px solid #ef4444;
    }

    .severity-low {
        background: #164e63;
        color: #67e8f9;
        border: 1px solid #06b6d4;
    }

    .dept-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border: 1px solid #404040;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
    }

    .dept-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
    }

    .dept-card-selected {
        border-color: #06b6d4;
        box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.4), 0 4px 8px rgba(0, 0, 0, 0.5);
        transform: translateY(-2px);
    }

    .dept-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        background: #06b6d4;
        border: 2px solid #0891b2;
    }

    .dept-card strong {
        font-family: 'Inter', sans-serif !important;
        color: #ffffff;
        display: block;
        margin-bottom: 0.125rem;
    }

    .dept-card p {
        font-family: 'Inter', sans-serif !important;
        color: #e5e7eb;
        font-size: 0.8rem;
        margin: 0;
    }

    .custom-divider {
        height: 1px;
        background: #404040;
        margin: 1.5rem 0;
        border: none;
    }

    .ticket-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #404040;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
    }

    .ticket-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        transform: translateX(2px);
    }

    .ticket-id {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        color: #06b6d4;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }

    .timeline-item {
        display: flex;
        gap: 0.75rem;
        padding: 0.75rem 0;
        position: relative;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: 15px;
        top: 40px;
        bottom: -20px;
        width: 2px;
        background: #404040;
    }

    .timeline-item:last-child::before {
        display: none;
    }

    .timeline-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #06b6d4;
        border: 2px solid #0891b2;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        flex-shrink: 0;
    }

    .timeline-content {
        flex: 1;
    }

    .timeline-status {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }

    .timeline-date {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem;
        color: #e5e7eb;
    }

    .timeline-notes {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem;
        color: #e5e7eb;
        margin-top: 0.5rem;
        line-height: 1.6;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: #1a1a1a;
        border-radius: 8px;
        border: 1px solid #404040;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif !important;
        color: #e5e7eb;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #06b6d4;
        border-color: #06b6d4;
        color: #ffffff;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application entry point."""

    st.markdown('<h1 style="font-family: Playfair Display, sans-serif; font-size: 3.5rem !important; font-weight: 700; color: #ffffff; text-align: center; margin-top: -1rem; margin-bottom: 0.25rem; letter-spacing: 2px;">🏛️ ekajalakkam</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-family: Cormorant Garamond, sans-serif; font-size: 1.15rem; color: #e5e7eb; text-align: center; margin-bottom: 1.5rem; letter-spacing: 3px; text-transform: uppercase;">Public Grievance Analysis & Prioritization System</p>', unsafe_allow_html=True)

    # Check API health
    api_healthy = check_api_health()
    if not api_healthy:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Backend Offline</strong><br>
            The FastAPI server is not running on port 8000. Please start the backend service.
        </div>
        """, unsafe_allow_html=True)

    # Main navigation tabs
    main_tab1, main_tab2, main_tab3 = st.columns([1, 1, 1])
    
    with main_tab1:
        if st.button("📝 Submit Complaint", use_container_width=True, key="nav_submit"):
            st.session_state.current_page = "submit"
            st.rerun()
    
    with main_tab2:
        if st.button("🔍 Track Complaint", use_container_width=True, key="nav_track"):
            st.session_state.current_page = "track"
            st.rerun()
    
    with main_tab3:
        if st.button("👤 Admin Portal", use_container_width=True, key="nav_admin"):
            st.session_state.current_page = "admin"
            st.rerun()

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "submit"

    # Sidebar info
    st.sidebar.markdown("""
    <div style="padding: 1rem;">
        <h3 style="color: #ffffff; margin-bottom: 1rem; font-size: 1.1rem;">
            📖 About
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="card" style="padding: 1rem; margin: 0;">
        <p style="color: #e5e7eb; font-size: 0.9rem; line-height: 1.7; margin: 0;">
            <strong style="color: #ffffff;">ekajalakkam</strong> is an AI-powered grievance redressal system that automatically categorizes and routes complaints to the appropriate government department.
        </p>
        <hr class="custom-divider" style="margin: 1rem 0;">
        <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0;">
            <strong style="color: #ffffff;">Departments:</strong><br>
            ⚡ Electricity &nbsp; 💧 Water<br>
            🚽 Sewage &nbsp; 📄 Billing
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Route to appropriate page
    if st.session_state.current_page == "submit":
        submit_complaint_page()
    elif st.session_state.current_page == "track":
        track_complaint_page()
    elif st.session_state.current_page == "admin":
        admin_portal()


def submit_complaint_page():
    """Citizen Portal for submitting complaints."""
    
    api_healthy = check_api_health()

    if not api_healthy:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Service Unavailable</strong><br>
            Backend API is not running. Please start the FastAPI server on port 8000.
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
    <div class="card" style="margin-top: 1rem;">
        <h2 class="section-header">📝 Submit Your Grievance</h2>
        <p style="color: #e5e7eb; line-height: 1.8; margin-bottom: 0;">
            Report issues related to government utilities. Our AI system automatically
            categorizes and routes your complaint to the appropriate department for swift resolution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Department Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="dept-card">
            <div class="dept-icon">⚡</div>
            <div>
                <strong>Electricity</strong>
                <p>Power & lighting</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dept-card">
            <div class="dept-icon">💧</div>
            <div>
                <strong>Water Supply</strong>
                <p>Water distribution</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="dept-card">
            <div class="dept-icon">🚽</div>
            <div>
                <strong>Sewage</strong>
                <p>Drainage systems</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="dept-card">
            <div class="dept-icon">📄</div>
            <div>
                <strong>Billing</strong>
                <p>Accounts & billing</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)

    with st.form(key="complaint_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            citizen_name = st.text_input("Your Name", placeholder="John Doe")
            citizen_email = st.text_input("Email", placeholder="john@example.com")

        with col2:
            citizen_phone = st.text_input("Phone", placeholder="+91 9876543210")
            location = st.text_input("Location", placeholder="Area/Street name")

        complaint_text = st.text_area(
            label="Describe Your Issue *",
            placeholder="E.g., 'No water supply in our area for 2 days' or 'Electricity pole sparking dangerously near the main road. The wire is hanging low and children play in this area.'",
            help="Please provide detailed information including location, duration, and any safety concerns",
            height=180
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button(
                label="📤 Submit Complaint",
                use_container_width=True
            )

        if submit_button:
            if len(complaint_text.strip()) < 10:
                st.markdown("""
                <div class="error-box">
                    <strong>⚠️ More Details Needed</strong><br>
                    Please provide a description with at least 10 characters.
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.spinner("🤖 AI is analyzing your complaint..."):
                    result = submit_complaint({
                        "text": complaint_text,
                        "citizen_name": citizen_name if citizen_name else None,
                        "citizen_email": citizen_email if citizen_email else None,
                        "citizen_phone": citizen_phone if citizen_phone else None,
                        "location": location if location else None
                    })

                if "error" in result:
                    st.markdown(f"""
                    <div class="error-box">
                        <strong>❌ Submission Error</strong><br>
                        {result['error']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-box">
                        <h3 style="margin: 0 0 0.5rem 0; color: #ffffff;">✅ Ticket Registered Successfully!</h3>
                        <p style="margin: 0; color: #e5e7eb;">Your grievance has been submitted and will be addressed.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(f"""
                        <div class="ticket-card" style="text-align: center;">
                            <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Ticket ID</p>
                            <p class="ticket-id" style="margin: 0.75rem 0 0 0; font-size: 1.4rem;">{result.get('ticket_id', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        dept_emoji = get_department_emoji(result.get("department", ""))
                        st.markdown(f"""
                        <div class="ticket-card" style="text-align: center;">
                            <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Department</p>
                            <p style="font-size: 1.3rem; font-weight: 600; color: #ffffff; margin: 0.75rem 0 0 0;">
                                {dept_emoji} {result.get('department', 'N/A')}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        severity = result.get('severity', 'N/A')
                        severity_class = 'severity-high' if severity == 'High' else 'severity-low'
                        severity_emoji = "🔴" if severity == 'High' else "🟢"
                        st.markdown(f"""
                        <div class="ticket-card" style="text-align: center;">
                            <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Priority</p>
                            <span class="status-badge {severity_class}" style="margin-top: 0.5rem; font-size: 0.9rem;">
                                {severity_emoji} {severity}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="info-box">
                        <strong style="color: #e5e7eb;">📊 AI Analysis Complete</strong><br>
                        <span style="color: #ffffff;">
                        Your complaint has been automatically categorized:<br><br>
                        <strong>• Department:</strong> {result.get('predicted_department', 'N/A')}<br>
                        <strong>• Severity:</strong> {result.get('predicted_severity', 'N/A')}<br><br>
                        <em style="color: #e5e7eb;">Save your Ticket ID to track status online.</em>
                        </span>
                    </div>
                    """, unsafe_allow_html=True)


def track_complaint_page():
    """Track complaint status page."""

    api_healthy = check_api_health()

    if not api_healthy:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Service Unavailable</strong><br>
            Backend API is not running.
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
    <div class="card">
        <h2 class="section-header">🔍 Track Your Complaint</h2>
        <p style="color: #e5e7eb; line-height: 1.8; margin-bottom: 0;">
            Enter your Ticket ID to check the current status and view the complete timeline of your grievance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Track form
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        ticket_id = st.text_input(
            "Enter Ticket ID",
            placeholder="E.g., EKJ-10000",
            label_visibility="collapsed"
        )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        track_button = st.button("🔍 Track Status", use_container_width=True)

    if track_button:
        if not ticket_id.strip():
            st.markdown("""
            <div class="error-box">
                <strong>⚠️ Ticket ID Required</strong><br>
                Please enter your Ticket ID to track the complaint.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Fetching complaint status..."):
                result = track_complaint(ticket_id.strip())

            if "error" in result:
                st.markdown(f"""
                <div class="error-box">
                    <strong>❌ Not Found</strong><br>
                    {result['error']}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display complaint status
                st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

                # Status header
                dept_emoji = get_department_emoji(result.get("department", ""))

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"""
                    <div class="ticket-card" style="text-align: center;">
                        <p style="color: #e5e7eb; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Ticket ID</p>
                        <p class="ticket-id" style="margin: 0.5rem 0 0 0;">{result.get('ticket_id', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    status = result.get('status', 'Unknown')
                    status_class = f'status-{status.lower().replace(" ", "-")}'
                    st.markdown(f"""
                    <div class="ticket-card" style="text-align: center;">
                        <p style="color: #e5e7eb; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Status</p>
                        <span class="status-badge {status_class}" style="margin-top: 0.5rem; display: inline-block;">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="ticket-card" style="text-align: center;">
                        <p style="color: #e5e7eb; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Department</p>
                        <p style="font-size: 1.1rem; font-weight: 600; color: #ffffff; margin: 0.5rem 0 0 0;">
                            {dept_emoji} {result.get('department', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    severity = result.get('severity', 'N/A')
                    severity_class = 'severity-high' if severity == 'High' else 'severity-low'
                    st.markdown(f"""
                    <div class="ticket-card" style="text-align: center;">
                        <p style="color: #e5e7eb; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Priority</p>
                        <span class="status-badge {severity_class}" style="margin-top: 0.5rem; display: inline-block;">{severity}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Timeline
                st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
                st.markdown("""
                <div class="card">
                    <h3 style="color: #ffffff; margin-bottom: 1rem;">
                        📅 Complaint Timeline
                    </h3>
                </div>
                """, unsafe_allow_html=True)

                timeline = result.get('timeline', [])
                if timeline and len(timeline) > 0:
                    for entry in timeline:
                        # Safely get timeline entry fields
                        new_status = entry.get('new_status', 'Unknown') if isinstance(entry, dict) else 'Unknown'
                        notes = entry.get('notes', '') if isinstance(entry, dict) else ''
                        updated_by = entry.get('updated_by', 'System') if isinstance(entry, dict) else 'System'

                        created_at = entry.get('created_at', '') if isinstance(entry, dict) else ''
                        if created_at:
                            try:
                                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                                formatted_date = dt.strftime('%b %d, %Y at %I:%M %p')
                            except:
                                formatted_date = created_at
                        else:
                            formatted_date = 'Unknown'

                        status_icon = "📝" if new_status == 'Pending' else \
                                      "🔄" if new_status == 'In Progress' else \
                                      "✅" if new_status == 'Resolved' else "🔒"

                        st.markdown(f"""
                        <div class="timeline-item">
                            <div class="timeline-icon">{status_icon}</div>
                            <div class="timeline-content">
                                <div class="timeline-status">{status_icon} Status: {new_status}</div>
                                <div class="timeline-date">{formatted_date}</div>
                                {f"<div class='timeline-notes'>📝 Notes: {notes}</div>" if notes else ''}
                                {f"<div class='timeline-date' style='font-size: 0.8rem;'>Updated by: {updated_by}</div>" if updated_by else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-box" style="text-align: center;">
                        <p style="color: #ffffff;">No timeline entries available yet. The complaint has just been registered.</p>
                    </div>
                    """, unsafe_allow_html=True)


def admin_portal():
    """Admin portal with department selection."""
    
    api_healthy = check_api_health()

    if not api_healthy:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Service Unavailable</strong><br>
            Backend API is not running.
        </div>
        """, unsafe_allow_html=True)
        return

    # Check if admin is logged in
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if st.session_state.admin_logged_in:
        department_admin_dashboard()
    else:
        admin_login_page()


def admin_login_page():
    """Admin login page with department selection."""
    
    st.markdown("""
    <div class="card" style="max-width: 700px; margin: 2rem auto;">
        <h2 class="section-header" style="justify-content: center;">🔐 Department Admin Login</h2>
        <p style="color: #e5e7eb; text-align: center; margin-bottom: 2rem; line-height: 1.6;">
            Select your department and enter your credentials to access the admin dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Department selection
    st.markdown("""
    <div class="card">
        <h3 style="color: #ffffff; margin-bottom: 1rem;">
            1️⃣ Select Your Department
        </h3>
    </div>
    """, unsafe_allow_html=True)

    departments = get_departments()
    if not departments:
        departments = ["Electricity", "Water Supply", "Waste-Water/Sewage", "Billing & Accounts"]

    # Display department cards for selection
    cols = st.columns(4)
    selected_department = None
    
    for i, dept in enumerate(departments):
        with cols[i % 4]:
            emoji = get_department_emoji(dept)
            if st.button(f"{emoji} {dept.split()[0]}", key=f"dept_select_{dept}", use_container_width=True):
                st.session_state.selected_department = dept
                selected_department = dept

    if selected_department or "selected_department" in st.session_state:
        dept = selected_department or st.session_state.selected_department
        
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3 style="color: #ffffff; margin-bottom: 1rem;">
                2️⃣ Enter Credentials
            </h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            login_button = st.button("🔓 Login to Dashboard", use_container_width=True)
            
            if login_button:
                if not username or not password:
                    st.markdown("""
                    <div class="error-box">
                        <strong>⚠️ Missing Credentials</strong><br>
                        Please enter both username and password.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    with st.spinner("Authenticating..."):
                        result = admin_login(username, password)

                    if "error" in result:
                        st.markdown("""
                        <div class="error-box">
                            <strong>❌ Login Failed</strong><br>
                            Invalid username or password.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.session_state.admin_logged_in = True
                        st.session_state.admin_username = result.get('username', '')
                        st.session_state.admin_department = result.get('department', '')
                        st.session_state.admin_name = result.get('full_name', '')
                        st.markdown("""
                        <div class="success-box">
                            <strong>✅ Login Successful!</strong><br>
                            Redirecting to dashboard...
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()

        # Show credentials help (collapsible)
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        with st.expander("📋 Need Login Credentials? (Click to expand)", expanded=False):
            creds = get_admin_credentials()
            if creds:
                st.markdown("""
                <div style="color: #ffffff; padding: 1rem;">
                Use these credentials for testing (password: <strong style="color: #e5e7eb;">admin123</strong> for all):<br><br>
                """, unsafe_allow_html=True)

                for dept, info in creds.get('departments', {}).items():
                    emoji = get_department_emoji(dept)
                    st.markdown(f"{emoji} **{dept}:** Username: `{info['username']}`")

                st.markdown("</div>", unsafe_allow_html=True)


def department_admin_dashboard():
    """Department-specific admin dashboard."""
    
    department = st.session_state.get('admin_department', 'Electricity')
    admin_name = st.session_state.get('admin_name', 'Admin')
    
    # Sidebar logout
    st.sidebar.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.session_state.selected_department = None
        st.rerun()

    dept_emoji = get_department_emoji(department)
    
    # Header
    st.markdown(f"""
    <div class="card">
        <h2 class="section-header">{dept_emoji} {department} Dashboard</h2>
        <p style="color: #e5e7eb; margin: 0;">Welcome back, <strong style="color: #ffffff;">{admin_name}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch dashboard stats
    stats = get_department_dashboard(department)

    if not stats:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Unable to load dashboard data.</strong>
        </div>
        """, unsafe_allow_html=True)
        return

    # KPI Cards
    st.markdown('<h2 class="section-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-indigo">
            <div class="kpi-value">{stats.get('total_complaints', 0)}</div>
            <div class="kpi-label">Total Complaints</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-rose">
            <div class="kpi-value">{stats.get('high_severity_count', 0)}</div>
            <div class="kpi-label">High Priority</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-amber">
            <div class="kpi-value">{stats.get('pending_count', 0)}</div>
            <div class="kpi-label">Pending</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-card-emerald">
            <div class="kpi-value">{stats.get('resolved_count', 0)}</div>
            <div class="kpi-label">Resolved</div>
        </div>
        """, unsafe_allow_html=True)

    # Additional stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="ticket-card" style="text-align: center;">
            <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0;">Recent (7 days)</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">{stats.get('recent_complaints', 0)}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_hours = stats.get('avg_resolution_hours', 0)
        st.markdown(f"""
        <div class="ticket-card" style="text-align: center;">
            <p style="color: #e5e7eb; font-size: 0.85rem; margin: 0;">Avg. Resolution Time</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">{avg_hours} hrs</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Charts
    st.markdown('<h2 class="section-header">📈 Analytics</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        by_severity = stats.get('by_severity', {})
        if by_severity:
            df_sev = pd.DataFrame({
                'Severity': list(by_severity.keys()),
                'Count': list(by_severity.values())
            })
            fig_sev = px.pie(
                df_sev,
                names='Severity',
                values='Count',
                title='Complaints by Severity',
                color='Severity',
                color_discrete_map={'High': '#f43f5e', 'Low': '#06b6d4'}
            )
            fig_sev.update_layout(
                height=300,
                font=dict(family='Inter, sans-serif', size=12, color='#e5e7eb'),
                title_font=dict(family='Playfair Display, sans-serif', size=14, color='#ffffff'),
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a'
            )
            st.plotly_chart(fig_sev, use_container_width=True)

    with col2:
        by_status = stats.get('by_status', {})
        if by_status:
            df_status = pd.DataFrame({
                'Status': list(by_status.keys()),
                'Count': list(by_status.values())
            })
            fig_status = px.bar(
                df_status,
                x='Status',
                y='Count',
                title='Complaints by Status',
                color='Status',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_status.update_layout(
                height=300,
                showlegend=False,
                font=dict(family='Inter, sans-serif', size=12, color='#e5e7eb'),
                title_font=dict(family='Playfair Display, sans-serif', size=14, color='#ffffff'),
                margin=dict(l=40, r=20, t=40, b=40),
                paper_bgcolor='#1a1a1a',
                plot_bgcolor='#1a1a1a',
                xaxis=dict(showgrid=True, gridcolor='#404040'),
                yaxis=dict(showgrid=True, gridcolor='#404040')
            )
            st.plotly_chart(fig_status, use_container_width=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Complaints Management
    st.markdown('<h2 class="section-header">📋 Complaint Management</h2>', unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Progress", "Resolved", "Closed"],
            key="status_filter"
        )
    with col2:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "High", "Low"],
            key="severity_filter"
        )

    status_param = None if status_filter == "All" else status_filter
    severity_param = None if severity_filter == "All" else severity_filter

    complaints_data = get_department_complaints(department, status_param, severity_param)
    complaints = complaints_data.get('complaints', [])

    if complaints:
        df_complaints = pd.DataFrame(complaints)
        df_complaints['created_at'] = pd.to_datetime(df_complaints['created_at']).dt.strftime('%Y-%m-%d %H:%M')

        st.dataframe(
            df_complaints[['ticket_id', 'text', 'severity', 'status', 'created_at']],
            use_container_width=True,
            height=300,
            hide_index=True
        )

        # Update status section
        st.markdown("""
        <div class="card">
            <h3 style="color: #ffffff; margin-bottom: 1rem;">
                🔧 Update Complaint Status
            </h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            ticket_to_update = st.selectbox(
                "Select Ticket",
                options=[c['ticket_id'] for c in complaints],
                format_func=lambda x: f"{x}",
                key="ticket_select"
            )
        with col2:
            new_status = st.selectbox(
                "New Status",
                options=["Pending", "In Progress", "Resolved", "Closed"],
                key="status_select"
            )
        with col3:
            if st.button("Update", use_container_width=True, key="update_btn"):
                result = update_complaint_status(department, ticket_to_update, new_status)
                if "error" in result:
                    st.markdown(f"""
                    <div class="error-box">
                        <strong>❌ Update Failed</strong><br>
                        {result['error']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ Updated!</strong> Ticket {ticket_to_update} → {new_status}
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
        with col4:
            if st.button("📅 View Timeline", use_container_width=True, key="view_timeline"):
                st.session_state.view_timeline_ticket = ticket_to_update
                st.session_state.show_timeline_modal = True

        # Timeline modal
        if st.session_state.get('show_timeline_modal', False):
            ticket_id = st.session_state.get('view_timeline_ticket', '')
            timeline_data = get_complaint_timeline(ticket_id)
            
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
                <h3 style="color: #ffffff; margin-bottom: 1rem;">
                    📅 Timeline for {ticket_id}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            if "error" not in timeline_data:
                timeline = timeline_data.get('timeline', [])
                for entry in timeline:
                    created_at = entry.get('created_at', '')
                    if created_at:
                        try:
                            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            formatted_date = dt.strftime('%b %d, %Y at %I:%M %p')
                        except:
                            formatted_date = created_at
                    else:
                        formatted_date = 'Unknown'

                    status_icon = "📝" if entry.get('new_status') == 'Pending' else \
                                  "🔄" if entry.get('new_status') == 'In Progress' else \
                                  "✅" if entry.get('new_status') == 'Resolved' else "🔒"

                    st.markdown(f"""
                    <div class="timeline-item">
                        <div class="timeline-icon">{status_icon}</div>
                        <div class="timeline-content">
                            <div class="timeline-status">{status_icon} {entry.get('new_status', 'Unknown')}</div>
                            <div class="timeline-date">{formatted_date}</div>
                            {f"<div class='timeline-notes'>📝 {entry.get('notes', '')}</div>" if entry.get('notes') else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("Close Timeline", key="close_timeline"):
                st.session_state.show_timeline_modal = False
                st.rerun()
    else:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 4rem 2rem;">
            <p style="font-size: 3rem; margin-bottom: 1rem;">📭</p>
            <h3 style="color: #ffffff; margin-bottom: 0.5rem;">No Complaints Found</h3>
            <p style="color: #e5e7eb; margin: 0;">No complaints match the selected filters.</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
