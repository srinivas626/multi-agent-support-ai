# Multi-Agent Support AI

A customer support agent built on [LangGraph](https://github.com/langchain-ai/langgraph)
and Amazon Bedrock (Claude) that routes each incoming message through a small
state machine of specialized agents — knowledge retrieval, general chat, and
gated actions (ticket creation, email) — and exposes the result over a FastAPI
HTTP API.

Action requests are checked against a role-based permission table before
anything runs, and high-risk actions (like sending an email) are flagged as
requiring human approval rather than executed automatically.

## Features

- **Multi-agent routing** — an LLM classifies each question as `rag`,
  `general`, or `action` and the graph branches accordingly
  ([app/agents/router.py](app/agents/router.py)).
- **RAG over internal documents** — company support docs in
  `data/documents/` are chunked and embedded (`BAAI/bge-small-en-v1.5`) into a
  local FAISS index (`data/vectorstore/`) for retrieval-grounded answers.
- **Role-based permissions** — `user` / `support_agent` / `admin` roles are
  checked against an action allowlist before any tool runs
  ([app/guardrails/permissions.py](app/guardrails/permissions.py)).
- **Risk-gated actions** — actions marked high-risk (currently `send_email`)
  are intercepted and reported as pending human approval instead of being
  executed ([app/guardrails/risk.py](app/guardrails/risk.py)).
- **Input validation** — tool arguments are validated with Pydantic models
  before execution ([app/guardrails/validation.py](app/guardrails/validation.py)).
- **Web UI** — a minimal static chat page served at `/ui/`.

## Architecture

```
app/
├── agents/                 # Individual agent implementations
│   ├── router.py               # Classifies a question into rag / general / action
│   ├── knowledge_agent.py      # RAG-based question answering
│   ├── general_agent.py        # Fallback conversational agent
│   ├── action_agent.py         # Decides which action + arguments to use
│   └── response_agent.py       # Formats the final reply
├── graph/                  # LangGraph state machine
│   ├── workflow.py             # Builds and compiles the agent graph
│   ├── nodes.py                 # Node implementations (routing, permissions, execution)
│   └── state.py                  # Shared graph state (AgentState)
├── guardrails/              # Safety layer
│   ├── permissions.py           # Role -> allowed-actions table
│   ├── risk.py                   # Marks high-risk actions as needing approval
│   └── validation.py              # Pydantic input validation for tool arguments
├── rag/                     # Retrieval-augmented generation pipeline
│   ├── loader.py                 # Loads source documents
│   ├── chunker.py                 # Splits documents into chunks
│   ├── embeddings.py               # HuggingFace embeddings (BAAI/bge-small-en-v1.5)
│   ├── vectorstore.py               # FAISS vector store
│   ├── retriever.py                  # Similarity search
│   ├── qa.py                          # RAG question answering
│   └── build_index.py                 # Builds/persists the FAISS index
├── tools/                    # Actions agents can invoke
│   ├── ticket_tool.py             # Creates a support ticket (mock)
│   └── email_tool.py               # Sends an email (mock)
├── schemas/models.py         # Pydantic request/response models
├── static/index.html         # Web chat UI, served at /ui/
├── llm.py                    # Bedrock chat model client (ChatBedrockConverse)
├── config.py                  # Environment variable configuration
└── main.py                    # FastAPI app entrypoint
```

## Prerequisites

- Python 3.12+ (`numpy==2.5.2` in `requirements.txt` requires it)
- An AWS account with Bedrock model access enabled for the Claude model you intend to use
- IAM credentials (user or role) with `bedrock:InvokeModel` / `bedrock:Converse` permission
- Docker, if you plan to build/run the container

## Setup

1. **Create and activate a virtual environment**:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:

   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables.** Create a `.env` file in the project root:

   ```env
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_SESSION_TOKEN=
   AWS_REGION=us-east-1
   BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
   ```

   The model ID must be an **inference profile ID** (`us.` prefix) — invoking
   a raw foundation model ID directly fails with a `ValidationException` on
   newer Claude models.

## Building the knowledge base

Source documents live in `data/documents/`. To rebuild the FAISS index after
changing them:

```powershell
python -m app.rag.build_index
```

This writes the updated index to `data/vectorstore/`.

## Running the app

```powershell
uvicorn app.main:app --reload --port 8000
```

- `GET /health` — health check
- `GET /` — status message
- `POST /chat` — body `{"message": "...", "role": "user"}`, returns `{"answer": "...", "route": "..."}`
- `GET /ui/` — web chat UI
- `GET /docs` — interactive API docs (Swagger UI)

Example:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"message\": \"How do I reset my VPN connection?\"}"
```

## Running with Docker

```bash
docker build -t multi-agent-support-ai .
docker run --rm -p 8000:8000 --env-file .env multi-agent-support-ai
```

## Testing

Test files (pytest) are colocated with the modules they cover:

```powershell
pytest app
```

## Deploying to AWS

Pushing to `main` triggers [.github/workflows/deploy.yml](.github/workflows/deploy.yml),
which builds the Docker image, pushes it to Amazon ECR, and redeploys it on an
EC2 instance via AWS Systems Manager (no SSH required).

This needs one-time AWS setup: an ECR repository, an EC2 instance (with Docker
and an IAM instance role for SSM/ECR/Bedrock access), an IAM OIDC role that
GitHub Actions assumes to authenticate, and four GitHub repository secrets
(`AWS_ROLE_ARN`, `AWS_REGION`, `ECR_REPOSITORY`, `EC2_INSTANCE_ID`).

See `AWS-Deployment-Guide.pdf` in this repo for the full step-by-step walkthrough.

## Status / notes

- Ticket creation and email sending are mocked ([app/tools](app/tools)) — they
  return a structured result but don't call a real ticketing/email system.
- Approval on a high-risk action (`send_email`) is reported back in the
  response, not yet resumable — there is no endpoint to submit an approval
  decision and continue the same request.
