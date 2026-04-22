from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url='/',title="Learnix System", description="Learnix o'quv markazi CRM tizimi")

app.include_router(api)

app.mount("/images", StaticFiles(directory="images"), name="images")


origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
