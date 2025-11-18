from fastapi import FastAPI

from app.trainings.router import router as router_trainings
from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.rooms.router import router as router_rooms
from app.subscriptions.router import router as router_subscriptions
from app.memberships.router import router as router_memberships


app = FastAPI()

@app.get("/")
async def top_page():
    return {"msg": "top page"}

app.include_router(router_users)
app.include_router(router_rooms)
app.include_router(router_trainings)
app.include_router(router_bookings)
app.include_router(router_subscriptions)
app.include_router(router_memberships)