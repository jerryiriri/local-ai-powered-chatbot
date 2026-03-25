# Local AI-Powered Chatbot

A privacy-first, locally deployed AI chatbot built with Python, FastAPI, Streamlit, LangChain, and Ollama.

This system is designed for environments where cloud-based AI is not viable due to data sensitivity, unreliable connectivity, or cost constraints. It enables fully local AI interaction with no external API calls, making it suitable for public sector, digital inclusion, and privacy-sensitive use cases.

---

## Why I Built This

Most AI chatbot implementations depend on cloud APIs like OpenAI or Anthropic. For many real-world contexts, that dependency creates genuine problems. Data leaves the machine. Costs accumulate with every query. Connectivity cannot be guaranteed. For users in public sector environments or low-resource settings, those are not minor inconveniences but real barriers to access.

I built this project to answer a specific question: can a fully capable AI chatbot be deployed entirely on local infrastructure, with no external API calls, no ongoing costs, and no data leaving the device?

The answer is yes. Working through that question end to end shaped how I think about AI system design. The architectural patterns I developed here, particularly around local LLM serving, conversation persistence, and containerised deployment, directly informed the design of StepWise, an AI-powered digital inclusion platform I later built based on 13 documented real-world support cases from my AbilityNet volunteer work.

This project reflects a broader and increasingly important shift in AI deployment: moving away from cloud-dependent tools toward locally controlled, privacy-aware systems that can operate reliably in the environments where people actually need them.

---

## What It Does

The system provides a conversational AI interface powered entirely by locally hosted large language models. Users interact through a clean web interface, receive context-aware responses, and maintain persistent conversation history across sessions. No data leaves the machine at any point.

Key capabilities:

- Natural language query handling through a browser-based interface
- Local LLM inference via Ollama with no external API calls required
- Persistent conversation memory stored in SQLite across sessions
- Context-aware responses using LangChain orchestration
- Fully containerised deployment using Docker Compose
- Support for multiple models including Llama 3, Mistral, Gemma, and Phi-3

### Example Use Case

In a privacy-sensitive or low-connectivity environment, such as a public service setting or community support context, users can interact with the system to receive guidance or explanations without requiring internet access or exposing sensitive data to third-party services.

This is particularly relevant in digital inclusion scenarios, where users may rely on shared devices, limited connectivity, or require additional privacy safeguards. It is the same context that motivated the design of StepWise, where the Ollama fallback layer ensures the system can still function when cloud inference is unavailable.

---

## Screenshots

### Chat Interface
![Chat interface on load](screenshots/chat-interface.png)
*The Streamlit frontend on initial load*

### Active Conversation
![Active conversation with AI response](screenshots/active-conversation.png)
*A user query and the locally generated AI response*

### Backend API Documentation
![FastAPI Swagger UI](screenshots/api-docs.png)
*Auto-generated API documentation at localhost:8000/docs*

---

## Technical Architecture

The system uses a modular, service-oriented architecture with clear separation between the interface layer, orchestration layer, and model runtime.

```
User Input (Streamlit)
        |
        v
FastAPI Backend API
        |
        v
LangChain Orchestration Layer
        |
        v
Ollama LLM Runtime (local model serving)
        |
        v
Response Generation
        |
        v
SQLite (conversation persistence)
        |
        v
Response returned to Streamlit frontend
```

### Component Responsibilities

| Component | Role |
|-----------|------|
| Streamlit | Frontend chat interface. Handles user input, displays responses, and manages session state. |
| FastAPI | Backend API layer. Receives requests, manages routing, and handles communication with LangChain. |
| LangChain | Orchestration layer. Manages conversation chains, injects history into context, and interfaces with Ollama. |
| Ollama | Local LLM runtime. Serves the language model entirely on the local machine with no external API calls. |
| SQLite | Persistent storage for conversation history. Context survives session restarts. |
| Docker Compose | Orchestrates the multi-container environment with defined networking and startup sequencing. |

---

## Design Decisions

**Why FastAPI over Flask**

FastAPI provides native async support, automatic OpenAPI documentation, and Pydantic-based request validation out of the box. For an AI application where response latency and structured data handling both matter, FastAPI is a stronger foundation. The auto-generated docs at `/docs` also make it straightforward to test and validate the API independently of the frontend during development, which matters when you are iterating on the AI pipeline specifically.

**Why Streamlit for the frontend**

The priority for this project was the backend architecture and AI integration rather than frontend complexity. Streamlit allowed the interface to be built and iterated quickly while keeping focus on what mattered most: the orchestration, the local inference layer, and the persistence design. A production-scale or multi-user deployment would replace this with a React frontend, which is the approach taken in StepWise.

**Why SQLite for persistence**

SQLite keeps the stack self-contained and simple. Conversation history does not need the overhead of a full database server for a local single-user deployment. For a multi-user or cloud-hosted version, this moves to PostgreSQL, which is the choice made in StepWise where session state and flow tracking require a more capable backend.

**Why Docker Compose for orchestration**

Running FastAPI, Streamlit, and Ollama as separate services requires reliable inter-container networking and controlled startup sequencing. Docker Compose handles this cleanly and makes the application reproducible across any machine with Docker installed, without environment-specific configuration. This is the same deployment approach carried forward into StepWise.

**Why a fully local stack**

Four reasons drove this decision. No data leaves the machine, which matters in privacy-sensitive contexts. No external API dependency means the system works without internet access. No per-token costs makes it viable for resource-constrained deployments. And full control over which model runs and how it is configured. These are the same reasons the Ollama local fallback layer was included in StepWise, where it handles inference when the primary GPT-4o integration is unavailable or unsuitable for the use case.

---

## Connection to Broader Work

This project was the direct technical predecessor to the AI architecture in StepWise. Building and testing this system end to end before starting StepWise meant the architectural decisions in the larger product were grounded in real implementation experience rather than untested design assumptions.

**Local LLM fallback layer**

This project validated the Ollama deployment pattern and gave me direct experience with model configuration, the pull workflow, and inference latency characteristics. That experience shaped how I designed the fallback layer in StepWise, where Ollama handles inference when GPT-4o is unavailable or cost-constrained. Without having run this in practice first, that fallback design would have been theoretical.

**LangChain orchestration patterns**

The conversation chain structure developed here informed how I designed the RAG retrieval pipeline in StepWise, where LangChain manages the interface between user input, a FAISS vector store seeded from real casework, and the LLM response layer. The context injection patterns are a direct extension of what was built and tested here.

**Backend architecture**

StepWise uses the same FastAPI and database-backed backend pattern, extended with a structured flow engine, session state tracking, and a human context detection layer. The foundation was established in this project and built on from there.

**Containerised deployment**

Both projects use Docker Compose for consistent, portable environment management. The networking patterns and service coordination approach developed here transferred directly into the StepWise deployment design.

---

## System Validation

The system has been tested across multiple local environments to confirm:

- Consistent deployment and container startup using Docker Compose
- Model response behaviour across different LLMs including Llama 3, Mistral, and Gemma
- Correct persistence and retrieval of conversation history across session restarts
- End-to-end interaction between the Streamlit frontend, FastAPI backend, and Ollama runtime
- Environment variable configuration for model switching without code changes

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI (Python) |
| Frontend | Streamlit |
| LLM Orchestration | LangChain |
| LLM Runtime | Ollama |
| Persistence | SQLite |
| Containerisation | Docker, Docker Compose |
| Package Management | uv |

---

## Prerequisites

- Docker and Docker Compose
- Minimum 8GB RAM recommended for local LLM inference
- (Optional) `uv` for local development without Docker

---

## Setup and Run

**1. Clone the repository**

```bash
git clone https://github.com/jerryiriri/local-ai-powered-chatbot.git
cd local-ai-powered-chatbot
```

**2. Environment setup**

```bash
cp .env.example .env
```

Review `.env` and update the model name if you want to use a different LLM.

**3. Start all services**

```bash
docker compose up --build
```

**4. Pull your chosen model**

Once the containers are running, pull the model into the Ollama container:

```bash
docker exec -it chatbot-ollama ollama pull llama3
```

Replace `llama3` with your preferred model. Options include `mistral`, `gemma`, `phi3`, or any model available through Ollama.

**5. Access the application**

- Chat interface: http://localhost:8501
- Backend API documentation: http://localhost:8000/docs

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── config.py           # Configuration and environment settings
│   │   ├── database.py         # SQLite connection and session management
│   │   ├── main.py             # FastAPI entry point and route definitions
│   │   ├── models.py           # Pydantic request and response models
│   │   └── streamlit_app.py    # Streamlit frontend application
│   └── pyproject.toml          # Project dependencies (uv)
├── docker-compose.yml          # Multi-container orchestration
├── Dockerfile                  # Container definition for backend and frontend
├── .env.example                # Environment variable reference
└── README.md
```

---

## Local Development Without Docker

```bash
# Install uv
pip install uv

# Navigate to backend
cd backend
uv sync

# Terminal 1 - run the backend
uv run uvicorn app.main:app --reload

# Terminal 2 - run the frontend
uv run streamlit run app/streamlit_app.py
```

Make sure Ollama is running locally or update `.env` to point to your Ollama instance URL.

---

## About the Developer

Jerry Iriri is a data engineer and AI product designer with around 10 years of experience across enterprise data architecture, cloud infrastructure, and business intelligence. His work focuses on building practical, privacy-aware AI systems that operate reliably in real-world environments, including public sector and digital inclusion contexts.

This project was built as an independent technical exploration of local LLM deployment and directly informed the architecture of StepWise, an AI-powered digital inclusion platform currently in development.

LinkedIn: [linkedin.com/in/jerry-iriri](https://linkedin.com/in/jerry-iriri)
