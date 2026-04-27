import { SummaryResponse, Timeframe } from "./types";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function fetchSummaries(input: {
  userId: string;
  topics: string[];
  timeframe: Timeframe;
  region: string;
}): Promise<SummaryResponse> {
  const res = await fetch(`${BACKEND}/api/summaries`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: input.userId,
      topics: input.topics,
      timeframe: input.timeframe,
      region: input.region,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to fetch summaries");
  }

  return res.json();
}
