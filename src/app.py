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

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Ekajalakkam - Grievance Redressal System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# ============================================================================
# Glassmorphism CSS Styles
# ============================================================================

GLASS_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Vibrant Mesh Gradient Background */
.stApp {
    background-color: #030014 !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(76, 29, 149, 0.4) 0px, transparent 50%),
        radial-gradient(at 50% 0%, rgba(30, 58, 138, 0.4) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(134, 25, 143, 0.4) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(134, 25, 143, 0.4) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(30, 58, 138, 0.4) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(76, 29, 149, 0.4) 0px, transparent 50%) !important;
    background-attachment: fixed !important;
}

/* High-End Glass Cards */
.glass-card, .kpi-card, .ticket-card, .dept-card {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 2rem !important;
    margin: 1rem 0 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.glass-card:hover, .kpi-card:hover, .ticket-card:hover, .dept-card:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    transform: translateY(-5px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* High-Contrast Gradient Typography */
.main-header {
    font-family: 'Poppins', sans-serif !important;
    font-size: 6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #FF00FF 0%, #7000FF 30%, #00FFFF 70%, #FF00FF 100%) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    letter-spacing: -2px !important;
    line-height: 1.2 !important;
    margin: 4rem 0 2rem 0 !important;
    display: block !important;
}

.sub-header {
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.4rem !important;
    background: linear-gradient(90deg, #00FFFF, #FF00FF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-weight: 600 !important;
    letter-spacing: 8px !important;
    text-transform: uppercase !important;
    margin-top: -1.5rem !important;
    margin-bottom: 4rem !important;
    display: block !important;
}

.section-header {
    font-family: 'Poppins', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #FFFFFF, #94a3b8) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 1.5rem !important;
}

/* Interactive Elements */
.stButton > button {
    background: linear-gradient(90deg, #7000FF 0%, #FF00FF 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    box-shadow: 0 4px 15px rgba(112, 0, 255, 0.3) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(255, 0, 255, 0.5) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
    backdrop-filter: blur(5px) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border: 1px solid #FF00FF !important;
    box-shadow: 0 0 15px rgba(255, 0, 255, 0.2) !important;
    background: rgba(255, 255, 255, 0.07) !important;
}

/* KPI specifics */
.kpi-value {
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #94a3b8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.kpi-label {
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    font-size: 0.9rem !important;
    letter-spacing: 3px !important;
    font-weight: 600 !important;
}

/* Status Badges */
.status-badge {
    padding: 8px 16px !important;
    border-radius: 100px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    backdrop-filter: blur(10px) !important;
    display: inline-block !important;
}

.status-pending { background: rgba(245, 158, 11, 0.15) !important; color: #fbbf24 !important; border: 1px solid rgba(245, 158, 11, 0.3) !important; }
.status-resolved { background: rgba(16, 185, 129, 0.15) !important; color: #34d399 !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; }

.severity-high { 
    background: rgba(244, 63, 94, 0.2) !important; 
    color: #fb7185 !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
}
.severity-low { 
    background: rgba(16, 185, 129, 0.2) !important; 
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
}

/* Ticket Details */
.ticket-id {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #00FFFF, #7000FF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 1.5rem !important;
}

/* Department Cards */
.dept-icon {
    font-size: 2.5rem !important;
    margin-bottom: 1rem !important;
}

/* Timeline */
.timeline-item {
    display: flex !important;
    margin-bottom: 1.5rem !important;
    position: relative !important;
}

.timeline-icon {
    min-width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    background: rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-right: 1.5rem !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.timeline-content {
    background: rgba(255, 255, 255, 0.03) !important;
    padding: 1.2rem !important;
    border-radius: 16px !important;
    flex-grow: 1 !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.timeline-status {
    font-weight: 700 !important;
    color: #FFFFFF !important;
    margin-bottom: 0.2rem !important;
}

.timeline-date {
    font-size: 0.8rem !important;
    color: #94a3b8 !important;
    margin-bottom: 0.8rem !important;
}

.timeline-notes {
    color: #cbd5e1 !important;
    font-size: 0.95rem !important;
    font-style: italic !important;
}

/* Boxes */
.success-box, .error-box, .info-box {
    padding: 1.5rem !important;
    border-radius: 16px !important;
    margin: 1.5rem 0 !important;
    backdrop-filter: blur(10px) !important;
}

.success-box { background: rgba(16, 185, 129, 0.1) !important; border: 1px solid rgba(16, 185, 129, 0.2) !important; }
.error-box { background: rgba(244, 63, 94, 0.1) !important; border: 1px solid rgba(244, 63, 94, 0.2) !important; }
.info-box { background: rgba(59, 130, 246, 0.1) !important; border: 1px solid rgba(59, 130, 246, 0.2) !important; }

/* Divider */
.custom-divider {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
    margin: 3rem 0 !important;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.fade-in-up {
    animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(GLASS_CSS, unsafe_allow_html=True)

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


def agent_login(username: str, password: str) -> dict:
    """Agent login."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/agent/login",
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


def get_agent_complaints(department: str, status: str = None, severity: str = None) -> dict:
    """Get complaints for a department (Agent view)."""
    try:
        params = {}
        if status:
            params["status"] = status
        if severity:
            params["severity"] = severity

        response = requests.get(
            f"{API_BASE_URL}/agent/{department}/complaints",
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


def agent_update_complaint_status(department: str, ticket_id: str, new_status: str, notes: str = None) -> dict:
    """Update complaint status by Agent."""
    try:
        payload = {"status": new_status}
        if notes:
            payload["notes"] = notes
            
        response = requests.put(
            f"{API_BASE_URL}/agent/{department}/update_status/{ticket_id}",
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


def get_department_emoji(department: str) -> str:
    """Get emoji for department."""
    emojis = {
        "Electricity": "⚡",
        "Water Supply": "💧",
        "Waste-Water/Sewage": "🚽",
        "General": "📋"
    }
    return emojis.get(department, "📋")


def get_status_color(status: str) -> str:
    """Get color for status badge."""
    colors = {
        "Pending": "#f59e0b",
        "Resolved": "#10b981"
    }
    return colors.get(status, "#6b7280")


# ============================================================================
# Main Application
# ============================================================================

def main():
    st.markdown('<div class="main-header">Ekajalakkam</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Integrated Public Grievance Redressal Portal</div>', unsafe_allow_html=True)

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "submit"

    main_tab1, main_tab2, main_tab3, main_tab4 = st.columns([1, 1, 1, 1])
    
    # Set page based on which tab is clicked
    with main_tab1:
        clicked1 = st.button("📝 Submit Complaint", width='stretch', key="nav_submit")
        if clicked1:
            st.session_state.current_page = "submit"
    
    with main_tab2:
        clicked2 = st.button("🔍 Track Complaint", width='stretch', key="nav_track")
        if clicked2:
            st.session_state.current_page = "track"
    
    with main_tab3:
        clicked3 = st.button("👤 Admin Portal", width='stretch', key="nav_admin")
        if clicked3:
            st.session_state.current_page = "admin"

    with main_tab4:
        clicked4 = st.button("👷 Agent Portal", width='stretch', key="nav_agent")
        if clicked4:
            st.session_state.current_page = "agent"

    # Route to appropriate page
    if st.session_state.current_page == "submit":
        submit_complaint_page()
    elif st.session_state.current_page == "track":
        track_complaint_page()
    elif st.session_state.current_page == "admin":
        admin_portal()
    elif st.session_state.current_page == "agent":
        agent_portal()


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
    <div class="glass-card fade-in-up">
        <h2 class="section-header">📝 Submit Your Grievance</h2>
        <p style="color: #94a3b8; line-height: 1.8; margin-bottom: 0;">
            Report issues related to government utilities. Our AI system automatically 
            categorizes and routes your complaint to the appropriate department for swift resolution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Department Cards
    col1, col2, col3 = st.columns(3)
    
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
    
    # Complaint Form
    st.markdown("""
    <div class="glass-card">
        <h3 style="font-family: 'Poppins', sans-serif; color: #e0e7ff; margin-bottom: 1rem;">
            📋 Complaint Details
        </h3>
    </div>
    """, unsafe_allow_html=True)

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
                width='stretch'
            )

        if submit_button:
            errors = []

            if len(complaint_text.strip()) < 10:
                errors.append("Please provide a complaint description with at least 10 characters.")
            
            if citizen_phone and len(citizen_phone.replace(" ", "").replace("-", "")) != 10:
                errors.append("Phone number must have exactly 10 digits.")
            
            if citizen_email and "@gmail.com" not in citizen_email.lower():
                errors.append("Please enter a valid Gmail address ending with @gmail.com")
            
            if errors:
                error_msg = "⚠️ Please fix the following:<br>" + "<br>".join(f"• {e}" for e in errors)
                st.markdown(f"""
                <div class="error-box">
                    <strong>{error_msg}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                placeholder = st.empty()
                with placeholder.container():
                    st.markdown("""
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <h3 style="color: #e0e7ff; font-family: 'Poppins', sans-serif;">🤖 Analyzing with AI...</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                    <div class="skeleton-card" style="padding: 2rem;">
                        <div class="skeleton-text skeleton-title"></div>
                        <div style="margin-top: 2rem;">
                            <div class="skeleton-text skeleton-line-1"></div>
                            <div class="skeleton-text skeleton-line-2"></div>
                            <div class="skeleton-text skeleton-line-3"></div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                        <div class="skeleton-card" style="flex: 1; height: 120px;"></div>
                        <div class="skeleton-card" style="flex: 1; height: 120px;"></div>
                        <div class="skeleton-card" style="flex: 1; height: 120px;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                result = submit_complaint({
                    "text": complaint_text,
                    "citizen_name": citizen_name if citizen_name else None,
                    "citizen_email": citizen_email if citizen_email else None,
                    "citizen_phone": citizen_phone if citizen_phone else None,
                    "location": location if location else None
                })
                
                placeholder.empty()

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
                        <h3 style="margin: 0 0 0.5rem 0; color: #6ee7b7;">✅ Ticket Registered Successfully!</h3>
                        <p style="margin: 0; color: #a7f3d0;">Your grievance has been submitted and will be addressed.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(f"""
                        <div class="ticket-card" style="text-align: center;">
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Ticket ID</p>
                            <p class="ticket-id" style="margin: 0.75rem 0 0 0; font-size: 1.4rem;">{result.get('ticket_id', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        dept_emoji = get_department_emoji(result.get("department", ""))
                        st.markdown(f"""
                        <div class="ticket-card" style="text-align: center;">
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Department</p>
                            <p style="font-size: 1.3rem; font-weight: 600; color: #e0e7ff; margin: 0.75rem 0 0 0;">
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
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Priority</p>
                            <span class="status-badge {severity_class}" style="margin-top: 0.5rem; font-size: 0.9rem;">
                                {severity_emoji} {severity}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="info-box">
                        <strong style="color: #93c5fd;">📊 AI Analysis Complete</strong><br>
                        <span style="color: #cbd5e1;">
                        Your complaint has been automatically categorized:<br><br>
                        <strong>• Department:</strong> {result.get('predicted_department', 'N/A')}<br>
                        <strong>• Severity:</strong> {result.get('predicted_severity', 'N/A')}<br><br>
                        <em style="color: #94a3b8;">Save your Ticket ID to track status online.</em>
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

    # Initialize tracking state
    if "tracking_result" not in st.session_state:
        st.session_state.tracking_result = None

    # Only show search form if no result yet
    if st.session_state.tracking_result is None:
        st.markdown("""
        <div class="glass-card fade-in-up">
            <h2 class="section-header">🔍 Track Your Complaint</h2>
            <p style="color: #94a3b8; line-height: 1.8; margin-bottom: 0;">
                Enter your Ticket ID to check the current status and view the complete timeline of your grievance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            ticket_id = st.text_input(
                "Enter Ticket ID",
                placeholder="E.g., EKJ-10000",
                label_visibility="collapsed"
            )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            track_button = st.button("🔍 Track Status", width='stretch')

        if track_button:
            if not ticket_id.strip():
                st.markdown("""
                <div class="error-box">
                    <strong>⚠️ Ticket ID Required</strong><br>
                    Please enter your Ticket ID to track the complaint.
                </div>
                """, unsafe_allow_html=True)
            else:
                result = track_complaint(ticket_id.strip())
                if "error" in result:
                    st.markdown(f"""
                    <div class="error-box">
                        <strong>❌ Not Found</strong><br>
                        {result['error']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.tracking_result = result
                    st.rerun()

    # Display results
    result = st.session_state.tracking_result
    if result:
        # Clear button - centered
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("← Track Another Complaint", width='stretch'):
                st.session_state.tracking_result = None
                st.rerun()

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

        dept_emoji = get_department_emoji(result.get("department", ""))

        # Equal sized columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="ticket-card" style="text-align: center; height: 100%;">
                <p style="color: #94a3b8; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Ticket ID</p>
                <p class="ticket-id" style="margin: 0.5rem 0 0 0;">{result.get('ticket_id', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            status = result.get('status', 'Unknown')
            status_class = f'status-{status.lower().replace(" ", "-")}'
            st.markdown(f"""
            <div class="ticket-card" style="text-align: center; height: 100%;">
                <p style="color: #94a3b8; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Status</p>
                <span class="status-badge {status_class}" style="margin-top: 0.5rem; display: inline-block;">{status}</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="ticket-card" style="text-align: center; height: 100%;">
                <p style="color: #94a3b8; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Department</p>
                <p style="font-size: 1.1rem; font-weight: 600; color: #e0e7ff; margin: 0.5rem 0 0 0;">
                    {dept_emoji} {result.get('department', 'N/A')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            severity = result.get('severity', 'N/A')
            severity_class = 'severity-high' if severity == 'High' else 'severity-low'
            st.markdown(f"""
            <div class="ticket-card" style="text-align: center; height: 100%;">
                <p style="color: #94a3b8; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Priority</p>
                <span class="status-badge {severity_class}" style="margin-top: 0.5rem; display: inline-block;">{severity}</span>
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


def agent_portal():
    """Agent portal with department selection."""
    
    api_healthy = check_api_health()

    if not api_healthy:
        st.markdown("""
        <div class="error-box">
            <strong>⚠️ Service Unavailable</strong><br>
            Backend API is not running.
        </div>
        """, unsafe_allow_html=True)
        return

    # Check if agent is logged in
    if "agent_logged_in" not in st.session_state:
        st.session_state.agent_logged_in = False

    if st.session_state.agent_logged_in:
        department_agent_dashboard()
    else:
        agent_login_page()


def agent_login_page():
    """Agent login page."""

    st.markdown("""
    <div style="max-width: 400px; margin: 3rem auto;">
        <div class="glass-card" style="text-align: center;">
            <h2 class="section-header">👷 Agent Login</h2>
            <p style="color: #94a3b8; margin-bottom: 1.5rem;">
                Enter your credentials to access the field agent portal.
            </p>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your agent username", key="agent_user")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="agent_pass")

    login_button = st.button("🔓 Login", width='stretch', key="agent_login_btn")

    if login_button:
        if not username or not password:
            st.markdown("""
            <div class="error-box" style="margin-top: 1rem;">
                <strong>⚠️ Missing Credentials</strong><br>
                Please enter both username and password.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Logging in..."):
                result = agent_login(username, password)

            if "error" in result:
                st.markdown("""
                <div class="error-box">
                    <strong>❌ Login Failed</strong><br>
                    Invalid username or password.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.agent_logged_in = True
                st.session_state.agent_username = result.get('username', '')
                st.session_state.agent_department = result.get('department', '')
                st.session_state.agent_name = result.get('full_name', '')
                st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


def department_agent_dashboard():
    """Department-specific agent dashboard."""
    
    department = st.session_state.get('agent_department', 'Electricity')
    agent_name = st.session_state.get('agent_name', 'Agent')
    
    dept_emoji = get_department_emoji(department)
    
    # Logout button in header
    st.markdown(f"""
    <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem;">
        <div>
            <h2 class="section-header" style="margin: 0;">{dept_emoji} {department} Agent Portal</h2>
            <p style="color: #94a3b8; margin: 0;">Field Agent: <strong style="color: #e0e7ff;">{agent_name}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", width='content', key="agent_logout"):
        st.session_state.agent_logged_in = False
        st.rerun()
    
    st.markdown('<h2 class="section-header">📋 Assigned Complaints</h2>', unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
["All", "Pending", "Resolved"],
                key="agent_status_filter"
        )
    with col2:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "High", "Low"],
            key="agent_severity_filter"
        )

    status_param = None if status_filter == "All" else status_filter
    severity_param = None if severity_filter == "All" else severity_filter

    complaints_data = get_agent_complaints(department, status_param, severity_param)
    complaints = complaints_data.get('complaints', [])

    if complaints:
        # Display as a searchable table
        df_complaints = pd.DataFrame(complaints)
        df_complaints['created_at'] = pd.to_datetime(df_complaints['created_at']).dt.strftime('%Y-%m-%d %H:%M')

        st.dataframe(
            df_complaints[['ticket_id', 'text', 'severity', 'status', 'location', 'created_at']],
            width='stretch',
            height=400,
            hide_index=True
        )

        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
        
        # Action area
        st.markdown("""
        <div class="glass-card">
            <h3 style="font-family: 'Poppins', sans-serif; color: #e0e7ff; margin-bottom: 1rem;">
                🔄 Update Resolution Progress
            </h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ticket_to_update = st.selectbox(
                "Select Ticket ID",
                options=[c['ticket_id'] for c in complaints],
                key="agent_ticket_select"
            )
            
            # Show details of selected ticket
            selected_c = next((c for c in complaints if c['ticket_id'] == ticket_to_update), None)
            if selected_c:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">COMPLAINT TEXT</p>
                    <p style="color: #e0e7ff; margin: 0.5rem 0;">{selected_c['text']}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.5rem 0 0 0;">LOCATION</p>
                    <p style="color: #e0e7ff; margin: 0.2rem 0;">📍 {selected_c.get('location', 'Not specified')}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            new_status = st.selectbox(
                "Update Status To",
                options=["Pending", "Resolved"],
                key="agent_status_select"
            )
            update_notes = st.text_area("Resolution Notes", placeholder="Describe the action taken...", key="agent_notes")
            
            if st.button("Submit Update", width='stretch', key="agent_update_btn"):
                with st.spinner("Updating..."):
                    result = agent_update_complaint_status(department, ticket_to_update, new_status, update_notes)
                
                if "error" in result:
                    st.error(f"Failed to update: {result['error']}")
                else:
                    st.success(f"Ticket {ticket_to_update} updated to {new_status}!")
                    st.rerun()
    else:
        st.info("No complaints found for your department with current filters.")


def admin_login_page():
    """Admin login page - just username and password (department is auto-detected)."""

    # Single centered login card
    st.markdown("""
    <div style="max-width: 400px; margin: 3rem auto;">
        <div class="glass-card" style="text-align: center;">
            <h2 class="section-header">🔐 Admin Login</h2>
            <p style="color: #94a3b8; margin-bottom: 1.5rem;">
                Enter your credentials to access the admin dashboard.
            </p>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="admin_pass")

    login_button = st.button("🔓 Login", width='stretch')

    if login_button:
        if not username or not password:
            st.markdown("""
            <div class="error-box" style="margin-top: 1rem;">
                <strong>⚠️ Missing Credentials</strong><br>
                Please enter both username and password.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Loading..."):
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
                st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


def department_admin_dashboard():
    """Department-specific admin dashboard."""
    
    department = st.session_state.get('admin_department', 'Electricity')
    admin_name = st.session_state.get('admin_name', 'Admin')
    
    dept_emoji = get_department_emoji(department)
    
    # Logout button in header
    st.markdown(f"""
    <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem;">
        <div>
            <h2 class="section-header" style="margin: 0;">{dept_emoji} {department} Dashboard</h2>
            <p style="color: #94a3b8; margin: 0;">Welcome back, <strong style="color: #e0e7ff;">{admin_name}</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Logout", width='content'):
        st.session_state.admin_logged_in = False
        st.session_state.selected_department = None
        st.rerun()
    
    # Fetch dashboard stats with loading
    with st.spinner("Loading..."):
        stats = get_department_dashboard(department)

    if not stats:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div class="custom-loader"></div>
            <p class="loading-text">Loading dashboard data...</p>
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
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Recent (7 days)</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #e0e7ff; margin: 0.5rem 0;">{stats.get('recent_complaints', 0)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_hours = stats.get('avg_resolution_hours', 0)
        st.markdown(f"""
        <div class="ticket-card" style="text-align: center;">
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">Avg. Resolution Time</p>
            <p style="font-size: 1.5rem; font-weight: 700; color: #e0e7ff; margin: 0.5rem 0;">{avg_hours} hrs</p>
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
                color_discrete_map={'High': '#f43f5e', 'Low': '#10b981'}
            )
            fig_sev.update_layout(
                height=300,
                font=dict(family='Inter', size=12, color='#cbd5e1'),
                title_font=dict(family='Poppins', size=14, color='#e0e7ff'),
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_sev, width='stretch')

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
                font=dict(family='Inter', size=12, color='#cbd5e1'),
                title_font=dict(family='Poppins', size=14, color='#e0e7ff'),
                margin=dict(l=40, r=20, t=40, b=40),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig_status, width='stretch')

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Complaints Management
    st.markdown('<h2 class="section-header">📋 Complaint Management</h2>', unsafe_allow_html=True)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Resolved"],
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
            width='stretch',
            height=300,
            hide_index=True
        )

        # Update status section
        st.markdown("""
        <div class="glass-card">
            <h3 style="font-family: 'Poppins', sans-serif; color: #e0e7ff; margin-bottom: 1rem;">
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
                options=["Pending", "Resolved"],
                key="status_select"
            )
        with col3:
            if st.button("Update", width='stretch', key="update_btn"):
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
            if st.button("📅 View Timeline", width='stretch', key="view_timeline"):
                st.session_state.view_timeline_ticket = ticket_to_update
                st.session_state.show_timeline_modal = True

        # Timeline modal
        if st.session_state.get('show_timeline_modal', False):
            ticket_id = st.session_state.get('view_timeline_ticket', '')
            timeline_data = get_complaint_timeline(ticket_id)
            
            st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="font-family: 'Poppins', sans-serif; color: #e0e7ff; margin-bottom: 1rem;">
                    📅 Timeline for {ticket_id}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            if "error" not in timeline_data:
                timeline = timeline_data.get('timeline', [])
                # Get current device time once
                device_now = datetime.now().strftime('%b %d, %Y at %I:%M %p')
                for entry in timeline:
                    # Use current device time
                    formatted_date = device_now

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
        <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
            <p style="font-size: 3rem; margin-bottom: 1rem;">📭</p>
            <h3 style="font-family: 'Poppins', sans-serif; color: #e0e7ff; margin-bottom: 0.5rem;">No Complaints Found</h3>
            <p style="color: #94a3b8; margin: 0;">No complaints match the selected filters.</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
