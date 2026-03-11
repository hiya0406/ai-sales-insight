# 📊 AI Sales Insight Automation Tool

A full-stack application that processes sales data files and generates AI-powered executive insights via email using Google Gemini API.

## 🚀 Features

- **File Upload**: Support for CSV and Excel (.xlsx, .xls) files
- **AI-Powered Insights**: Uses Google Gemini API to analyze sales data and generate executive summaries
- **Email Delivery**: Automatically sends insights to specified email addresses
- **Security**: File type validation, size limits, email validation, and rate limiting
- **Modern UI**: Clean, responsive Next.js frontend with Tailwind CSS
- **API Documentation**: Auto-generated Swagger docs at `/docs`

## 🏗️ Architecture

```
├── frontend/          # Next.js React application
├── backend/           # FastAPI Python server
├── docker/            # Docker configurations
├── .github/workflows/ # CI/CD pipelines
└── docker-compose.yml # Multi-container setup
```

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management

### Backend
- **FastAPI** - Python web framework
- **Pandas** - Data processing
- **Google Generative AI** - AI insights
- **Resend** - Email service
- **Redis** - Rate limiting
- **Pydantic** - Data validation

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Redis** - Rate limiting store

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- Redis server
- Google Gemini API key
- Resend API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-sales-insight
```

### 2. Environment Setup

Copy the environment example files:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Update `.env` with your API keys:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Resend API Key (for email sending)
RESEND_API_KEY=your_resend_api_key_here

# Frontend Environment
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (if not running)
redis-server

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📖 Usage

1. **Access the Application**: Open http://localhost:3000 in your browser
2. **Upload Sales Data**: Select a CSV or Excel file containing sales data
3. **Enter Email**: Provide the email address where insights should be sent
4. **Generate Insights**: Click "Generate Insights" to process the data
5. **Receive Report**: Check your email for the AI-generated sales insights

### Expected Sales Data Format

Your CSV/Excel file should contain sales data with columns like:
- Date/Time
- Product/Category
- Revenue/Amount
- Region/Location
- Customer information

## 🔧 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /upload` - Upload file and generate insights
- `GET /health` - Health check
- `GET /docs` - Swagger documentation

## 🛡️ Security Features

- **File Validation**: Only CSV and Excel files accepted
- **Size Limits**: Maximum file size of 10MB
- **Email Validation**: Proper email format verification
- **Rate Limiting**: 5 requests per minute per IP
- **CORS Protection**: Configurable allowed origins

## 🚀 Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Render)

1. Connect your GitHub repository to Render
2. Configure environment variables
3. Deploy as a web service

### Environment Variables for Production

```env
GEMINI_API_KEY=your_production_gemini_key
RESEND_API_KEY=your_production_resend_key
CORS_ORIGINS=https://your-frontend-domain.com
REDIS_URL=your_redis_connection_string
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Linting
flake8 .
black --check .

# Type checking
mypy .

# Run tests (if implemented)
pytest
```

### Frontend Tests

```bash
cd frontend

# Linting
npm run lint

# Type checking
npx tsc --noEmit

# Build test
npm run build
```

## 📝 Development

### Adding New Features

1. **Backend**: Add endpoints in `main.py`
2. **Frontend**: Create components in `src/app/`
3. **Styles**: Use Tailwind CSS classes
4. **API**: Update Pydantic models for validation

### Code Quality

- Backend follows PEP 8 Python standards
- Frontend uses TypeScript strict mode
- All code is linted and formatted
- Docker images are optimized for production

## 🐛 Troubleshooting

### Common Issues

1. **Redis Connection Error**: Ensure Redis is running on port 6379
2. **API Key Errors**: Verify your Gemini and Resend API keys
3. **File Upload Issues**: Check file format and size limits
4. **CORS Errors**: Verify frontend URL is in allowed origins

### Logs

```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend

# Manual setup logs
# Backend: Check terminal output
# Frontend: Check browser console
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation at `/docs`

---

**Built with ❤️ using Next.js, FastAPI, and Google Gemini AI**
