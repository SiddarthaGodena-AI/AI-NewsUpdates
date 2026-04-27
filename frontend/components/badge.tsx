import React from "react";

export function Badge({
  children,
  tone = "slate",
}: {
  children: React.ReactNode;
  tone?: "slate" | "blue" | "emerald" | "amber" | "rose" | "violet";
}) {
  const tones: Record<string, string> = {
    slate: "bg-slate-800 text-slate-200 ring-slate-700",
    blue: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
    emerald: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
    amber: "bg-amber-500/15 text-amber-200 ring-amber-400/30",
    rose: "bg-rose-500/15 text-rose-200 ring-rose-400/30",
    violet: "bg-violet-500/15 text-violet-200 ring-violet-400/30",
  };
  return (
    <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ring-1 ${tones[tone]}`}>
      {children}
    </span>
  );
}
