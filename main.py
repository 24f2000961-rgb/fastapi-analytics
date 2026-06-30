import os
from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, db=0, decode_responses=True)


@app.get("/healthz")
async def healthz():
    try:
        pong = r.ping()
        return {"status": "ok", "redis": "up" if pong else "down"}
    except Exception:
        return {"status": "ok", "redis": "down"}


@app.post("/hit/{key}")
async def hit(key: str):
    count = r.incr(f"counter:{key}")
    return {"key": key, "count": count}


@app.get("/count/{key}")
async def count(key: str):
    val = r.get(f"counter:{key}")
    return {"key": key, "count": int(val) if val is not None else 0}
