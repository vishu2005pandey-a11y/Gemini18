"use client";
import { ShoppingBag } from "lucide-react";
import ProductCard from "../ProductCard";
import { useState } from "react";
import BuyModal from "../BuyModal";
import { haptic } from "@/lib/twa";

interface Props {
  product: any;
}

export default function BrowseTab({ product }: Props) {
  const [showBuy, setShowBuy] = useState(false);

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Browse Categories</h1>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Categories */}
        <div className="grid grid-cols-2 gap-3">
          {/* Gemini category */}
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

          {/* All Products */}
          <div
            className="card p-5 flex flex-col items-start gap-3 cursor-pointer active:scale-95 transition-transform"
            onClick={() => haptic("light")}
          >
            <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl"
              style={{ background: "linear-gradient(135deg, #22d3a522 0%, #4f8eff22 100%)", border: "1px solid #22d3a544" }}>
              🛍️
            </div>
            <div>
              <p className="text-white font-semibold text-sm leading-tight">All Products</p>
              <p className="text-[#555566] text-xs">Browse everything</p>
            </div>
          </div>
        </div>

        {/* Featured */}
        <div>
          <h2 className="text-white font-bold text-base mb-3">Featured</h2>
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

      {showBuy && (
        <BuyModal
          product={{ name: product?.name || "Gemini Pro 18m", price: product?.price || 4.99, stock: product?.stock || 0 }}
          onClose={() => setShowBuy(false)}
          onConfirm={() => setShowBuy(false)}
        />
      )}
    </div>
  );
}
