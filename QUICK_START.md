# 🚀 Quick Start Guide

## Step 1: Get API Keys

### Google Gemini API (Free)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with "AIza...")

### Resend API (Free tier)
1. Go to https://resend.com
2. Sign up for an account
3. Go to API Keys section
4. Create and copy your API key

## Step 2: Update Environment Files

Edit these files and replace with your actual keys:

### File: `.env`
```
GEMINI_API_KEY=AIza...your_gemini_key_here
RESEND_API_KEY=re_...your_resend_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### File: `backend/.env`
```
GEMINI_API_KEY=AIza...your_gemini_key_here
RESEND_API_KEY=re_...your_resend_key_here
CORS_ORIGINS=http://localhost:3000
```

## Step 3: Run Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 4: Run Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

## Step 5: Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Step 6: Test It

1. Open http://localhost:3000
2. Upload a CSV/Excel file with sales data
3. Enter your email
4. Click "Generate Insights"
5. Check your email for the AI report!

## Sample CSV Data

Create a test CSV file with this format:

```csv
Date,Product,Category,Revenue,Region
2024-01-01,Laptop,Electronics,1200,North
2024-01-02,Phone,Electronics,800,South
2024-01-03,Chair,Furniture,300,East
2024-01-04,Desk,Furniture,500,West
2024-01-05,Tablet,Electronics,600,North
```
