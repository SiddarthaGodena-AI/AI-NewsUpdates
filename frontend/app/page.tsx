"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Globe, Clock3, ChevronRight, Zap } from "lucide-react";
import { fetchSummaries } from "@/lib/api";
import { SummaryResponse, Timeframe } from "@/lib/types";
import { SummaryCard } from "@/components/summary-card";
import { Badge } from "@/components/badge";

const PRESET_TOPICS = ["Artificial Intelligence", "War", "Petrol", "Technology", "Finance"];

export default function Page() {
  const [topics, setTopics] = useState<string[]>(["Artificial Intelligence", "Finance"]);
  const [customTopic, setCustomTopic] = useState("");
  const [timeframe, setTimeframe] = useState<Timeframe>("daily");
  const [region, setRegion] = useState("global");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<SummaryResponse | null>(null);
  const [error, setError] = useState("");

  const userId = "demo-user";

  useEffect(() => {
    const saved = localStorage.getItem("smartnews-preferences");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed.topics) && parsed.topics.length) setTopics(parsed.topics);
        if (parsed.region) setRegion(parsed.region);
        if (parsed.timeframe) setTimeframe(parsed.timeframe);
      } catch {}
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("smartnews-preferences", JSON.stringify({ topics, region, timeframe }));
  }, [topics, region, timeframe]);

  const canRun = topics.length > 0 && !loading;

  const toggleTopic = (topic: string) => {
    setTopics((prev) => (prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]));
  };

  const addCustomTopic = () => {
    const t = customTopic.trim();
    if (!t) return;
    setTopics((prev) => (prev.includes(t) ? prev : [...prev, t]));
    setCustomTopic("");
  };

  const run = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetchSummaries({ userId, topics, timeframe, region });
      setData(res);
    } catch (e: any) {
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const recommendations = useMemo(() => data?.recommendations || [], [data]);

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.12),_transparent_35%),radial-gradient(circle_at_right,_rgba(168,85,247,0.14),_transparent_25%)]">
      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
        <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <motion.section initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-soft backdrop-blur">
            <div className="flex flex-wrap items-center gap-3">
              <Badge tone="violet">SmartNews AI</Badge>
              <Badge tone="blue">Client demo ready</Badge>
            </div>
            <h1 className="mt-5 text-4xl font-bold tracking-tight text-white md:text-6xl">
              Premium AI news briefs for the topics that matter.
            </h1>
            <p className="mt-4 max-w-2xl text-lg leading-8 text-slate-300">
              Generate a 2-minute read from full article pages, sorted by daily, weekly, or monthly views, with source validation, sentiment, bias, and audio playback.
            </p>

            <div className="mt-8 grid gap-4 md:grid-cols-3">
              <Control label="Timeframe">
                <select value={timeframe} onChange={(e) => setTimeframe(e.target.value as Timeframe)} className="w-full bg-transparent outline-none">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </Control>
              <Control label="Region">
                <select value={region} onChange={(e) => setRegion(e.target.value)} className="w-full bg-transparent outline-none">
                  <option value="global">Global</option>
                  <option value="india">India</option>
                  <option value="us">US</option>
                  <option value="uk">UK</option>
                  <option value="eu">EU</option>
                </select>
              </Control>
              <Control label="Topic search">
                <div className="flex gap-2">
                  <input
                    value={customTopic}
                    onChange={(e) => setCustomTopic(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && addCustomTopic()}
                    placeholder="Add custom topic"
                    className="w-full bg-transparent outline-none placeholder:text-slate-500"
                  />
                  <button onClick={addCustomTopic} className="rounded-xl bg-slate-200 px-3 py-2 text-sm font-semibold text-slate-950">
                    Add
                  </button>
                </div>
              </Control>
            </div>

            <div className="mt-6">
              <p className="text-sm font-medium text-slate-300">Preset topics</p>
              <div className="mt-3 flex flex-wrap gap-3">
                {PRESET_TOPICS.map((topic) => (
                  <button
                    key={topic}
                    onClick={() => toggleTopic(topic)}
                    className={`rounded-full border px-4 py-2 text-sm transition ${
                      topics.includes(topic)
                        ? "border-sky-400 bg-sky-400/15 text-sky-100"
                        : "border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
                    }`}
                  >
                    {topic}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-8 flex flex-wrap items-center gap-4">
              <button
                disabled={!canRun}
                onClick={run}
                className="inline-flex items-center gap-2 rounded-2xl bg-white px-6 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Sparkles className="h-4 w-4" />
                Generate briefing
              </button>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <Globe className="h-4 w-4" />
                Geo-filtered and source-validated
              </div>
            </div>
          </motion.section>

          <section className="grid gap-6">
            <div className="rounded-[2rem] border border-white/10 bg-slate-900/70 p-6 shadow-soft">
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <Zap className="h-4 w-4" /> Upgrade highlights
              </div>
              <div className="mt-4 grid gap-3">
                {[
                  "Multi-source validation with confidence scoring",
                  "Audio news mode using browser speech synthesis",
                  "Sentiment and bias indicators per topic",
                  "Personalized topic recommendations",
                ].map((x) => (
                  <div key={x} className="rounded-2xl bg-white/5 p-4 text-sm text-slate-200">
                    {x}
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-soft">
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <Clock3 className="h-4 w-4" /> Current configuration
              </div>
              <div className="mt-4 space-y-2 text-sm text-slate-200">
                <div>Topics: {topics.join(", ")}</div>
                <div>Timeframe: {timeframe}</div>
                <div>Region: {region}</div>
              </div>
            </div>
          </section>
        </div>

        {error ? (
          <div className="mt-6 rounded-2xl border border-rose-400/30 bg-rose-500/10 p-4 text-rose-100">{error}</div>
        ) : null}

        {loading ? (
          <div className="mt-8 grid gap-4">
            {[1, 2].map((i) => (
              <div key={i} className="h-64 animate-pulse rounded-[2rem] border border-white/10 bg-white/5" />
            ))}
          </div>
        ) : null}

        {data ? (
          <div className="mt-8 grid gap-4">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-soft">
              <div className="flex flex-wrap items-center gap-3">
                <Badge tone="emerald">Recommendations</Badge>
                {recommendations.map((r) => (
                  <Badge key={r}>{r}</Badge>
                ))}
              </div>
            </div>
            {data.results.map((item) => (
              <SummaryCard key={`${item.topic}-${item.timeframe}`} item={item} />
            ))}
          </div>
        ) : (
          <div className="mt-8 rounded-[2rem] border border-dashed border-white/15 bg-white/5 p-8 text-slate-300">
            Choose topics and generate a premium news briefing.
          </div>
        )}

        <footer className="mt-10 flex items-center justify-between border-t border-white/10 pt-6 text-sm text-slate-500">
          <div>Built for client pitching and live demo stability.</div>
          <div className="inline-flex items-center gap-2">
            <ChevronRight className="h-4 w-4" /> SmartNews AI
          </div>
        </footer>
      </div>
    </main>
  );
}

function Control({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
      <span className="mb-2 block text-xs uppercase tracking-[0.2em] text-slate-400">{label}</span>
      {children}
    </label>
  );
}
