# AI-NewsUpdates
SmartNews AI – Backend API  An intelligent, production-ready AI-powered news aggregation and summarization backend built with FastAPI. It fetches real-time news, enriches content, summarizes articles, and personalizes recommendations based on user behavior.

🚀 Features
📰 News Aggregation
Fetches news from multiple sources:
NewsAPI
GNews
Google News RSS (fallback scraping)
Topic normalization (AI, War, Petrol, etc.)
Region-based filtering (India, US, Global, etc.)
Timeframe filtering (Daily / Weekly / Monthly)

🧠 AI Summarization
Converts raw news into concise, high-quality summaries
Supports multiple topics in a single request
Designed for clean frontend consumption

🎯 Personalization Engine
Tracks user behavior (topic usage)
Recommends topics dynamically
Stores user preferences:
Topics
Region
Default timeframe

🗄️ Lightweight Database
Uses SQLite for:
User preferences
Topic usage tracking
Thread-safe operations with locking

🌐 API-First Design
RESTful endpoints
CORS enabled for frontend integration
Scalable architecture (service-based modules)

🏗️ Project Structure
backend/
│
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── database.py            # SQLite DB operations
│   ├── schemas.py             # Request/response models
│   │
│   ├── services/
│   │   ├── news_service.py    # News fetching & scraping
│   │   ├── summarizer.py      # AI summarization logic
│   │   ├── personalization.py # Recommendation engine
│   │
│   └── sample_data.py         # Fallback articles
│
└── smartnews.db               # SQLite database

⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/your-username/smartnews-ai.git
cd smartnews-ai/backend

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Environment Variables
Create a .env file:
NEWSAPI_KEY=your_newsapi_key
GNEWS_KEY=your_gnews_key

⚠️ If keys are not provided, system falls back to scraping + sample data.

▶️ Run the Server
uvicorn app.main:app --reload
Server will start at:
http://127.0.0.1:8000

📡 API Endpoints
✅ Health Check
GET /health

📚 Get Available Topics
GET /api/topics

⚙️ Save User Preferences
POST /api/preferences
{
  "user_id": "user123",
  "topics": ["AI", "Technology"],
  "region": "india",
  "default_timeframe": "daily"
}

📥 Get User Preferences
GET /api/preferences/{user_id}

📊 Track User Activity
POST /api/usage

🧠 Generate News Summaries
POST /api/summaries
{
  "user_id": "user123",
  "topics": ["AI", "Finance"],
  "timeframe": "daily",
  "region": "india"
}
Response:
{
  "user_id": "user123",
  "recommendations": ["Technology", "Business"],
  "results": [
    {
      "topic": "AI",
      "summary": "...",
      "articles": [...]
    }
  ]
}

🧩 Core Components Explained
🔹 news_service.py
Multi-source news fetching
RSS scraping fallback
Full article content extraction using BeautifulSoup

🔹 summarizer.py
Converts articles → structured summaries
Designed for AI integration (LLMs)

🔹 personalization.py
Recommends topics based on:
User history
Frequency of usage

🔹 database.py
SQLite-based persistence
Thread-safe operations

🧠 How It Works
User selects topics
System fetches news from APIs/scrapers
Filters by timeframe & region
Extracts full article content
Summarizes articles
Tracks usage
Recommends new topics

🛠️ Tech Stack
Backend: FastAPI
Database: SQLite
Web Scraping: BeautifulSoup
HTTP Requests: Requests
AI Ready: Plug-and-play summarization layer
Deployment Ready: Uvicorn / ASGI
