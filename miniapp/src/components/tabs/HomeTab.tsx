"use client";
import { Search, Zap, ArrowRight, RefreshCw } from "lucide-react";
import ProductCard from "../ProductCard";
import { useState, useCallback } from "react";
import BuyModal from "../BuyModal";
import { haptic } from "@/lib/twa";
import { Product, getProduct } from "@/lib/api";

interface Props {
  userId: number | null;
  product: Product | null;
  referralReward?: number;
  onBuySuccess: () => void;
  onRefresh?: (p: Product) => void;
}

export default function HomeTab({ userId, product, referralReward = 0.50, onBuySuccess, onRefresh }: Props) {
  const [showBuy, setShowBuy]     = useState(false);
  const [filter, setFilter]       = useState("All");
  const [refreshing, setRefreshing] = useState(false);

  const sold  = product?.sold  ?? 0;
  const stock = product?.stock ?? 0;
  const price = product?.price ?? 0;
  const name  = product?.name  ?? "";
  const imageUrl = product?.image_url ?? "";

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    haptic("light");
    try {
      const fresh = await getProduct();
      if (fresh && onRefresh) onRefresh(fresh);
    } finally {
      setRefreshing(false);
    }
  }, [onRefresh]);

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-3 border-b border-[#2a2a3a]">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-[#8888aa] text-xs">Welcome to</p>
            <h1 className="text-white font-bold text-lg leading-tight">
              Alpha Shop&nbsp;🔥
            </h1>
          </div>
          <button
            onClick={handleRefresh}
            className="w-8 h-8 rounded-xl bg-[#1a1a24] border border-[#2a2a3a] flex items-center justify-center"
          >
            <RefreshCw
              size={14}
              className={`text-[#6c63ff] ${refreshing ? "animate-spin" : ""}`}
            />
          </button>
        </div>

        {/* Search bar */}
        <div className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-3 py-2.5">
          <Search size={15} className="text-[#555566]" />
          <span className="text-[#555566] text-sm">Search products...</span>
        </div>
      </div>

      <div className="px-4 flex flex-col gap-4">

        {/* Referral Banner */}
        <div
          className="rounded-2xl p-4 flex items-center justify-between cursor-pointer active:scale-[0.98] transition-transform"
          style={{ background: "linear-gradient(135deg,#1a1a2e 0%,#16213e 100%)", border: "1px solid #6c63ff44" }}
          onClick={() => haptic("light")}
        >
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ background: "linear-gradient(135deg,#6c63ff 0%,#4f8eff 100%)" }}>
              <Zap size={16} className="text-white" />
            </div>
            <div>
              <p className="text-[11px] text-[#6c63ff] font-semibold uppercase tracking-wide mb-0.5">
                🎁 REFERRAL PROGRAM
              </p>
              <p className="text-white font-semibold text-sm">
                Invite friends & earn{" "}
                <span className="text-[#6c63ff]">${referralReward.toFixed(2)} each</span>
              </p>
              <p className="text-[#555566] text-xs mt-0.5">Withdraw from $3.00</p>
            </div>
          </div>
          <ArrowRight size={16} className="text-[#6c63ff] flex-shrink-0" />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { label: "Links Sold",  value: sold > 0  ? `${sold.toLocaleString()}+` : "—" },
            { label: "In Stock",    value: stock > 0 ? stock.toLocaleString()       : "—" },
            { label: "Rating",      value: product?.rating ? `${product.rating}★`   : "—" },
          ].map(({ label, value }) => (
            <div key={label} className="card p-3 flex flex-col items-center gap-1">
              <span className="text-[#6c63ff] font-bold text-sm">{value}</span>
              <span className="text-[#555566] text-[10px]">{label}</span>
            </div>
          ))}
        </div>

        {/* Products */}
        {product ? (
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-white font-bold text-base">All Products</h2>
            </div>

            {/* Filter chips */}
            <div className="flex gap-2 mb-3 overflow-x-auto pb-1 no-scrollbar">
              {["All", "In stock", "Featured"].map((f) => (
                <button
                  key={f}
                  onClick={() => { haptic("light"); setFilter(f); }}
                  className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium border transition-all
                    ${filter === f
                      ? "text-white border-transparent"
                      : "text-[#555566] border-[#2a2a3a] bg-[#1a1a24]"
                    }`}
                  style={filter === f
                    ? { background: "linear-gradient(135deg,#6c63ff 0%,#4f8eff 100%)" }
                    : {}}
                >
                  {f}
                </button>
              ))}
            </div>

            {/* Product grid */}
            {(filter === "In stock" && stock <= 0) ? (
              <div className="card p-8 flex flex-col items-center gap-2 text-center">
                <span className="text-3xl">📭</span>
                <p className="text-white font-semibold">Out of Stock</p>
                <p className="text-[#555566] text-sm">Check back soon!</p>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <ProductCard
                  name={name}
                  price={price}
                  sold={sold}
                  imageUrl={imageUrl}
                  isNew
                  outOfStock={stock <= 0}
                  onBuy={() => setShowBuy(true)}
                />
                <div className="card p-4 flex flex-col items-center justify-center gap-2 opacity-40">
                  <span className="text-3xl">🔒</span>
                  <p className="text-[#555566] text-xs text-center">More coming soon</p>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Loading skeleton */
          <div className="grid grid-cols-2 gap-3">
            {[0, 1].map(i => (
              <div key={i} className="card p-3 h-48 shimmer rounded-2xl" />
            ))}
          </div>
        )}
      </div>

      {showBuy && product && (
        <BuyModal
          product={{ name, price, stock }}
          userId={userId}
          onClose={() => setShowBuy(false)}
          onSuccess={() => { setShowBuy(false); onBuySuccess(); }}
        />
      )}
    </div>
  );
}
