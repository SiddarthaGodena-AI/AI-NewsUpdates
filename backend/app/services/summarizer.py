from __future__ import annotations

import re
from typing import Dict, List

POSITIVE = {
    "growth", "gain", "improve", "optimistic", "strong", "success", "progress", "stability", "positive"
}
NEGATIVE = {
    "war", "loss", "risk", "fall", "decline", "concern", "crisis", "shortage", "uncertainty", "tension"
}
BIAS_MARKERS = {
    "allegedly", "reportedly", "claims", "sources say", "accused", "blames", "controversial"
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _sentences(text: str) -> List[str]:
    text = _clean(text)
    if not text:
        return []
    chunks = re.split(r"(?<=[.!?])\s+", text)
    return [c.strip() for c in chunks if c.strip()]


def _score_sentence(sentence: str, keywords: List[str]) -> float:
    s = sentence.lower()
    score = 0.0
    for kw in keywords:
        if kw in s:
            score += 2.0
    score += min(len(sentence) / 180.0, 1.0)
    return score


def _article_text(article: dict) -> str:
    # Prefer full scraped page text, then description/title
    return " ".join(
        x for x in [
            article.get("full_text", ""),
            article.get("description", ""),
            article.get("title", ""),
        ] if x
    ).strip()


def summarize_articles(topic: str, timeframe: str, articles: List[dict]) -> Dict[str, object]:
    all_text = " ".join(_article_text(a) for a in articles).strip()

    keywords = [w.lower() for w in re.findall(r"[a-zA-Z]{4,}", topic)]
    if not keywords:
        keywords = [topic.lower()]

    sent_list = _sentences(all_text)
    ranked = sorted(sent_list, key=lambda s: _score_sentence(s, keywords), reverse=True)
    summary_sents = ranked[:3] if ranked else [f"Latest coverage on {topic} remains active across multiple sources."]

    source_count = len({a.get("source", "Unknown") for a in articles})
    headlines = [a.get("title", "") for a in articles[:5]]

    text_lower = all_text.lower()
    pos = sum(text_lower.count(w) for w in POSITIVE)
    neg = sum(text_lower.count(w) for w in NEGATIVE)

    if pos > neg + 1:
        sentiment = "Positive"
        sentiment_score = 0.72
    elif neg > pos + 1:
        sentiment = "Negative"
        sentiment_score = 0.28
    else:
        sentiment = "Neutral"
        sentiment_score = 0.50

    bias_hits = sum(text_lower.count(w) for w in BIAS_MARKERS)
    bias = "Low" if bias_hits <= 1 else "Medium" if bias_hits <= 3 else "High"
    confidence = min(0.95, 0.45 + source_count * 0.08 + max(0, len(articles) - 1) * 0.03)

    key_highlights = []
    for line in headlines[:3]:
        if line and line not in key_highlights:
            key_highlights.append(line)
    if len(key_highlights) < 3:
        for s in summary_sents:
            if s not in key_highlights:
                key_highlights.append(s)
            if len(key_highlights) >= 3:
                break

    summary = " ".join(summary_sents)
    if len(summary.split()) > 70:
        summary = " ".join(summary.split()[:70]).rstrip() + "."

    why_it_matters = (
        f"This {timeframe} update matters because it affects policy, markets, or public attention around {topic}."
    )

    return {
        "topic": topic,
        "timeframe": timeframe.title(),
        "title": f"{topic.title()} — {timeframe.title()} Briefing",
        "key_highlights": key_highlights[:5],
        "summary": summary,
        "why_it_matters": why_it_matters,
        "sources": source_count,
        "confidence": round(confidence, 2),
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "bias": bias,
        "articles": articles,
    }
