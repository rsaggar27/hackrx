# HackRx FastAPI Backend

This is the FastAPI version of the HackRx backend, converted from Django.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **LangGraph**: Insurance document analysis using LangGraph pipeline
- **Pydantic**: Automatic request/response validation
- **CORS**: Cross-origin resource sharing enabled
- **Auto-documentation**: Interactive API docs at `/docs`

## Installation

1. Activate the virtual environment:
```bash
source .venv2/bin/activate
```

2. Install dependencies:
```bash
pip install -r req2.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your API keys
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
```

## Running the Server

### Option 1: Using the startup script
```bash
python run_server.py
```

### Option 2: Direct uvicorn command
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## API Endpoints

### Health Check
- **GET** `/` - Basic health check
- **GET** `/health` - Detailed health check

### Main Endpoint
- **POST** `/hackrx/run` - Process insurance documents and answer questions

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8001/docs
- **ReDoc documentation**: http://localhost:8001/redoc

## Request Format

```json
{
  "documents": "https://example.com/insurance-policy.pdf",
  "questions": [
    "Is a 30-year-old pregnant female in Delhi covered under a newly issued insurance policy?",
    "What are the coverage limits for maternity benefits?"
  ]
}
```

## Response Format

```json
{
  "answers": [
    "Yes, the policy covers maternity benefits for pregnant females...",
    "The coverage limit for maternity benefits is ₹50,000..."
  ]
}
```

## Project Structure

```
fastapi_backend/
├── .venv2/                 # Virtual environment
├── app/                    # Main application
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── langgraph_runner.py # LangGraph pipeline
│   └── utils/             # Utility modules
│       ├── __init__.py
│       ├── chunker.py
│       ├── document_loader.py
│       ├── query_rephraser.py
│       └── retriever.py
├── req2.txt               # Requirements file
├── run_server.py          # Startup script
└── README.md              # This file
```

## Migration from Django

### Key Changes:
1. **Framework**: Django → FastAPI
2. **Validation**: Manual validation → Pydantic automatic validation
3. **Documentation**: Manual docs → Auto-generated OpenAPI docs
4. **Performance**: Better async support and performance
5. **Type Safety**: Full type hints and validation

### Preserved Functionality:
- All LangGraph pipeline functionality
- Same request/response format
- Same business logic
- Same error handling patterns

## Development

### Adding New Endpoints
1. Add new route functions in `app/main.py`
2. Use Pydantic models for request/response validation
3. Add proper error handling with HTTPException

## Production Deployment

For production:
1. Set `DEBUG=False` in environment
2. Configure proper CORS origins
3. Use a production ASGI server like Gunicorn
4. Set up proper logging and monitoring

Example production command:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
``` 