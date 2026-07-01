"use client";
import { useEffect, useState, useCallback } from "react";
import { Copy, ExternalLink, CheckCircle, XCircle, Clock, RefreshCw } from "lucide-react";
import { checkPayment, cancelOrder, CreateOrderResult } from "@/lib/api";
import { haptic } from "@/lib/twa";

interface Props {
  order: CreateOrderResult;
  onSuccess: (links: string[]) => void;
  onCancel: () => void;
}

type CheckStatus = "idle" | "checking" | "paid" | "pending" | "expired" | "cancelled";

export default function PaymentScreen({ order, onSuccess, onCancel }: Props) {
  const [timeLeft, setTimeLeft] = useState(order.timeout);
  const [copied, setCopied] = useState<"address" | "amount" | null>(null);
  const [status, setStatus] = useState<CheckStatus>("idle");
  const [links, setLinks] = useState<string[]>([]);
  const [checkError, setCheckError] = useState("");

  // Countdown timer
  useEffect(() => {
    if (timeLeft <= 0) return;
    const id = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(id);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [timeLeft]);

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, "0");
    const s = (secs % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  const copyToClipboard = async (text: string, type: "address" | "amount") => {
    try {
      await navigator.clipboard.writeText(text);
      haptic("light");
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    } catch {
      // fallback
    }
  };

  const handleCheckPayment = useCallback(async () => {
    if (status === "checking" || status === "paid") return;
    setStatus("checking");
    setCheckError("");
    try {
      const result = await checkPayment(order.order_id);
      if (result.status === "paid") {
        setLinks(result.links);
        setStatus("paid");
        haptic("success");
        onSuccess(result.links);
      } else if (result.status === "expired" || result.status === "cancelled") {
        setStatus(result.status);
        haptic("error");
      } else {
        setStatus("pending");
        setTimeout(() => setStatus("idle"), 2000);
      }
    } catch (err) {
      setCheckError("Connection error. Try again.");
      setStatus("idle");
    }
  }, [order.order_id, status, onSuccess]);

  const handleCancel = async () => {
    haptic("medium");
    await cancelOrder(order.order_id);
    onCancel();
  };

  const isExpired = timeLeft <= 0;

  return (
    <div className="fixed inset-0 z-50 bg-[#0a0a0f] overflow-y-auto">
      <div className="flex flex-col min-h-screen px-4 pb-8 pt-6 gap-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h2 className="text-white font-bold text-xl">Complete Payment</h2>
          <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium
            ${isExpired
              ? "bg-[#ff4f6e22] text-[#ff4f6e]"
              : "bg-[#22d3a522] text-[#22d3a5]"
            }`}>
            <Clock size={14} />
            <span>{isExpired ? "Expired" : formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* Order summary */}
        <div className="card p-4 flex items-center justify-between">
          <div>
            <p className="text-[#8888aa] text-xs">Order ID</p>
            <p className="text-white font-mono text-sm">{order.order_id}</p>
          </div>
          <div className="text-right">
            <p className="text-[#8888aa] text-xs">Total</p>
            <p className="text-white font-bold">${order.amount_usd.toFixed(2)}</p>
          </div>
        </div>

        {/* Payment details */}
        <div className="card p-5 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-base"
              style={{ background: "linear-gradient(135deg, #6c63ff22 0%, #4f8eff22 100%)", border: "1px solid #6c63ff44" }}>
              🔷
            </div>
            <div>
              <p className="text-white font-semibold">Pay with ETH (ERC20)</p>
              <p className="text-[#555566] text-xs">Send exact amount to the address below</p>
            </div>
          </div>

          {/* Amount */}
          <div>
            <p className="text-[#8888aa] text-xs mb-2">Amount to send</p>
            <div className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-4 py-3">
              <p className="flex-1 text-white font-bold font-mono">
                {order.crypto_amount} {order.currency}
              </p>
              <button
                onClick={() => copyToClipboard(String(order.crypto_amount), "amount")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all
                  ${copied === "amount"
                    ? "bg-[#22d3a522] text-[#22d3a5]"
                    : "bg-[#2a2a3a] text-[#8888aa]"
                  }`}
              >
                <Copy size={12} />
                {copied === "amount" ? "Copied!" : "Copy"}
              </button>
            </div>
          </div>

          {/* Address */}
          <div>
            <p className="text-[#8888aa] text-xs mb-2">Send to address (TRC20)</p>
            <div className="flex items-center gap-2 bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-4 py-3">
              <p className="flex-1 text-white text-xs font-mono break-all leading-relaxed">
                {order.address}
              </p>
              <button
                onClick={() => copyToClipboard(order.address, "address")}
                className={`flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all
                  ${copied === "address"
                    ? "bg-[#22d3a522] text-[#22d3a5]"
                    : "bg-[#2a2a3a] text-[#8888aa]"
                  }`}
              >
                <Copy size={12} />
                {copied === "address" ? "Copied!" : "Copy"}
              </button>
            </div>
          </div>

          {/* Pay Now link */}
          {order.payment_url && (
            <a
              href={order.payment_url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => haptic("medium")}
              className="flex items-center justify-center gap-2 w-full py-3 rounded-xl text-sm font-semibold"
              style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 100%)" }}
            >
              <ExternalLink size={15} />
              Open Payment Page
            </a>
          )}
        </div>

        {/* Warning */}
        <div className="flex items-start gap-2 p-3 rounded-xl bg-[#ff4f6e11] border border-[#ff4f6e33]">
          <span className="text-[#ff4f6e] flex-shrink-0 mt-0.5">⚠️</span>
          <p className="text-[#ff4f6e] text-xs leading-relaxed">
            Send the <strong>exact amount</strong> in a <strong>single transaction</strong>.
            Wrong amounts may not be detected. Network fee is separate.
          </p>
        </div>

        {/* Check payment */}
        {status === "pending" && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-[#fbbf2422] border border-[#fbbf2444]">
            <Clock size={16} className="text-[#fbbf24]" />
            <p className="text-[#fbbf24] text-sm">Payment not confirmed yet. Please wait and try again.</p>
          </div>
        )}

        {checkError && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-[#ff4f6e11] border border-[#ff4f6e33]">
            <XCircle size={16} className="text-[#ff4f6e]" />
            <p className="text-[#ff4f6e] text-sm">{checkError}</p>
          </div>
        )}

        {(status === "expired" || (isExpired && status !== "paid")) && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-[#ff4f6e11] border border-[#ff4f6e33]">
            <XCircle size={16} className="text-[#ff4f6e]" />
            <p className="text-[#ff4f6e] text-sm">This payment has expired. Please create a new order.</p>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex flex-col gap-3 mt-auto">
          <button
            onClick={handleCheckPayment}
            disabled={status === "checking" || status === "paid" || isExpired}
            className="w-full btn-primary py-4 text-base flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {status === "checking" ? (
              <>
                <RefreshCw size={18} className="animate-spin" />
                Checking...
              </>
            ) : (
              <>
                <CheckCircle size={18} />
                I&apos;ve Sent Payment
              </>
            )}
          </button>

          <button
            onClick={handleCancel}
            className="w-full py-3 rounded-xl text-[#555566] text-sm font-medium border border-[#2a2a3a] bg-[#1a1a24]"
          >
            Cancel Order
          </button>
        </div>
      </div>
    </div>
  );
}
