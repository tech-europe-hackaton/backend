# Content Generation API

A FastAPI-based backend service that generates social media content and images using AI APIs. The service integrates with Dust API for content generation and OpenAI DALL-E for image creation.

## 🌐 Live Deployment

The backend is deployed and accessible at: **[https://backend-smqp.onrender.com/docs](https://backend-smqp.onrender.com/docs)**

You can explore the interactive API documentation using the Swagger UI at the above link.

## 📁 Project Structure

```
hackaton/
├── backend/                    # Main backend application
│   ├── app.py                 # FastAPI application with all endpoints
│   ├── prompt.txt             # Content generation prompt template
│   ├── pyproject.toml         # Python dependencies and project config
│   ├── uv.lock               # Dependency lock file
│   └── README.md              # This documentation
├── mcp/                       # MCP (Model Context Protocol) service
│   ├── main.py               # MCP server implementation
│   ├── pyproject.toml        # MCP dependencies
│   └── README.md             # MCP documentation
└── response_example.txt       # Example API response
```

## 🚀 Local Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tech-europe-hackaton/backend.git
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory with the following variables:
   ```env
   WORKSPACE_ID=your_dust_workspace_id
   AGENT_ID=your_dust_agent_id
   DUST_API_KEY=your_dust_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application

**Start the FastAPI server:**
```bash
uv run python app.py
```

**Alternative using uvicorn directly:**
```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload when you make code changes during development.

### Accessing the Application

Once the server is running, you can access:

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### 1. Content Generation

**Endpoint:** `POST /generate-content`

Generates social media content using Dust API with customizable parameters.

**Request Body:**
```json
{
  "topics_of_interest": ["AI & Technology", "Startups"],
  "ai_voice": "professional",
  "about_context": "I want to promote my startup that creates an AI agent to help HR people to recruit",
  "post_preference": "make impactful post"
}
```

**Default Values:**
- `topics_of_interest`: `["AI & Technology", "Startups"]`
- `ai_voice`: `"professional"`
- `about_context`: `"I want to promote my startup that creates an AI agent to help HR people to recruit"`
- `post_preference`: `"make impactful post"`

**Response:**
Returns parsed JSON content directly:
```json
{
  "1": "content_id_1",
  "2": "content_id_2",
  "3": "content_id_3",
  ...
  "10": "content_id_10"
}
```

### 2. Image Generation

**Endpoint:** `POST /image-generation`

Generates images using OpenAI DALL-E 3 API.

**Request Body:**
```json
{
  "prompt": "A beautiful landscape with mountains and a lake"
}
```

**Default Value:**
- `prompt`: `"A beautiful landscape with mountains and a lake"`

**Response:**
```json
{
  "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/..."
}
```

### 3. Health Check

**Endpoint:** `GET /health`

Checks if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🔧 Features

- **AI Content Generation**: Uses Dust API to generate social media content based on user preferences
- **Image Generation**: Creates images using OpenAI DALL-E 3
- **CORS Support**: Configured for cross-origin requests
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Interactive Documentation**: Swagger UI and ReDoc for easy API exploration

## 🛠️ Dependencies

- **FastAPI**: Web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Requests**: HTTP library for API calls
- **OpenAI**: Official OpenAI Python client
- **Uvicorn**: ASGI server for running FastAPI applications

## 🌐 CORS Configuration

The API is configured with the following CORS settings:
- **Access-Control-Allow-Origin**: `*` (allows requests from any origin)
- **Access-Control-Allow-Headers**: `Content-Type`
- **Access-Control-Allow-Methods**: `POST`, `OPTIONS`

## 📝 Usage Examples

### Using curl

**Generate Content:**
```bash
curl -X POST "http://localhost:8000/generate-content" \
     -H "Content-Type: application/json" \
     -d '{
       "topics_of_interest": ["AI", "Machine Learning"],
       "ai_voice": "casual",
       "about_context": "Tech enthusiast sharing AI insights",
       "post_preference": "engaging and educational"
     }'
```

**Generate Image:**
```bash
curl -X POST "http://localhost:8000/image-generation" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Modern tech office with AI elements"}'
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

### Using the Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Modify the request body as needed
5. Click "Execute" to test the endpoint

## 🚨 Error Handling

The API returns appropriate HTTP status codes:
- **200**: Success
- **404**: Resource not found
- **500**: Internal server error

Error responses include descriptive error messages to help with debugging.

## 🛠️ Technology Stack

This project leverages the following technologies:

- **Dust**: AI agent platform for web scraping functionality and intelligent content generation
- **OpenAI**: Advanced AI models for image generation using DALL-E 3
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.13+**: Core programming language
- **uv**: Fast Python package manager and project manager

## 📄 License

This project is part of a hackathon submission and is intended for demonstration purposes.
