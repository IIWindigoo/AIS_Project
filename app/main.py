from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.trainings.router import router as router_trainings
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.rooms.router import router as router_rooms
from app.subscriptions.router import router as router_subscriptions
from app.memberships.router import router as router_memberships


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(router_users)
app.include_router(router_rooms)
app.include_router(router_trainings)
app.include_router(router_bookings)
app.include_router(router_subscriptions)
app.include_router(router_memberships)

frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_root():
    index_file = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_file)

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"msg": "Not found"}
