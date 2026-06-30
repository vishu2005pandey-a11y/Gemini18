"use client";
import { X, Minus, Plus, ShoppingCart, Shield } from "lucide-react";
import { useState } from "react";
import { haptic } from "@/lib/twa";

interface Props {
  product: { name: string; price: number; stock: number };
  onClose: () => void;
  onConfirm: (qty: number) => void;
}

export default function BuyModal({ product, onClose, onConfirm }: Props) {
  const [qty, setQty] = useState(1);

  const total = (product.price * qty).toFixed(2);

  const adjust = (delta: number) => {
    haptic("light");
    setQty((q) => Math.max(1, Math.min(100, q + delta)));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end" onClick={onClose}>
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

      {/* Sheet */}
      <div
        className="relative w-full bg-[#111118] rounded-t-3xl p-6 pb-10 slide-up"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Handle */}
        <div className="w-10 h-1 bg-[#2a2a3a] rounded-full mx-auto mb-5" />

        {/* Close */}
        <button onClick={onClose} className="absolute top-5 right-5 text-[#555566]">
          <X size={20} />
        </button>

        {/* Product */}
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-[#1a1a24] rounded-2xl flex items-center justify-center text-3xl flex-shrink-0">
            🤖
          </div>
          <div>
            <p className="font-semibold text-white">{product.name}</p>
            <p className="text-[#6c63ff] font-bold text-lg">${product.price.toFixed(2)}</p>
            <p className="text-[#555566] text-xs">{product.stock} in stock</p>
          </div>
        </div>

        {/* Quantity */}
        <div className="card-elevated p-4 rounded-2xl mb-4">
          <p className="text-[#8888aa] text-sm mb-3">Quantity</p>
          <div className="flex items-center justify-between">
            <button
              onClick={() => adjust(-1)}
              className="w-10 h-10 bg-[#0a0a0f] rounded-xl flex items-center justify-center text-white border border-[#2a2a3a]"
            >
              <Minus size={16} />
            </button>
            <span className="text-2xl font-bold text-white w-16 text-center">{qty}</span>
            <button
              onClick={() => adjust(1)}
              className="w-10 h-10 rounded-xl flex items-center justify-center text-white"
              style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}
            >
              <Plus size={16} />
            </button>
          </div>
        </div>

        {/* Quick qty presets */}
        <div className="flex gap-2 mb-5">
          {[1, 3, 5, 10].map((n) => (
            <button
              key={n}
              onClick={() => { haptic("light"); setQty(n); }}
              className={`flex-1 py-2 rounded-xl text-sm font-semibold border transition-all
                ${qty === n
                  ? "border-[#6c63ff] text-[#6c63ff] bg-[#6c63ff11]"
                  : "border-[#2a2a3a] text-[#555566] bg-[#1a1a24]"
                }`}
            >
              {n}×
            </button>
          ))}
        </div>

        {/* Total */}
        <div className="flex items-center justify-between mb-5 p-4 bg-[#1a1a24] rounded-2xl">
          <span className="text-[#8888aa]">Total</span>
          <span className="text-white font-bold text-xl">${total}</span>
        </div>

        {/* Terms note */}
        <div className="flex items-start gap-2 mb-5 text-[#555566] text-xs">
          <Shield size={14} className="mt-0.5 flex-shrink-0 text-[#6c63ff]" />
          <p>24-hour warranty on link activation. Activate within the time frame.</p>
        </div>

        {/* Confirm */}
        <button
          onClick={() => { haptic("success"); onConfirm(qty); }}
          className="w-full btn-primary py-4 text-base flex items-center justify-center gap-2"
        >
          <ShoppingCart size={18} />
          Pay ${total} with USDT
        </button>
      </div>
    </div>
  );
}
