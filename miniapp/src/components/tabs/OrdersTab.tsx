"use client";
import { useState } from "react";
import { ShoppingBag, ExternalLink, ChevronDown, ChevronUp } from "lucide-react";
import { haptic } from "@/lib/twa";
import { Order } from "@/lib/api";

interface Props {
  orders: Order[];
  onShop: () => void;
}

function OrderCard({ order }: { order: Order }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="card p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#1a1a24] flex items-center justify-center text-xl">
            🤖
          </div>
          <div>
            <p className="text-white font-semibold text-sm">Order #{order.order_id.slice(-6)}</p>
            <p className="text-[#555566] text-xs">{order.quantity}× link{order.quantity !== 1 ? "s" : ""}</p>
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

      {order.links && order.links.length > 0 ? (
        <>
          <button
            onClick={() => { haptic("light"); setExpanded((e) => !e); }}
            className="flex items-center justify-center gap-2 w-full btn-secondary py-2.5 text-sm"
          >
            {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            {expanded ? "Hide Links" : `View ${order.links.length} Link${order.links.length !== 1 ? "s" : ""}`}
          </button>

          {expanded && (
            <div className="flex flex-col gap-2 pt-1">
              {order.links.map((link, i) => (
                <div key={i} className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-3 py-2.5">
                  <p className="flex-1 text-[#8888aa] text-xs font-mono truncate">{link}</p>
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => haptic("light")}
                    className="flex-shrink-0 flex items-center gap-1 text-[#6c63ff] text-xs font-medium"
                  >
                    <ExternalLink size={12} />
                    Open
                  </a>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <p className="text-[#555566] text-xs text-center py-1">Links not available</p>
      )}
    </div>
  );
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
        <p className="text-[#555566] text-sm mt-0.5">{orders.length} order{orders.length !== 1 ? "s" : ""}</p>
      </div>

      <div className="px-4 flex flex-col gap-3">
        {orders.map((order) => (
          <OrderCard key={order.order_id} order={order} />
        ))}
      </div>
    </div>
  );
}
