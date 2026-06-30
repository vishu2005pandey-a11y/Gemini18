"use client";
import { Package, ShoppingBag, ExternalLink } from "lucide-react";
import { haptic } from "@/lib/twa";

interface Props {
  orders: any[];
  onShop: () => void;
}

export default function OrdersTab({ orders, onShop }: Props) {
  if (!orders || orders.length === 0) {
    return (
      <div className="flex flex-col gap-4 pb-4">
        <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
          <h1 className="text-white font-bold text-xl">My Orders</h1>
        </div>

        <div className="flex-1 flex items-center justify-center px-6 mt-16">
          <div className="card p-10 flex flex-col items-center gap-4 w-full text-center">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center"
              style={{ background: "linear-gradient(135deg, #6c63ff22 0%, #4f8eff22 100%)", border: "1px solid #6c63ff33" }}>
              <ShoppingBag size={28} className="text-[#6c63ff]" />
            </div>
            <div>
              <p className="text-white font-semibold text-base">No orders yet</p>
              <p className="text-[#555566] text-sm mt-1">
                When you buy a product, your orders and delivery keys will show up here.
              </p>
            </div>
            <button
              onClick={() => { haptic("medium"); onShop(); }}
              className="btn-primary mt-2 px-8 py-3"
            >
              Start shopping
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 pb-4">
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">My Orders</h1>
        <p className="text-[#555566] text-sm mt-0.5">{orders.length} order(s)</p>
      </div>

      <div className="px-4 flex flex-col gap-3">
        {orders.map((order: any) => (
          <div key={order.order_id} className="card p-4 flex flex-col gap-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#1a1a24] flex items-center justify-center text-xl">
                  🤖
                </div>
                <div>
                  <p className="text-white font-semibold text-sm">Gemini Pro 18m</p>
                  <p className="text-[#555566] text-xs">{order.quantity}× links</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-white font-bold">${order.amount_usd?.toFixed(2)}</p>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#22d3a522] text-[#22d3a5] font-medium">
                  ✓ Delivered
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between border-t border-[#2a2a3a] pt-3">
              <div>
                <p className="text-[#555566] text-xs">Order ID</p>
                <p className="text-white font-mono text-sm">{order.order_id}</p>
              </div>
              <p className="text-[#555566] text-xs">{order.paid_at?.slice(0, 10)}</p>
            </div>

            <button
              onClick={() => haptic("light")}
              className="flex items-center justify-center gap-2 w-full btn-secondary py-2.5 text-sm"
            >
              <ExternalLink size={14} />
              View Links
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
