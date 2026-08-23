from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.graph.workflow import graph


app = FastAPI(
    title="Multi-Agent Support AI",
    version="1.0.0",
)

app.mount(
    "/ui",
    StaticFiles(directory="app/static", html=True),
    name="ui",
)


class ChatRequest(BaseModel):
    message: str
    role: str = "user"


class ChatResponse(BaseModel):
    answer: str
    route: str


@app.get("/")
def root():

    return {
        "message": "Multi-Agent Support AI is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "question": request.message,
            "role": request.role,
        }
    )

    return ChatResponse(
        answer=result["final_response"],
        route=result["route"],
    )
