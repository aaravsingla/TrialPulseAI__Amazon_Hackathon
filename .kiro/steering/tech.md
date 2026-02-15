# Technology Stack

## Architecture

Full-stack application with separate frontend and backend services:
- **Frontend**: React + TypeScript SPA served via Vite
- **Backend**: Python FastAPI REST API
- **Communication**: Axios for HTTP requests, CORS enabled for local development

## Frontend Stack

### Core Technologies
- **React 19.2.0**: UI framework
- **TypeScript 5.9.3**: Type-safe development
- **Vite 7.2.4**: Build tool and dev server
- **Tailwind CSS 3.4.17**: Utility-first styling

### Key Libraries
- **UI Components**: Custom components built with `clsx` and `tailwind-merge`
- **Icons**: `lucide-react` for consistent iconography
- **Animations**: `framer-motion` for smooth transitions
- **Data Visualization**: 
  - `recharts` for charts and timelines
  - `react-simple-maps` for geographic visualizations
  - `d3-scale` for data scaling
- **HTTP Client**: `axios` for API communication

### Development Tools
- **Linting**: ESLint with React-specific plugins
- **Type Checking**: TypeScript with strict configuration
- **PostCSS**: For Tailwind processing

## Backend Stack

### Core Technologies
- **FastAPI**: Modern Python web framework
- **Python**: Runtime environment
- **Uvicorn**: ASGI server

### Key Libraries
- **google-generativeai**: Gemini 1.5 Flash model for AI chat
- **pandas**: Data processing and Excel file handling
- **pydantic**: Request/response validation
- **python-dotenv**: Environment variable management

### Data Processing
- Excel file parsing via `pandas`
- Site-level aggregation from subject data
- Dynamic risk scoring and DQI calculation

## Common Commands

### Frontend
```bash
cd frontend

# Development server (http://localhost:5173)
npm run dev

# Type checking and production build
npm run build

# Linting
npm run lint

# Preview production build
npm run preview
```

### Backend
```bash
cd backend

# Activate virtual environment (if using venv)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix

# Install dependencies
pip install fastapi uvicorn google-generativeai pandas python-dotenv openpyxl

# Run development server (http://localhost:8000)
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Setup

Backend requires `.env` file with:
```
GOOGLE_API_KEY=your_gemini_api_key
```

## API Endpoints

- `POST /api/nl-query`: Natural language query processing
- `GET /api/sites`: Retrieve all site data

## Build System Notes

- Frontend uses Vite's fast HMR for development
- TypeScript compilation happens during build (`tsc -b`)
- Backend has no build step (interpreted Python)
- CORS configured for `localhost` development
