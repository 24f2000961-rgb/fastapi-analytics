from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

API_KEY = "ak_fjtd1j7ylx8f6k6yzneri68d"
EMAIL_ADDR = "24f2000961@ds.study.iitm.ac.in"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analytics")
async def analytics(request: Request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    events = body.get("events", [])

    total_events = len(events)
    users = set()
    revenue = 0.0
    user_totals = defaultdict(float)

    for ev in events:
        user = ev.get("user")
        amount = ev.get("amount", 0)
        if user is not None:
            users.add(user)
        if amount is not None and amount > 0:
            revenue += amount
            if user is not None:
                user_totals[user] += amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    return {
        "email": EMAIL_ADDR,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }
