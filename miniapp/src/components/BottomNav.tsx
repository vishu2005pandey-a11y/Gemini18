"use client";
import { Home, Grid3x3, Package, Wallet, User } from "lucide-react";
import { haptic } from "@/lib/twa";

export type Tab = "home" | "browse" | "orders" | "wallet" | "account" | "leaderboard" | "referral";

interface Props {
  active: Tab;
  onChange: (tab: Tab) => void;
}

const tabs = [
  { id: "home",    label: "Home",    Icon: Home },
  { id: "browse",  label: "Browse",  Icon: Grid3x3 },
  { id: "orders",  label: "Orders",  Icon: Package },
  { id: "wallet",  label: "Wallet",  Icon: Wallet },
  { id: "account", label: "Account", Icon: User },
] as const;

// Tabs shown in bottom nav (main 5 only)
type MainTab = "home" | "browse" | "orders" | "wallet" | "account";
const MAIN_TABS = new Set<string>(["home", "browse", "orders", "wallet", "account"]);

export default function BottomNav({ active, onChange }: Props) {
  // Highlight account tab when on leaderboard/referral sub-pages
  const getActive = (id: string): boolean => {
    if (id === "account" && (active === "leaderboard" || active === "referral")) return true;
    return id === active;
  };

  return (
    <nav className="bottom-nav fixed bottom-0 left-0 right-0 z-50 flex justify-around items-center h-16 px-2">
      {tabs.map(({ id, label, Icon }) => (
        <button
          key={id}
          onClick={() => { haptic("light"); onChange(id as MainTab); }}
          className={`nav-item flex-1 py-2 ${getActive(id) ? "active" : ""}`}
        >
          <Icon
            size={22}
            strokeWidth={getActive(id) ? 2.2 : 1.8}
            className={getActive(id) ? "text-[#6c63ff]" : "text-[#555566]"}
          />
          <span className={getActive(id) ? "text-[#6c63ff]" : "text-[#555566]"}>
            {label}
          </span>
        </button>
      ))}
    </nav>
  );
}
