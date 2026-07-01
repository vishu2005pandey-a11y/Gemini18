"use client";
import { useState, useEffect } from "react";
import { Trophy } from "lucide-react";
import { getLeaderboard, LeaderboardEntry } from "@/lib/api";
import { haptic } from "@/lib/twa";

type Period = "weekly" | "monthly" | "alltime";

const MEDAL = ["🥇", "🥈", "🥉"];

export default function LeaderboardTab() {
  const [period, setPeriod] = useState<Period>("alltime");
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getLeaderboard(period).then((data) => {
      setEntries(data);
      setLoading(false);
    });
  }, [period]);

  const tabs: { label: string; value: Period }[] = [
    { label: "Weekly", value: "weekly" },
    { label: "Monthly", value: "monthly" },
    { label: "All Time", value: "alltime" },
  ];

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <div className="flex items-center gap-2">
          <Trophy size={20} className="text-[#6c63ff]" />
          <h1 className="text-white font-bold text-xl">Leaderboard</h1>
        </div>
        <p className="text-[#555566] text-sm mt-0.5">Top buyers by links purchased</p>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Period tabs */}
        <div className="flex gap-2 bg-[#111118] border border-[#2a2a3a] p-1 rounded-xl">
          {tabs.map((t) => (
            <button
              key={t.value}
              onClick={() => { haptic("light"); setPeriod(t.value); }}
              className={`flex-1 py-2 rounded-lg text-sm font-semibold transition-all
                ${period === t.value
                  ? "text-white"
                  : "text-[#555566]"
                }`}
              style={period === t.value
                ? { background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }
                : {}}
            >
              {t.label}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-8 h-8 rounded-full border-2 border-[#6c63ff] border-t-transparent animate-spin" />
          </div>
        ) : entries.length === 0 ? (
          <div className="card p-10 flex flex-col items-center gap-3 text-center">
            <Trophy size={32} className="text-[#2a2a3a]" />
            <p className="text-[#555566] text-sm">No data for this period yet</p>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            {entries.map((entry, idx) => (
              <div
                key={idx}
                className={`card p-4 flex items-center gap-4
                  ${idx === 0 ? "border border-[#fbbf2444]" : ""}
                `}
              >
                <div className="w-10 flex items-center justify-center text-xl flex-shrink-0">
                  {idx < 3 ? MEDAL[idx] : <span className="text-[#555566] font-bold text-sm">#{idx + 1}</span>}
                </div>
                <div
                  className="w-9 h-9 rounded-full flex items-center justify-center font-bold text-white flex-shrink-0"
                  style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}
                >
                  {(entry.first_name || entry.username || "?").charAt(0).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white font-semibold text-sm truncate">
                    {entry.first_name || entry.username || "Anonymous"}
                  </p>
                  {entry.username && (
                    <p className="text-[#555566] text-xs">@{entry.username}</p>
                  )}
                </div>
                <div className="text-right flex-shrink-0">
                  <p className="text-[#6c63ff] font-bold">{entry.total_links.toLocaleString()}</p>
                  <p className="text-[#555566] text-xs">links</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
