"use client";
import { useState, useEffect } from "react";
import { Copy, Users, Gift, TrendingUp } from "lucide-react";
import { getReferral, ReferralStats } from "@/lib/api";
import { haptic, getTWA } from "@/lib/twa";

interface Props {
  userId: number | null;
}

export default function ReferralTab({ userId }: Props) {
  const [stats, setStats] = useState<ReferralStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  const botUsername = process.env.NEXT_PUBLIC_BOT_USERNAME || "GammaChkerbot";
  const referralLink = userId
    ? `https://t.me/${botUsername}?start=ref${userId}`
    : "";

  useEffect(() => {
    if (!userId) { setLoading(false); return; }
    getReferral(userId).then((data) => {
      setStats(data);
      setLoading(false);
    });
  }, [userId]);

  const copyLink = async () => {
    if (!referralLink) return;
    try {
      await navigator.clipboard.writeText(referralLink);
      haptic("light");
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // fallback
    }
  };

  const shareLink = () => {
    haptic("medium");
    const twa = getTWA();
    if (twa) {
      twa.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=${encodeURIComponent("🤖 Visit our store and buy premium digital products!")}`);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col gap-4 pb-4">
        <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
          <h1 className="text-white font-bold text-xl">Refer & Earn</h1>
        </div>
        <div className="flex items-center justify-center py-12">
          <div className="w-8 h-8 rounded-full border-2 border-[#6c63ff] border-t-transparent animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Refer & Earn</h1>
        <p className="text-[#555566] text-sm mt-0.5">Earn $0.50 per friend who joins</p>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Hero banner */}
        <div
          className="rounded-2xl p-5 flex flex-col gap-3"
          style={{ background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)", border: "1px solid #6c63ff44" }}
        >
          <div className="w-12 h-12 rounded-2xl flex items-center justify-center"
            style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}>
            <Gift size={24} className="text-white" />
          </div>
          <div>
            <p className="text-white font-bold text-lg leading-tight">Invite Friends</p>
            <p className="text-[#8888aa] text-sm mt-1">
              Share your referral link. For every friend who joins the bot,
              you earn <span className="text-[#6c63ff] font-semibold">$0.50</span> — no purchase needed.
            </p>
          </div>
          <p className="text-[#555566] text-xs">Withdraw from $3.00 minimum</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { label: "Invited", value: stats?.total_invited ?? 0, icon: Users },
            { label: "Converted", value: stats?.successful ?? 0, icon: TrendingUp },
            { label: "Earned", value: `$${(stats?.total_earnings ?? 0).toFixed(2)}`, icon: Gift },
          ].map(({ label, value, icon: Icon }) => (
            <div key={label} className="card p-3 flex flex-col items-center gap-1.5">
              <Icon size={16} className="text-[#6c63ff]" />
              <span className="text-white font-bold text-sm">{value}</span>
              <span className="text-[#555566] text-[10px]">{label}</span>
            </div>
          ))}
        </div>

        {/* Available balance */}
        <div className="card p-4 flex items-center justify-between">
          <div>
            <p className="text-[#8888aa] text-xs">Available Balance</p>
            <p className="text-white font-bold text-xl">
              ${(stats?.available_balance ?? 0).toFixed(2)}
            </p>
          </div>
          <div className="px-2 py-0.5 rounded-full text-xs"
            style={{ background: "linear-gradient(135deg, #6c63ff22 0%, #4f8eff22 100%)", border: "1px solid #6c63ff44", color: "#6c63ff" }}>
            USDT
          </div>
        </div>

        {/* Referral link */}
        <div className="card p-4 flex flex-col gap-3">
          <p className="text-white font-semibold text-sm">Your Referral Link</p>
          <div className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-4 py-3">
            <p className="flex-1 text-[#8888aa] text-xs font-mono truncate">{referralLink}</p>
            <button
              onClick={copyLink}
              className={`flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all
                ${copied ? "bg-[#22d3a522] text-[#22d3a5]" : "bg-[#2a2a3a] text-[#8888aa]"}`}
            >
              <Copy size={12} />
              {copied ? "Copied!" : "Copy"}
            </button>
          </div>

          <button
            onClick={shareLink}
            className="w-full btn-primary py-3 text-sm flex items-center justify-center gap-2"
          >
            <Users size={16} />
            Share on Telegram
          </button>
        </div>

        {/* How it works */}
        <div className="card p-4 flex flex-col gap-3">
          <p className="text-white font-semibold text-sm">How it works</p>
          {[
            { n: "1", text: "Share your link with friends" },
            { n: "2", text: "Friend clicks and starts the bot" },
            { n: "3", text: "You earn $0.50 automatically" },
          ].map(({ n, text }) => (
            <div key={n} className="flex items-center gap-3">
              <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}>
                {n}
              </div>
              <p className="text-[#8888aa] text-sm">{text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
