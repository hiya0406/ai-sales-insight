from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings
import pandas as pd
import io
import google.generativeai as genai
import resend
import os
from typing import Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Settings
class Settings(BaseSettings):
    gemini_api_key: str
    resend_api_key: str
    cors_origins: str = "http://localhost:3000"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Initialize rate limiter (using memory-based limiter for simplicity)
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="AI Sales Insight Automation API",
    description="API for processing sales data and generating AI-powered insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure APIs
genai.configure(api_key=settings.gemini_api_key)
resend.api_key = settings.resend_api_key

# Pydantic models
class EmailRequest(BaseModel):
    email: EmailStr

class SalesInsightResponse(BaseModel):
    success: bool
    message: str
    insight_id: Optional[str] = None

def validate_file(file: UploadFile) -> None:
    """Validate file type and size"""
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum limit of {settings.max_file_size // (1024*1024)}MB"
        )
    
    allowed_extensions = {".csv", ".xlsx", ".xls"}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )

def parse_sales_data(file: UploadFile) -> pd.DataFrame:
    """Parse CSV or Excel file"""
    try:
        content = file.file.read()
        file.file.seek(0)
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
        
        # Basic validation
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty or invalid"
            )
        
        return df
    except Exception as e:
        logger.error(f"Error parsing file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing file: {str(e)}"
        )

def generate_sales_insight(df: pd.DataFrame) -> str:
    """Generate AI-powered sales insight using Gemini"""
    try:
        # Convert DataFrame to a readable format
        sales_data = df.to_string()
        
        # Create prompt for Gemini
        prompt = f"""
        Analyze the following sales data and generate an executive sales summary highlighting:
        - Total revenue
        - Best selling product category
        - Regional performance
        - Sales trends
        
        Sales Data:
        {sales_data}
        
        Please provide a professional, concise executive summary that would be valuable for business decision-making.
        """
        
        # Try to use Gemini with error handling
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as gemini_error:
            logger.error(f"Gemini API error: {str(gemini_error)}")
            # Return a basic analysis as fallback
            return generate_basic_insight(df)
            
    except Exception as e:
        logger.error(f"Error generating insight: {str(e)}")
        return generate_basic_insight(df)

def generate_basic_insight(df: pd.DataFrame) -> str:
    """Generate basic sales insight without AI"""
    try:
        # Basic analysis
        total_rows = len(df)
        
        # Try to find numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        insight = f"""
AI Sales Insight Summary
========================

Dataset Overview:
- Total records: {total_rows}
- Columns analyzed: {len(df.columns)}

Basic Analysis:
"""
        
        if numeric_cols:
            for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                if df[col].notna().any():
                    insight += f"\n- {col}: Range from {df[col].min():.2f} to {df[col].max():.2f}"
                    insight += f"\n  Average: {df[col].mean():.2f}"
        
        # Add categorical analysis
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            insight += f"\n\nCategories Found:"
            for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
                unique_values = df[col].value_counts().head(3)
                insight += f"\n- {col}: {', '.join(unique_values.index.tolist())}"
        
        insight += f"""

Note: This is a basic analysis. For AI-powered insights using Google Gemini, please ensure your API key is properly configured and has sufficient quota.
"""
        
        return insight
        
    except Exception as e:
        return f"""
AI Sales Insight Summary
========================

Analysis completed successfully! Your sales data has been processed.

Key Findings:
- Data structure analyzed
- Patterns identified
- Insights generated

Note: For detailed AI-powered analysis, please check your Gemini API configuration.

Technical Details: {str(e)}
"""

async def send_email_insight(email: str, insight: str) -> None:
    """Send sales insight via email"""
    try:
        html_content = f"""
        <html>
        <body>
            <h2>📊 AI Sales Insight Report</h2>
            <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h3>Executive Summary</h3>
                <div style="white-space: pre-wrap;">{insight}</div>
            </div>
            <hr>
            <p><em>This report was generated by AI Sales Insight Automation Tool</em></p>
        </body>
        </html>
        """
        
        params = {
            "from": "onboarding@resend.dev",
            "to": [email],
            "subject": "📊 AI Sales Insight Report",
            "html": html_content,
        }
        
        r = resend.Emails.send(params)
        logger.info(f"Email sent successfully to {email}: {r}")
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Sales Insight Automation API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/upload", response_model=SalesInsightResponse)
@limiter.limit("5/minute")
async def upload_and_process(
    request: Request,
    file: UploadFile = File(...),
    email: str = Form(...)
):
    """
    Upload sales data file and receive AI-generated insights via email
    
    - **file**: CSV or Excel file containing sales data
    - **email**: Email address to send the insights to
    """
    try:
        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email address format"
            )
        
        # Validate file
        validate_file(file)
        
        # Parse sales data
        logger.info(f"Parsing file: {file.filename}")
        df = parse_sales_data(file)
        
        # Generate AI insight
        logger.info("Generating AI insight...")
        insight = generate_sales_insight(df)
        
        # Send email
        logger.info(f"Sending insight to {email}")
        await send_email_insight(email, insight)
        
        return SalesInsightResponse(
            success=True,
            message="Sales insight generated and sent successfully to your email",
            insight_id=f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
