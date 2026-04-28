# 🏛️ CivicFix - Government Utility Grievance Redressal System

An end-to-end AI-powered platform for citizens to report utility grievances and for government administrators to efficiently manage and resolve them.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Model Performance](#model-performance)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

CivicFix enables citizens to report issues related to government utilities (Electricity, Water Supply, Waste-Water/Sewage, Billing) through a simple web interface. The system uses a TensorFlow-based Multi-Output Neural Network to automatically categorize complaints by department and severity, ensuring efficient routing to the appropriate authorities.

### Key Capabilities

- **Citizen Portal**: Simple form for grievance submission
- **AI Categorization**: Automatic department and severity classification
- **Admin Dashboard**: Real-time analytics and complaint management
- **Status Tracking**: Monitor complaint resolution progress

## ✨ Features

### For Citizens
- Easy-to-use complaint submission form
- Automatic AI-based categorization
- Ticket ID for tracking
- No login required

### For Administrators
- Password-protected dashboard
- Real-time statistics and KPIs
- Interactive charts (Plotly)
- Filter complaints by department/status
- Update complaint status
- Export capabilities

### Machine Learning
- Multi-output Neural Network (TensorFlow 2.x)
- Bidirectional LSTM architecture
- TextVectorization for preprocessing
- Class weight balancing for imbalanced data
- >85% accuracy on both classification tasks

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python FastAPI |
| **Frontend** | Streamlit |
| **Database** | SQLite + SQLAlchemy ORM |
| **ML Library** | TensorFlow 2.x (Keras API) |
| **Visualization** | Plotly |
| **Data Processing** | Pandas, Scikit-Learn |

## 📁 Project Structure

```
civic_fix/
├── data/
│   └── complaints_dataset.csv      # Generated synthetic data (1500+ records)
├── models/
│   ├── grievance_model.keras       # Trained TensorFlow model
│   ├── vectorizer_config.json      # Text preprocessing config
│   ├── label_encoders.json         # Label encoder mappings
│   └── training_metrics.json       # Model performance metrics
├── src/
│   ├── generate_data.py            # Synthetic data generator
│   ├── train_model.py              # ML training pipeline
│   ├── database.py                 # SQLAlchemy ORM setup
│   ├── main.py                     # FastAPI backend
│   └── app.py                      # Streamlit frontend
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Step 1: Clone/Navigate to Project

```bash
cd civic_fix
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Generate Synthetic Data

```bash
cd src
python generate_data.py
```

This creates `data/complaints_dataset.csv` with 1,500+ realistic complaint records.

### Step 4: Train the ML Model

```bash
python train_model.py
```

This will:
- Load and preprocess the data
- Train the Multi-Output Neural Network
- Save model artifacts to `models/` directory
- Display accuracy metrics (target: >85%)

## ⚡ Quick Start

After installation, run these commands in separate terminals:

### Terminal 1: Start FastAPI Backend

```bash
cd civic_fix/src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: **http://localhost:8000**

### Terminal 2: Start Streamlit Frontend

```bash
cd civic_fix/src
streamlit run app.py
```

Frontend will be available at: **http://localhost:8501**

## 📖 Usage Guide

### Citizen Portal

1. Open http://localhost:8501
2. Select "📝 Citizen Portal" from sidebar
3. Describe your issue in the text area
4. Click "Submit Complaint"
5. Note your Ticket ID and predicted category

**Example Complaints:**
- "No water supply in our area for 3 days, emergency situation"
- "Electricity pole sparking dangerously near children's play area"
- "Drainage blocked, sewage water entering homes"

### Admin Dashboard

1. Select "👤 Admin Dashboard" from sidebar
2. Enter password: `admin123`
3. View dashboard with:
   - KPI cards (Total, High Priority, Pending, Resolved)
   - Charts (Department distribution, Severity pie chart)
   - Complaint management table
4. Filter by department or status
5. Update complaint status using the action panel

## 📡 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `POST` | `/submit_complaint` | Submit new complaint |
| `GET` | `/admin/dashboard` | Get dashboard statistics |
| `GET` | `/admin/complaints` | List complaints (filterable) |
| `GET` | `/admin/complaints/{ticket_id}` | Get specific complaint |
| `PUT` | `/admin/update_status/{ticket_id}` | Update complaint status |

### Example API Usage

**Submit Complaint:**
```bash
curl -X POST "http://localhost:8000/submit_complaint" \
  -H "Content-Type: application/json" \
  -d '{"text": "Power cut since morning in Sector 12"}'
```

**Get Dashboard Stats:**
```bash
curl "http://localhost:8000/admin/dashboard"
```

**Update Status:**
```bash
curl -X PUT "http://localhost:8000/admin/update_status/CF-10000" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

## 📊 Model Performance

The Multi-Output Neural Network achieves excellent accuracy:

| Metric | Accuracy |
|--------|----------|
| Department Classification | ~100% |
| Severity Classification | ~100% |
| Overall (both correct) | ~100% |

### Model Architecture

```
Input (Raw Text)
    ↓
TextVectorization (vocab: 500, seq_len: 100)
    ↓
Embedding (128 dimensions)
    ↓
Bidirectional LSTM (64 units)
    ↓
Dropout (0.5)
    ↓
Dense (128, ReLU)
    ↓
Dropout (0.3)
    ↓
┌───────────────┬───────────────┐
│ Department    │ Severity      │
│ (Softmax, 4)  │ (Sigmoid, 1)  │
└───────────────┴───────────────┘
```

### Department Classes
- Electricity
- Water Supply
- Waste-Water/Sewage
- Billing & Accounts

### Severity Classes
- High (safety hazards, outages, flooding)
- Low (routine inquiries, minor issues)

## 🔧 Troubleshooting

### API Not Starting

**Error:** `ModuleNotFoundError`
```bash
# Ensure you're in the src directory and dependencies are installed
cd civic_fix
pip install -r requirements.txt
```

### Model Loading Error

**Error:** `Model not found`
```bash
# Re-run training
cd civic_fix/src
python train_model.py
```

### Database Error

**Error:** `sqlite3.OperationalError`
```bash
# Delete existing database and restart API
rm civicfix.db
uvicorn main:app --reload
```

### Port Already in Use

**Error:** `Address already in use`
```bash
# Use different ports
uvicorn main:app --port 8001
streamlit run app.py --server.port 8502
```

### ML Prediction Returns Default Values

If predictions always return "General/Low":
1. Check model files exist in `models/` directory
2. Verify model trained successfully (>85% accuracy)
3. Check API logs for ML loading errors

## 📝 Notes

- **Security**: The admin password (`admin123`) is hardcoded for demo purposes. In production, use proper authentication.
- **Database**: SQLite is used for simplicity. For production, consider PostgreSQL or MySQL.
- **Scalability**: For high-traffic scenarios, consider async database operations and model serving optimization.

## 🎓 Educational Value

This project demonstrates:
- End-to-end ML pipeline (data → training → deployment)
- Multi-output neural network architecture
- REST API development with FastAPI
- Interactive dashboard with Streamlit
- Database ORM with SQLAlchemy
- Production-ready project structure

---

**Built with ❤️ for Government Digital Transformation**
