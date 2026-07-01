"use client";
import { useEffect, useState, useCallback } from "react";
import BottomNav, { Tab } from "@/components/BottomNav";
import HomeTab from "@/components/tabs/HomeTab";
import BrowseTab from "@/components/tabs/BrowseTab";
import OrdersTab from "@/components/tabs/OrdersTab";
import WalletTab from "@/components/tabs/WalletTab";
import AccountTab from "@/components/tabs/AccountTab";
import LeaderboardTab from "@/components/tabs/LeaderboardTab";
import ReferralTab from "@/components/tabs/ReferralTab";
import { getTWAUser } from "@/lib/twa";
import {
  getProduct, getOrders, getWallet, getUser,
  Product, Order, Wallet, UserInfo,
} from "@/lib/api";

type TGUser = { id: number; first_name: string; last_name?: string; username?: string } | null;

export default function App() {
  const [tab, setTab]         = useState<Tab>("home");
  const [tgUser, setTgUser]   = useState<TGUser>(null);
  const [product, setProduct] = useState<Product | null>(null);
  const [orders, setOrders]   = useState<Order[]>([]);
  const [wallet, setWallet]   = useState<Wallet>({ balance: 0, deposits: [] });
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [ready, setReady]     = useState(false);
  const [referralReward]      = useState(0.5);

  // ── Load all data ──────────────────────────────────────────────────────────
  const loadData = useCallback(async (uid: number | null) => {
    const [prod, ords, wal] = await Promise.all([
      getProduct(),
      uid ? getOrders(uid) : Promise.resolve([]),
      uid ? getWallet(uid) : Promise.resolve({ balance: 0, deposits: [] }),
    ]);
    setProduct(prod);
    setOrders(ords);
    setWallet(wal);
    if (uid) {
      const info = await getUser(uid);
      if (info) setUserInfo(info);
    }
  }, []);

  // ── Init ───────────────────────────────────────────────────────────────────
  useEffect(() => {
    if (typeof window !== "undefined") {
      const twa = (window as any).Telegram?.WebApp;
      if (twa) { twa.ready(); twa.expand(); twa.setHeaderColor?.("#0a0a0f"); twa.setBackgroundColor?.("#0a0a0f"); }
    }
    const user = getTWAUser() as TGUser;
    setTgUser(user);
    loadData(user?.id ?? null).finally(() => setReady(true));
  }, [loadData]);

  // ── Auto-refresh product every 30s ────────────────────────────────────────
  useEffect(() => {
    const timer = setInterval(async () => {
      const fresh = await getProduct();
      if (fresh) setProduct(fresh);
    }, 30000);
    return () => clearInterval(timer);
  }, []);

  const reloadOrders = useCallback(async () => {
    if (!tgUser?.id) return;
    const ords = await getOrders(tgUser.id);
    setOrders(ords);
  }, [tgUser]);

  const handleProductRefresh = useCallback((p: Product) => setProduct(p), []);

  // ── Splash screen ──────────────────────────────────────────────────────────
  if (!ready) {
    return (
      <div className="fixed inset-0 bg-[#0a0a0f] flex flex-col items-center justify-center gap-4">
        <div className="w-20 h-20 rounded-3xl flex items-center justify-center text-4xl shadow-accent"
          style={{ background: "linear-gradient(135deg,#6c63ff 0%,#4f8eff 100%)" }}>
          ⚡
        </div>
        <div className="text-center">
          <h1 className="text-white font-bold text-2xl gradient-text">Alpha Shop</h1>
          <p className="text-[#555566] text-sm mt-1">Premium Digital Store</p>
        </div>
        <div className="flex gap-1.5 mt-4">
          {[0,1,2].map(i => (
            <div key={i} className="w-2 h-2 rounded-full"
              style={{ background:"linear-gradient(135deg,#6c63ff 0%,#4f8eff 100%)",
                animation:`pulse-dot 1.2s ease-in-out ${i*0.2}s infinite` }} />
          ))}
        </div>
      </div>
    );
  }

  // ── Render ─────────────────────────────────────────────────────────────────
  const renderTab = () => {
    switch (tab) {
      case "home":
        return <HomeTab userId={tgUser?.id ?? null} product={product}
          referralReward={referralReward}
          onBuySuccess={() => { reloadOrders(); setTab("orders"); }}
          onRefresh={handleProductRefresh} />;
      case "browse":
        return <BrowseTab product={product} userId={tgUser?.id ?? null}
          onBuySuccess={() => { reloadOrders(); setTab("orders"); }} />;
      case "orders":
        return <OrdersTab orders={orders} onShop={() => setTab("home")} />;
      case "wallet":
        return <WalletTab wallet={wallet} userId={tgUser?.id ?? null} />;
      case "account":
        return <AccountTab user={tgUser} userInfo={userInfo}
          onReferral={() => setTab("referral")}
          onLeaderboard={() => setTab("leaderboard")} />;
      case "leaderboard":
        return <LeaderboardTab />;
      case "referral":
        return <ReferralTab userId={tgUser?.id ?? null} />;
      default:
        return null;
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] pb-16 overflow-y-auto">
      <script src="https://telegram.org/js/telegram-web-app.js" async />
      {renderTab()}
      <BottomNav active={tab} onChange={setTab} />
    </main>
  );
}
