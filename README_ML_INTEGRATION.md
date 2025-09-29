# PhishShield ML Integration Guide

This guide explains how to set up and run the ML backend server and connect it with the frontend.

## Prerequisites

- Python 3.8+ installed
- Node.js and npm installed
- ML model files available in `ML Models/` directory

## Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server**:
   ```bash
   # From the backend directory
   uvicorn main:app --reload --port 8000
   
   # Or from the project root
   cd backend && uvicorn main:app --reload --port 8000
   ```

3. **Verify the backend is running**:
   - Open http://localhost:8000 in your browser
   - You should see a JSON response: `{"message":"PhishShield ML API is running"}`

## Frontend Setup

1. **Install frontend dependencies** (if not already done):
   ```bash
   npm install
   ```

2. **Start the frontend development server**:
   ```bash
   npm run dev
   ```

3. **Verify the frontend is running**:
   - Open http://localhost:8080 in your browser
   - You should see the PhishShield application

## Testing the Integration

1. **Test Email Detection**:
   - Navigate to the Email Detection page
   - Paste some email content and click "Analyze Email"
   - The frontend should call the backend API and display real ML results

2. **Test URL Detection**:
   - Navigate to the URL Detection page
   - Enter a URL and click "Analyze URL"
   - The frontend should call the backend API and display real ML results

## API Endpoints

### Email Analysis
- **URL**: `POST http://localhost:8000/api/analyze/email`
- **Request Body**:
  ```json
  {
    "email_text": "Your email content here..."
  }
  ```
- **Response**:
  ```json
  {
    "classification": "ham|spam|phishing",
    "confidence": 95.5,
    "threats": [
      {"description": "Threat description", "severity": "high"}
    ],
    "analysis": "Analysis text"
  }
  ```

### URL Analysis
- **URL**: `POST http://localhost:8000/api/analyze/url`
- **Request Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```
- **Response**:
  ```json
  {
    "classification": "safe|phishing",
    "confidence": 92.3,
    "threats": [
      {"description": "Threat description", "severity": "high"}
    ],
    "analysis": "Analysis text",
    "domain_info": {
      "age": "2 years",
      "registrar": "GoDaddy",
      "ssl": true
    }
  }
  ```

## Troubleshooting

### Common Issues

1. **Backend fails to start**:
   - Check that all Python dependencies are installed
   - Verify the ML model files exist in `ML Models/` directory

2. **Frontend cannot connect to backend**:
   - Ensure the backend is running on port 8000
   - Check for CORS errors in the browser console

3. **ML models not loading**:
   - Verify the paths to the pickle files are correct
   - Check that the models were trained and saved properly

### Development Tips

- The backend server automatically reloads when you make changes to `backend/main.py
