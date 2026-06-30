"use client";
import { Download, ArrowDownCircle } from "lucide-react";
import { useState } from "react";
import { haptic } from "@/lib/twa";

interface Props {
  wallet: { balance: number; deposits: any[] };
}

const PRESETS = [10, 25, 50, 100, 250, 500];

export default function WalletTab({ wallet }: Props) {
  const [custom, setCustom] = useState("");

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Wallet</h1>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {/* Balance Card */}
        <div
          className="rounded-2xl p-6"
          style={{ background: "linear-gradient(135deg, #6c63ff 0%, #4f8eff 60%, #22d3a5 100%)" }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-5 h-5 rounded border-2 border-white/40 flex items-center justify-center">
              <span className="text-[8px] text-white font-bold">$</span>
            </div>
            <p className="text-white/70 text-xs font-medium uppercase tracking-wide">Available Balance</p>
          </div>
          <p className="text-white font-bold text-4xl mb-1">
            ${wallet.balance.toFixed(2)}
          </p>
          <p className="text-white/60 text-sm">USDT • Use at checkout for instant payments</p>
        </div>

        {/* Add funds */}
        <div className="card p-5">
          <div className="flex items-center gap-2 mb-4">
            <Download size={16} className="text-[#6c63ff]" />
            <h2 className="text-white font-semibold">Add funds</h2>
          </div>

          {/* Preset amounts */}
          <div className="grid grid-cols-3 gap-2 mb-4">
            {PRESETS.map((amount) => (
              <button
                key={amount}
                onClick={() => { haptic("light"); setCustom(amount.toString()); }}
                className={`py-3 rounded-xl font-semibold text-sm border transition-all
                  ${custom === amount.toString()
                    ? "border-[#6c63ff] text-[#6c63ff] bg-[#6c63ff11]"
                    : "border-[#2a2a3a] text-white bg-[#1a1a24]"
                  }`}
              >
                ${amount}
              </button>
            ))}
          </div>

          {/* Custom input */}
          <div className="mb-2">
            <p className="text-[#8888aa] text-xs mb-2">Custom amount (USDT)</p>
            <div className="flex gap-2">
              <div className="flex-1 flex items-center bg-[#1a1a24] border border-[#2a2a3a] rounded-xl px-4">
                <span className="text-[#555566] mr-2">$</span>
                <input
                  type="number"
                  value={custom}
                  onChange={(e) => setCustom(e.target.value)}
                  placeholder="0.00"
                  className="flex-1 bg-transparent text-white py-3 outline-none placeholder:text-[#555566]"
                />
              </div>
              <button
                onClick={() => haptic("medium")}
                className="btn-primary px-6"
              >
                Deposit
              </button>
            </div>
          </div>

          <p className="text-[#555566] text-xs flex items-center gap-1">
            <span>⚡</span>
            Pay with USDT (TRC20 / BEP20). Funds credit automatically after on-chain confirmation.
          </p>
        </div>

        {/* Recent deposits */}
        <div className="card p-5">
          <h2 className="text-white font-semibold mb-4">Recent deposits</h2>

          {!wallet.deposits || wallet.deposits.length === 0 ? (
            <div className="flex flex-col items-center py-6 gap-2">
              <ArrowDownCircle size={32} className="text-[#2a2a3a]" />
              <p className="text-[#555566] text-sm">No deposits yet</p>
              <p className="text-[#555566] text-xs">Top up to pay faster at checkout</p>
            </div>
          ) : (
            wallet.deposits.map((d: any, i: number) => (
              <div key={i} className="flex items-center justify-between py-3 border-b border-[#2a2a3a] last:border-0">
                <div>
                  <p className="text-white text-sm font-medium">+${d.amount}</p>
                  <p className="text-[#555566] text-xs">{d.date}</p>
                </div>
                <span className="text-[10px] px-2 py-1 rounded-full bg-[#22d3a522] text-[#22d3a5]">Confirmed</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
