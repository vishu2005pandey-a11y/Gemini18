"use client";
import { Home, Grid3x3, Package, Wallet, User } from "lucide-react";
import { haptic } from "@/lib/twa";

interface Props {
  active: "home" | "browse" | "orders" | "wallet" | "account";
  onChange: (tab: "home" | "browse" | "orders" | "wallet" | "account") => void;
}

const tabs = [
  { id: "home",    label: "Home",    Icon: Home },
  { id: "browse",  label: "Browse",  Icon: Grid3x3 },
  { id: "orders",  label: "Orders",  Icon: Package },
  { id: "wallet",  label: "Wallet",  Icon: Wallet },
  { id: "account", label: "Account", Icon: User },
] as const;

export default function BottomNav({ active, onChange }: Props) {
  return (
    <nav className="bottom-nav fixed bottom-0 left-0 right-0 z-50 flex justify-around items-center h-16 px-2">
      {tabs.map(({ id, label, Icon }) => (
        <button
          key={id}
          onClick={() => { haptic("light"); onChange(id); }}
          className={`nav-item flex-1 py-2 ${active === id ? "active" : ""}`}
        >
          <Icon
            size={22}
            strokeWidth={active === id ? 2.2 : 1.8}
            className={active === id ? "text-[#6c63ff]" : "text-[#555566]"}
          />
          <span className={active === id ? "text-[#6c63ff]" : "text-[#555566]"}>
            {label}
          </span>
        </button>
      ))}
    </nav>
  );
}
