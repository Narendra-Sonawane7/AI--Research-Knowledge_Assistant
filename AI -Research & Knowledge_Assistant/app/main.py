from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import documents, search, qa, summary, compare, classify, analytics
from app.routers import auth
from app.models.user import User
from app.routers import agent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Research & Knowledge Assistant",
    version="1.0.0",
    description="Simple RAG + Groq + TensorFlow assignment project",
)
app.include_router(
    agent.router
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(search.router)
app.include_router(qa.router)
app.include_router(summary.router)
app.include_router(compare.router)
app.include_router(classify.router)
app.include_router(analytics.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "AI Research & Knowledge Assistant is running"}
