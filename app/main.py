from fastapi import FastAPI

from app.trainings.router import router as router_trainings
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings


app = FastAPI()

@app.get("/")
async def top_page():
    return {"msg": "top page"}

app.include_router(router_users)
app.include_router(router_trainings)
app.include_router(router_bookings)