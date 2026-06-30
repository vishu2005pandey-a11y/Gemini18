"use client";
import { useEffect, useState } from "react";
import BottomNav from "@/components/BottomNav";
import HomeTab from "@/components/tabs/HomeTab";
import BrowseTab from "@/components/tabs/BrowseTab";
import OrdersTab from "@/components/tabs/OrdersTab";
import WalletTab from "@/components/tabs/WalletTab";
import AccountTab from "@/components/tabs/AccountTab";
import { getTWAUser } from "@/lib/twa";
import { getProduct, getOrders, getWallet } from "@/lib/api";

type Tab = "home" | "browse" | "orders" | "wallet" | "account";

export default function App() {
  const [tab, setTab] = useState<Tab>("home");
  const [user, setUser]       = useState<any>(null);
  const [product, setProduct] = useState<any>(null);
  const [orders, setOrders]   = useState<any[]>([]);
  const [wallet, setWallet]   = useState({ balance: 0, deposits: [] });
  const [ready, setReady]     = useState(false);

  useEffect(() => {
    // Init Telegram WebApp
    if (typeof window !== "undefined") {
      const twa = (window as any).Telegram?.WebApp;
      if (twa) {
        twa.ready();
        twa.expand();
        twa.setHeaderColor("#0a0a0f");
        twa.setBackgroundColor("#0a0a0f");
      }
    }

    const tgUser = getTWAUser();
    setUser(tgUser);

    // Load data
    (async () => {
      const [prod, ords, wal] = await Promise.all([
        getProduct(),
        tgUser ? getOrders(tgUser.id) : Promise.resolve([]),
        tgUser ? getWallet(tgUser.id) : Promise.resolve({ balance: 0, deposits: [] }),
      ]);
      setProduct(prod);
      setOrders(ords);
      setWallet(wal);
      setReady(true);
    })();
  }, []);

  if (!ready) {
    return (
      <div className="fixed inset-0 bg-[#0a0a0f] flex flex-col items-center justify-center gap-4">
        {/* Logo */}
        <div
          className="w-20 h-20 rounded-3xl flex items-center justify-center text-4xl shadow-accent"
          style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}
        >
          ⚡
        </div>
        <div className="text-center">
          <h1 className="text-white font-bold text-2xl gradient-text">Alpha Shop</h1>
          <p className="text-[#555566] text-sm mt-1">Premium Digital Store</p>
        </div>
        {/* Loader */}
        <div className="flex gap-1.5 mt-4">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 rounded-full"
              style={{
                background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)",
                animation: `pulse-dot 1.2s ease-in-out ${i * 0.2}s infinite`,
              }}
            />
          ))}
        </div>
      </div>
    );
  }

  const renderTab = () => {
    switch (tab) {
      case "home":
        return (
          <HomeTab
            user={user}
            product={product}
            onBuySuccess={() => setTab("orders")}
          />
        );
      case "browse":
        return <BrowseTab product={product} />;
      case "orders":
        return <OrdersTab orders={orders} onShop={() => setTab("home")} />;
      case "wallet":
        return <WalletTab wallet={wallet} />;
      case "account":
        return <AccountTab user={user} onReferral={() => setTab("home")} />;
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] pb-16 overflow-y-auto">
      {/* Telegram WebApp script */}
      <script src="https://telegram.org/js/telegram-web-app.js" async />
      {renderTab()}
      <BottomNav active={tab} onChange={setTab} />
    </main>
  );
}
