"use client";
import { Search, Zap, TrendingUp, Star, ArrowRight } from "lucide-react";
import ProductCard from "../ProductCard";
import { useState } from "react";
import BuyModal from "../BuyModal";
import { haptic } from "@/lib/twa";

interface Props {
  user: any;
  product: any;
  onBuySuccess: () => void;
}

export default function HomeTab({ user, product, onBuySuccess }: Props) {
  const [showBuy, setShowBuy] = useState(false);

  const name = user?.first_name || "there";

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-3 border-b border-[#2a2a3a]">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-[#8888aa] text-xs">Welcome back</p>
            <h1 className="text-white font-bold text-lg leading-tight">
              — Alpha α&nbsp;
              <span className="text-lg">🔥</span>
            </h1>
          </div>
          <div className="flex items-center gap-1 bg-[#1a1a24] border border-[#2a2a3a] rounded-full px-3 py-1.5">
            <span className="text-[#8888aa] text-xs">Balance:</span>
            <span className="text-white text-xs font-semibold">$0.00</span>
          </div>
        </div>

        {/* Search */}
        <div className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-3 py-2.5">
          <Search size={15} className="text-[#555566]" />
          <span className="text-[#555566] text-sm">Search products, categories...</span>
        </div>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Referral Banner */}
        <div
          className="rounded-2xl p-4 flex items-center justify-between cursor-pointer"
          style={{ background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)", border: "1px solid #6c63ff44" }}
          onClick={() => haptic("light")}
        >
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}>
              <Zap size={16} className="text-white" />
            </div>
            <div>
              <p className="text-[11px] text-[#6c63ff] font-semibold uppercase tracking-wide mb-0.5">
                🎁 LIMITED-TIME CAMPAIGN
              </p>
              <p className="text-white font-semibold text-sm">
                Invite friends & earn <span className="text-[#6c63ff]">$0.50 each</span>
              </p>
              <p className="text-[#555566] text-xs mt-0.5">No purchases needed. Withdraw from $3.00</p>
            </div>
          </div>
          <ArrowRight size={16} className="text-[#6c63ff] flex-shrink-0" />
        </div>

        {/* Stats bar */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { label: "Links Sold", value: `${(product?.sold || 70000).toLocaleString()}+`, icon: TrendingUp },
            { label: "In Stock", value: product?.stock || 247, icon: Star },
            { label: "Rating", value: `${product?.rating || 4.8}★`, icon: Star },
          ].map(({ label, value, icon: Icon }) => (
            <div key={label} className="card p-3 flex flex-col items-center gap-1">
              <span className="text-[#6c63ff] font-bold text-sm">{value}</span>
              <span className="text-[#555566] text-[10px]">{label}</span>
            </div>
          ))}
        </div>

        {/* Hot Offers */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-base">🔥</span>
              <h2 className="text-white font-bold text-base">Hot Offers</h2>
            </div>
            <span className="text-[#6c63ff] text-xs font-medium">See all →</span>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <ProductCard
              name={product?.name || "Gemini Pro 18m"}
              price={product?.price || 4.99}
              sold={product?.sold}
              isNew
              outOfStock={!product?.stock}
              onBuy={() => setShowBuy(true)}
            />
            <div className="card p-3 flex flex-col items-center justify-center gap-2 opacity-40">
              <span className="text-3xl">🔒</span>
              <p className="text-[#555566] text-xs text-center">More products coming soon</p>
            </div>
          </div>
        </div>

        {/* All Products */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-white font-bold text-base">All Products</h2>
          </div>

          {/* Filter chips */}
          <div className="flex gap-2 mb-3 overflow-x-auto pb-1">
            {["All", "In stock", "On sale", "Featured"].map((f, i) => (
              <button
                key={f}
                className={`flex-shrink-0 px-3 py-1.5 rounded-full text-xs font-medium border transition-all
                  ${i === 0
                    ? "text-white border-transparent"
                    : "text-[#555566] border-[#2a2a3a] bg-[#1a1a24]"
                  }`}
                style={i === 0 ? { background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" } : {}}
                onClick={() => haptic("light")}
              >
                {f}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <ProductCard
              name={product?.name || "Gemini Pro 18m"}
              price={product?.price || 4.99}
              sold={product?.sold}
              isNew
              outOfStock={!product?.stock}
              onBuy={() => setShowBuy(true)}
            />
          </div>
        </div>
      </div>

      {/* Buy Modal */}
      {showBuy && (
        <BuyModal
          product={{ name: product?.name || "Gemini Pro 18m", price: product?.price || 4.99, stock: product?.stock || 0 }}
          onClose={() => setShowBuy(false)}
          onConfirm={(qty) => {
            setShowBuy(false);
            onBuySuccess();
          }}
        />
      )}
    </div>
  );
}
