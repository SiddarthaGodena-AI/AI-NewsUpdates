from __future__ import annotations

from typing import Dict, List

SAMPLE_ARTICLES: Dict[str, List[dict]] = {
    "artificial intelligence": [
        {
            "title": "AI companies accelerate model deployment in enterprise workflows",
            "source": "Tech Pulse",
            "published_at": "2026-04-28T06:00:00Z",
            "description": "Organizations are expanding AI assistants into customer support, document review, and code generation.",
            "url": "#",
        },
        {
            "title": "Regulators discuss guardrails for high-risk AI systems",
            "source": "Policy Daily",
            "published_at": "2026-04-27T12:00:00Z",
            "description": "New proposals focus on transparency, safety testing, and accountability for foundation models.",
            "url": "#",
        },
    ],
    "war": [
        {
            "title": "Diplomatic talks continue amid regional tensions",
            "source": "World Brief",
            "published_at": "2026-04-28T03:00:00Z",
            "description": "Officials emphasize ceasefire monitoring, aid access, and civilian protection.",
            "url": "#",
        },
        {
            "title": "Humanitarian groups warn of supply shortages",
            "source": "Global Report",
            "published_at": "2026-04-26T09:00:00Z",
            "description": "Displacement and logistics barriers remain the main concerns in affected zones.",
            "url": "#",
        },
    ],
    "petrol": [
        {
            "title": "Crude price movement impacts fuel retail sentiment",
            "source": "Energy Desk",
            "published_at": "2026-04-28T05:30:00Z",
            "description": "Supply expectations and refinery margins influence petrol price outlooks.",
            "url": "#",
        },
        {
            "title": "Energy markets watch inventory data closely this week",
            "source": "Market Wire",
            "published_at": "2026-04-25T11:00:00Z",
            "description": "Analysts expect volatility as traders react to geopolitical supply signals.",
            "url": "#",
        },
    ],
    "technology": [
        {
            "title": "Cloud infrastructure spending remains strong",
            "source": "Infra Daily",
            "published_at": "2026-04-28T07:00:00Z",
            "description": "Demand for AI-ready compute and storage continues to drive investment.",
            "url": "#",
        }
    ],
    "finance": [
        {
            "title": "Markets price in cautious growth outlook",
            "source": "Finance Now",
            "published_at": "2026-04-28T04:00:00Z",
            "description": "Investors focus on inflation data, interest rates, and earnings guidance.",
            "url": "#",
        }
    ],
}

DEFAULT_ARTICLES = [
    {
        "title": "Global markets react to mixed macroeconomic signals",
        "source": "Daily Brief",
        "published_at": "2026-04-28T06:00:00Z",
        "description": "Analysts remain focused on inflation, policy, and earnings across sectors.",
        "url": "#",
    }
]
