export type Timeframe = "daily" | "weekly" | "monthly";

export type SummaryResult = {
  topic: string;
  timeframe: string;
  title: string;
  key_highlights: string[];
  summary: string;
  why_it_matters: string;
  sources: number;
  confidence: number;
  sentiment: "Positive" | "Negative" | "Neutral";
  sentiment_score: number;
  bias: "Low" | "Medium" | "High";
  articles: {
    title: string;
    source: string;
    published_at: string;
    description: string;
    url: string;
  }[];
};

export type SummaryResponse = {
  user_id: string;
  region: string;
  timeframe: Timeframe;
  recommendations: string[];
  results: SummaryResult[];
};
