from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import get_preferences, init_db, record_topic_usage, save_preferences
from .schemas import PreferencesRequest, SaveUsageRequest, SummaryRequest
from .services.news_service import get_articles
from .services.personalization import recommend_topics
from .services.summarizer import summarize_articles

app = FastAPI(title="SmartNews AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/topics")
def topics():
    return {
        "topics": [
            "Artificial Intelligence",
            "War",
            "Petrol",
            "Technology",
            "Finance",
            "Business",
            "Sports",
            "Politics",
        ],
        "regions": ["global", "india", "us", "uk", "eu"],
        "timeframes": ["daily", "weekly", "monthly"],
    }


@app.post("/api/preferences")
def set_preferences(req: PreferencesRequest):
    save_preferences(
        req.user_id,
        {
            "topics": req.topics,
            "region": req.region,
            "default_timeframe": req.default_timeframe,
        },
    )
    return {"ok": True}


@app.get("/api/preferences/{user_id}")
def get_preferences_api(user_id: str):
    return get_preferences(user_id)


@app.post("/api/usage")
def usage(req: SaveUsageRequest):
    record_topic_usage(req.user_id, req.topic, req.timeframe, req.region)
    return {"ok": True}


@app.post("/api/summaries")
def summaries(req: SummaryRequest):
    if not req.topics:
        raise HTTPException(status_code=400, detail="At least one topic is required")

    results = []
    for topic in req.topics:
        articles = get_articles(topic, req.timeframe, req.region)
        result = summarize_articles(topic, req.timeframe, articles)
        results.append(result)
        record_topic_usage(req.user_id, topic, req.timeframe, req.region)

    return {
        "user_id": req.user_id,
        "region": req.region,
        "timeframe": req.timeframe,
        "recommendations": recommend_topics(req.user_id, req.topics),
        "results": results,
    }
