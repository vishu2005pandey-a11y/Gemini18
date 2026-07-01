"use client";
import { X, Minus, Plus, ShoppingCart, Shield, AlertCircle } from "lucide-react";
import { useState } from "react";
import { haptic, getTWA } from "@/lib/twa";
import { createOrder, CreateOrderResult, Product } from "@/lib/api";
import PaymentScreen from "./PaymentScreen";

interface Props {
  product: Pick<Product, "name" | "price" | "stock">;
  userId: number | null;
  onClose: () => void;
  onSuccess: () => void;
}

type ModalState = "select" | "creating" | "payment" | "done";

export default function BuyModal({ product, userId, onClose, onSuccess }: Props) {
  const [qty, setQty] = useState(1);
  const [state, setState] = useState<ModalState>("select");
  const [error, setError] = useState("");
  const [order, setOrder] = useState<CreateOrderResult | null>(null);
  const [deliveredLinks, setDeliveredLinks] = useState<string[]>([]);

  const total = (product.price * qty).toFixed(2);

  const adjust = (delta: number) => {
    haptic("light");
    setQty((q) => Math.max(1, Math.min(product.stock || 100, q + delta)));
  };

  const handleConfirm = async () => {
    if (!userId) {
      setError("User not identified. Please restart the Mini App.");
      return;
    }
    haptic("medium");
    setState("creating");
    setError("");
    try {
      const twa = getTWA();
      const initData = twa?.initData || "";
      const result = await createOrder(userId, qty, initData);
      setOrder(result);
      setState("payment");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to create order";
      if (msg.includes("insufficient_stock")) {
        setError("Not enough stock available. Please reduce quantity.");
      } else if (msg.includes("payment_provider")) {
        setError("Payment provider unavailable. Please try again later.");
      } else {
        setError(msg || "Something went wrong. Please try again.");
      }
      setState("select");
    }
  };

  const handlePaymentSuccess = (links: string[]) => {
    setDeliveredLinks(links);
    setState("done");
    onSuccess();
  };

  // Payment screen overlays everything
  if (state === "payment" && order) {
    return (
      <PaymentScreen
        order={order}
        onSuccess={handlePaymentSuccess}
        onCancel={() => { setState("select"); setOrder(null); }}
      />
    );
  }

  // Delivered links screen
  if (state === "done") {
    return (
      <div className="fixed inset-0 z-50 flex items-end" onClick={onClose}>
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
        <div
          className="relative w-full bg-[#111118] rounded-t-3xl p-6 pb-10 slide-up max-h-[80vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="w-10 h-1 bg-[#2a2a3a] rounded-full mx-auto mb-5" />
          <div className="flex flex-col items-center gap-3 mb-6">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
              style={{ background: "linear-gradient(135deg, #22d3a522 0%, #4f8eff22 100%)", border: "1px solid #22d3a544" }}>
              ✅
            </div>
            <p className="text-white font-bold text-xl">Payment Confirmed!</p>
            <p className="text-[#555566] text-sm text-center">Your redemption links are ready</p>
          </div>
          <div className="flex flex-col gap-3">
            {deliveredLinks.map((link, i) => (
              <div key={i} className="card p-4 flex items-center justify-between gap-3">
                <p className="text-[#8888aa] text-xs font-mono flex-1 truncate">{link}</p>
                <a
                  href={link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium"
                  style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)", color: "white" }}
                >
                  Redeem
                </a>
              </div>
            ))}
          </div>
          <button onClick={onClose} className="w-full btn-primary py-3 mt-6">
            Done
          </button>
        </div>
      </div>
    );
  }

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

        {/* Error */}
        {error && (
          <div className="flex items-start gap-2 p-3 rounded-xl bg-[#ff4f6e11] border border-[#ff4f6e33] mb-4">
            <AlertCircle size={16} className="text-[#ff4f6e] mt-0.5 flex-shrink-0" />
            <p className="text-[#ff4f6e] text-xs">{error}</p>
          </div>
        )}

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
              onClick={() => { haptic("light"); setQty(Math.min(n, product.stock || n)); }}
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
          onClick={handleConfirm}
          disabled={state === "creating" || !product.stock}
          className="w-full btn-primary py-4 text-base flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {state === "creating" ? (
            <>
              <div className="w-5 h-5 rounded-full border-2 border-white border-t-transparent animate-spin" />
              Creating order...
            </>
          ) : (
            <>
              <ShoppingCart size={18} />
              Pay ${total} with USDT
            </>
          )}
        </button>
      </div>
    </div>
  );
}
