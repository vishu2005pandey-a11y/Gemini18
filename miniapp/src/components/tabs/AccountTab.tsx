"use client";
import { Gift, HelpCircle, LogOut, ChevronRight, Trophy } from "lucide-react";
import { haptic, closeMiniApp, getTWA } from "@/lib/twa";
import { UserInfo } from "@/lib/api";

interface Props {
  user: { id?: number; first_name?: string; last_name?: string; username?: string } | null;
  userInfo: UserInfo | null;
  onReferral: () => void;
  onLeaderboard: () => void;
}

export default function AccountTab({ user, userInfo, onReferral, onLeaderboard }: Props) {
  const firstName = userInfo?.first_name || user?.first_name || "Alpha";
  const lastName = user?.last_name || "";
  const name = lastName ? `${firstName} ${lastName}` : firstName;
  const username = userInfo?.username || user?.username;
  const initials = name.charAt(0).toUpperCase();

  const badge = userInfo?.badge || "🆕 New Member";
  const totalOrders = userInfo?.total_orders ?? 0;
  const linksBought = userInfo?.links_bought ?? 0;
  const totalSpent = userInfo?.total_spent ?? 0;
  const referralBalance = userInfo?.referral_balance ?? 0;

  const openSupport = () => {
    haptic("light");
    const twa = getTWA();
    if (twa) {
      twa.openTelegramLink("https://t.me/GammaChkerbot");
    }
  };

  const menuItems = [
    {
      icon: Gift,
      label: "Refer & Earn",
      sub: `Invite friends — earn commission. Balance: $${referralBalance.toFixed(2)}`,
      iconColor: "#6c63ff",
      iconBg: "#6c63ff22",
      action: onReferral,
    },
    {
      icon: Trophy,
      label: "Leaderboard",
      sub: "See top buyers and rankings",
      iconColor: "#fbbf24",
      iconBg: "#fbbf2422",
      action: onLeaderboard,
    },
    {
      icon: HelpCircle,
      label: "Help & Support",
      sub: "FAQs and contact our team on Telegram",
      iconColor: "#4f8eff",
      iconBg: "#4f8eff22",
      action: openSupport,
    },
  ];

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Account</h1>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* User info */}
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-white font-bold text-2xl flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}
          >
            {initials}
          </div>
          <div>
            <p className="text-white font-bold text-lg leading-tight">{name}</p>
            {username && <p className="text-[#8888aa] text-sm">@{username}</p>}
            {/* Badge */}
            <span
              className="inline-block mt-1 text-xs px-2.5 py-0.5 rounded-full font-medium"
              style={{
                background: "linear-gradient(135deg, #6c63ff22 0%, #4f8eff22 100%)",
                border: "1px solid #6c63ff44",
                color: "#6c63ff",
              }}
            >
              {badge}
            </span>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { label: "Orders", value: totalOrders.toString() },
            { label: "Links", value: linksBought.toString() },
            { label: "Spent", value: `$${totalSpent.toFixed(2)}` },
          ].map(({ label, value }) => (
            <div key={label} className="card p-3 flex flex-col items-center gap-0.5">
              <p className="text-white font-bold text-base">{value}</p>
              <p className="text-[#555566] text-[11px]">{label}</p>
            </div>
          ))}
        </div>

        {/* Menu */}
        <div className="card divide-y divide-[#2a2a3a]">
          {menuItems.map(({ icon: Icon, label, sub, iconColor, iconBg, action }) => (
            <button
              key={label}
              onClick={() => { haptic("light"); action(); }}
              className="w-full flex items-center gap-4 p-4 text-left active:bg-[#1a1a24] transition-colors"
            >
              <div
                className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                style={{ background: iconBg }}
              >
                <Icon size={18} style={{ color: iconColor }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white font-medium text-sm">{label}</p>
                <p className="text-[#555566] text-xs truncate">{sub}</p>
              </div>
              <ChevronRight size={16} className="text-[#555566] flex-shrink-0" />
            </button>
          ))}
        </div>

        {/* Referral balance highlight */}
        {referralBalance > 0 && (
          <div
            className="rounded-2xl p-4 flex items-center justify-between"
            style={{ background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)", border: "1px solid #6c63ff44" }}
          >
            <div>
              <p className="text-[#6c63ff] text-xs font-semibold uppercase tracking-wide">Referral Balance</p>
              <p className="text-white font-bold text-xl">${referralBalance.toFixed(2)}</p>
              <p className="text-[#555566] text-xs mt-0.5">Available to withdraw from $3.00</p>
            </div>
            <div className="text-3xl">💰</div>
          </div>
        )}

        {/* Sign out */}
        <button
          onClick={() => { haptic("light"); closeMiniApp(); }}
          className="flex items-center gap-2 text-[#ff4f6e] font-medium py-2 px-4"
        >
          <LogOut size={16} />
          <span>Close Mini App</span>
        </button>

        <p className="text-center text-[#555566] text-xs pb-4">Alpha Shop · v1.0</p>
      </div>
    </div>
  );
}
