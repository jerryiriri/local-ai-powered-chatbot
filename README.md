# Local AI Chatbot

A fully local, Dockerized AI chatbot using Python (FastAPI), Streamlit, LangChain, and Ollama.

## Features

- **100% Local**: No external APIs or internet required after initial setup.
- **Dockerized**: Easy deployment with Docker Compose.
- **Persistent History**: Chat history saved in SQLite database.
- **Configurable**: Environment variables for customization.
- **Clean Architecture**: Separation of concerns between backend (FastAPI) and frontend (Streamlit).

## Prerequisites

- Docker and Docker Compose
- (Optional) `uv` for local development

## Setup & Run

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd local-ai-powered-chatbot
    ```

2.  **Environment Setup**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

3.  **Start Services**:
    Run with Docker Compose:
    ```bash
    docker compose up --build
    ```

4.  **Pull LLM Model**:
    Once the containers are running, you need to pull the model in the Ollama container. Open a new terminal and run:
    ```bash
    docker exec -it chatbot-ollama ollama pull llama3
    ```
    (Or replace `llama3` with your preferred model like `mistral`, `gemma`, etc., and update `.env` accordingly).

5.  **Access the App**:
    - **Frontend (Chat Interface)**: [http://localhost:8501](http://localhost:8501)
    - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database connection & session
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── models.py       # Pydantic models
│   │   └── streamlit_app.py # Streamlit frontend application
│   └── pyproject.toml      # Project dependencies (UV)
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Container definition for backend/frontend
└── .env.example            # Environment variables example
```

## Development

To run locally without Docker:

1.  Install `uv`.
2.  Navigate to `backend`:
    ```bash
    cd backend
    uv sync
    ```
3.  Run Backend:
    ```bash
    uv run uvicorn app.main:app --reload
    ```
4.  Run Frontend (in a separate terminal):
    ```bash
    cd backend
    uv run streamlit run app/streamlit_app.py
    ```
5.  Ensure you have a local instance of Ollama running or update `.env` to point to the correct URL.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM Runtime**: Ollama
- **Orchestration**: LangChain
- **Database**: SQLite
- **Package Manager**: uv
