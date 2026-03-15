# 🌿 Kindness Chain — The Good Neighbor Guard

> Built by Claude for the Battle of the AIs experiment  
> Christopher Hughes · Sacramento, CA  
> Truth · Safety · We Got Your Back

---

## What is this?

**Kindness Chain** is a community board where people share real acts of kindness — things they did, witnessed, or received. Others can "light a candle" (like) the ones that move them.

No algorithms. No ads. No negativity. Just a growing chain of good.

**Features:**
- Post an act of kindness (280 chars, like a kindness tweet)
- Category tags: Neighbor, Stranger, Family, Community, Nature
- Light a candle 🕯️ for acts that inspire you
- Live chain counter — watch the total grow
- Auto-seeding with real starter entries so it never looks empty
- No login required. No accounts. Just goodness.

---

## Deploy to Render

1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Done ✅

---

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# Open http://localhost:8000
```

---

*No AI API costs. Zero. Pure FastAPI + vanilla JS + a JSON file.*  
*Deployable in under 5 minutes.*
