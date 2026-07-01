"use client";
import { ShoppingBag, Star } from "lucide-react";
import ProductCard from "../ProductCard";
import { useState } from "react";
import BuyModal from "../BuyModal";
import { haptic } from "@/lib/twa";
import { Product } from "@/lib/api";

interface Props {
  product: Product | null;
  userId: number | null;
  onBuySuccess: () => void;
}

export default function BrowseTab({ product, userId, onBuySuccess }: Props) {
  const [showBuy, setShowBuy] = useState(false);

  const name = product?.name || "Gemini Pro 18m";
  const price = product?.price ?? 4.99;
  const stock = product?.stock ?? 0;
  const sold = product?.sold ?? 0;
  const imageUrl = product?.image_url || "";
  const description = product?.description || "Premium Gemini AI Pro access for 18 months.";

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Browse</h1>
        <p className="text-[#555566] text-sm mt-0.5">All available products</p>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Categories */}
        <div className="grid grid-cols-2 gap-3">
          <div
            className="card p-5 flex flex-col items-start gap-3 cursor-pointer active:scale-95 transition-transform"
            onClick={() => haptic("light")}
          >
            <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl"
              style={{ background: "linear-gradient(135deg, #6c63ff22 0%, #4f8eff22 100%)", border: "1px solid #6c63ff44" }}>
              🤖
            </div>
            <div>
              <p className="text-white font-semibold text-sm leading-tight">Gemini Pro</p>
              <p className="text-[#555566] text-xs">18-month subscriptions</p>
            </div>
          </div>

          <div
            className="card p-5 flex flex-col items-start gap-3 cursor-pointer active:scale-95 transition-transform opacity-40"
            onClick={() => haptic("light")}
          >
            <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl"
              style={{ background: "linear-gradient(135deg, #22d3a522 0%, #4f8eff22 100%)", border: "1px solid #22d3a544" }}>
              🔒
            </div>
            <div>
              <p className="text-white font-semibold text-sm leading-tight">More Soon</p>
              <p className="text-[#555566] text-xs">Coming soon</p>
            </div>
          </div>
        </div>

        {/* Product detail card */}
        <div className="card p-5 flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h2 className="text-white font-bold text-base">{name}</h2>
            {product?.stock && product.stock > 0 ? (
              <span className="text-xs px-2.5 py-1 rounded-full bg-[#22d3a522] text-[#22d3a5] font-medium">
                In Stock
              </span>
            ) : (
              <span className="text-xs px-2.5 py-1 rounded-full bg-[#ff4f6e22] text-[#ff4f6e] font-medium">
                Out of Stock
              </span>
            )}
          </div>

          <p className="text-[#8888aa] text-sm leading-relaxed">{description}</p>

          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-1">
              <Star size={14} className="text-[#fbbf24]" fill="#fbbf24" />
              <span className="text-white font-semibold">{product?.rating ?? 4.8}</span>
              <span className="text-[#555566]">({product?.reviews ?? 0} reviews)</span>
            </div>
            <span className="text-[#555566]">·</span>
            <span className="text-[#555566]">{sold.toLocaleString()} sold</span>
          </div>

          <div className="flex items-center justify-between pt-1">
            <p className="text-white font-bold text-2xl">${price.toFixed(2)}</p>
            <button
              disabled={stock <= 0}
              onClick={() => { haptic("medium"); setShowBuy(true); }}
              className="btn-primary px-6 py-2.5 flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ShoppingBag size={16} />
              Buy Now
            </button>
          </div>
        </div>

        {/* Featured grid */}
        <div>
          <h2 className="text-white font-bold text-base mb-3">Featured</h2>
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
          </div>
        </div>
      </div>

      {showBuy && (
        <BuyModal
          product={{ name, price, stock }}
          userId={userId}
          onClose={() => setShowBuy(false)}
          onSuccess={() => {
            setShowBuy(false);
            onBuySuccess();
          }}
        />
      )}
    </div>
  );
}
