"use client";

import { motion } from "framer-motion";
import { Badge } from "./badge";
import { BarChart3, Brain, Link2, Volume2 } from "lucide-react";
import { SummaryResult } from "@/lib/types";
import { useMemo, useState } from "react";

export function SummaryCard({ item }: { item: SummaryResult }) {
  const [speaking, setSpeaking] = useState(false);

  const tone = useMemo(() => {
    if (item.sentiment === "Positive") return "emerald";
    if (item.sentiment === "Negative") return "rose";
    return "blue";
  }, [item.sentiment]);

  const speak = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const text = `${item.title}. ${item.summary}. Why it matters: ${item.why_it_matters}`;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.02;
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-soft backdrop-blur"
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex flex-wrap gap-2">
            <Badge tone="violet">Live scraped article text</Badge>
            <Badge tone="amber">{item.sources} sources</Badge>
          </div>
          <p className="mt-3 text-xs uppercase tracking-[0.3em] text-slate-400">{item.timeframe}</p>
          <h3 className="mt-2 text-2xl font-semibold text-white">{item.topic}</h3>
          <p className="mt-1 text-sm text-slate-300">{item.title}</p>
        </div>
        <div className="flex gap-2">
          <Badge tone={tone}>{item.sentiment}</Badge>
          <Badge tone="violet">Bias {item.bias}</Badge>
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl bg-slate-900/70 p-4">
          <div className="mb-3 flex items-center gap-2 text-sm text-slate-300">
            <Brain className="h-4 w-4" /> Summarized from full article pages
          </div>
          <p className="leading-7 text-slate-200">{item.summary}</p>
          <div className="mt-4">
            <p className="mb-2 text-sm font-medium text-slate-300">Key highlights</p>
            <ul className="space-y-2">
              {item.key_highlights.map((x) => (
                <li key={x} className="flex gap-2 text-sm text-slate-200">
                  <span className="mt-2 h-2 w-2 rounded-full bg-sky-400" />
                  <span>{x}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/70 p-4">
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <BarChart3 className="h-4 w-4" /> Intelligence panel
          </div>
          <div className="mt-4 space-y-4">
            <div>
              <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
                <span>Confidence</span>
                <span>{Math.round(item.confidence * 100)}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-gradient-to-r from-sky-400 to-violet-400" style={{ width: `${item.confidence * 100}%` }} />
              </div>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Why it matters</p>
              <p className="mt-2 text-sm leading-6 text-slate-200">{item.why_it_matters}</p>
            </div>
            <button
              onClick={speaking ? () => window.speechSynthesis?.cancel() : speak}
              className="inline-flex items-center gap-2 rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.02]"
            >
              <Volume2 className="h-4 w-4" />
              {speaking ? "Stop audio" : "Play audio news"}
            </button>
            <div className="space-y-2">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Source links</p>
              {item.articles?.slice(0, 3).map((a) => (
                <a key={a.url + a.title} href={a.url} target="_blank" rel="noreferrer" className="flex items-start gap-2 rounded-xl border border-white/10 bg-white/5 p-3 text-xs text-slate-200 hover:bg-white/10">
                  <Link2 className="mt-0.5 h-3.5 w-3.5 shrink-0" />
                  <span>{a.title || a.url}</span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
