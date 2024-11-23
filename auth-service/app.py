from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apis import login

app = FastAPI()

app.include_router(login.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # uvicorn app:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)