from __future__ import annotations

from typing import Dict, List

from ..database import get_usage_counts


def recommend_topics(user_id: str, seed_topics: List[str]) -> List[str]:
    usage = get_usage_counts(user_id)
    ranked = sorted(usage.items(), key=lambda x: x[1], reverse=True)
    ordered = [topic for topic, _ in ranked]

    for topic in seed_topics:
        if topic not in ordered:
            ordered.append(topic)

    extra = ["technology", "finance", "artificial intelligence", "petrol", "war"]
    for topic in extra:
        if topic not in ordered:
            ordered.append(topic)

    return ordered[:6]
