"""
The Good Neighbor Guard — Kindness Chain
Built by Christopher Hughes · Sacramento, CA
Created with the help of AI collaborators (Claude · GPT · Gemini · Groq)
Truth · Safety · We Got Your Back
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
import time
import uuid
from datetime import datetime, timezone

app = FastAPI(title="Kindness Chain — The Good Neighbor Guard")

DATA_FILE = "kindness_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"acts": [], "total_count": 0}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class KindnessAct(BaseModel):
    message: str
    author: Optional[str] = "A Good Neighbor"
    category: Optional[str] = "general"

class LightAct(BaseModel):
    act_id: str

CATEGORIES = {
    "neighbor": "🏠 Neighbor",
    "stranger": "🌍 Stranger",
    "family": "❤️ Family",
    "community": "🤝 Community",
    "nature": "🌿 Nature",
    "general": "✨ General",
}

@app.get("/api/acts")
def get_acts(limit: int = 20, offset: int = 0):
    data = load_data()
    acts = sorted(data["acts"], key=lambda x: x.get("lights", 0) + x.get("timestamp", 0), reverse=True)
    return {
        "acts": acts[offset:offset+limit],
        "total": len(data["acts"]),
        "chain_count": data.get("total_count", 0)
    }

@app.get("/api/recent")
def get_recent(limit: int = 5):
    data = load_data()
    acts = sorted(data["acts"], key=lambda x: x.get("timestamp", 0), reverse=True)
    return {"acts": acts[:limit]}

@app.post("/api/acts")
def add_act(act: KindnessAct):
    if not act.message or len(act.message.strip()) < 5:
        raise HTTPException(status_code=400, detail="Message too short")
    if len(act.message) > 280:
        raise HTTPException(status_code=400, detail="Message too long (max 280 chars)")
    
    data = load_data()
    
    new_act = {
        "id": str(uuid.uuid4()),
        "message": act.message.strip(),
        "author": (act.author or "A Good Neighbor").strip()[:50],
        "category": act.category if act.category in CATEGORIES else "general",
        "category_label": CATEGORIES.get(act.category, "✨ General"),
        "timestamp": time.time(),
        "date": datetime.now(timezone.utc).strftime("%B %d, %Y"),
        "lights": 0,
    }
    
    data["acts"].append(new_act)
    data["total_count"] = data.get("total_count", 0) + 1
    save_data(data)
    
    return {"success": True, "act": new_act, "chain_count": data["total_count"]}

@app.post("/api/light")
def light_an_act(payload: LightAct):
    data = load_data()
    for act in data["acts"]:
        if act["id"] == payload.act_id:
            act["lights"] = act.get("lights", 0) + 1
            save_data(data)
            return {"success": True, "lights": act["lights"]}
    raise HTTPException(status_code=404, detail="Act not found")

@app.get("/api/stats")
def get_stats():
    data = load_data()
    total = len(data["acts"])
    total_lights = sum(a.get("lights", 0) for a in data["acts"])
    cats = {}
    for a in data["acts"]:
        c = a.get("category", "general")
        cats[c] = cats.get(c, 0) + 1
    return {
        "total_acts": total,
        "total_lights": total_lights,
        "chain_count": data.get("total_count", 0),
        "categories": cats,
    }

@app.get("/api/categories")
def get_categories():
    return CATEGORIES

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
