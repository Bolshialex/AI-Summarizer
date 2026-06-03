from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.summary import router as summary_router
from routes.transcribe import router as transcribe_router

app = FastAPI(title="Summarize-AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe_router)
app.include_router(summary_router)


@app.get("/")
def root():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)