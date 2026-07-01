"use client";
import { Heart, ShoppingCart } from "lucide-react";
import { haptic } from "@/lib/twa";
import Image from "next/image";

interface Props {
  name: string;
  price: number;
  sold?: number;
  stock?: number;
  isNew?: boolean;
  isSale?: boolean;
  outOfStock?: boolean;
  imageUrl?: string;
  onBuy: () => void;
}

export default function ProductCard({
  name, price, sold, stock, isNew, isSale, outOfStock, imageUrl, onBuy,
}: Props) {
  return (
    <div className="card p-3 flex flex-col gap-2 relative">
      {/* Tags */}
      <div className="absolute top-3 left-3 flex gap-1 z-10">
        {isSale && <span className="tag-sale">sale</span>}
        {isNew && <span className="tag-new">new</span>}
        {outOfStock && (
          <span className="bg-[#555566] text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">
            out of stock
          </span>
        )}
      </div>

      {/* Wishlist */}
      <button className="absolute top-3 right-3 z-10 text-[#555566] hover:text-[#ff4f6e] transition-colors">
        <Heart size={16} />
      </button>

      {/* Product Image */}
      <div className="w-full aspect-square rounded-xl bg-[#1a1a24] flex items-center justify-center mt-1 overflow-hidden">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={name}
            width={200}
            height={200}
            className="w-full h-full object-cover rounded-xl"
            unoptimized
          />
        ) : (
          <span className="text-4xl">🤖</span>
        )}
      </div>

      {/* Info */}
      <div className="flex flex-col gap-0.5">
        <p className="text-[13px] font-semibold text-white leading-tight line-clamp-2">{name}</p>
        {sold !== undefined && (
          <p className="text-[11px] text-[#555566]">{sold.toLocaleString()} sold</p>
        )}
      </div>

      {/* Price + Buy */}
      <div className="flex items-center justify-between mt-auto">
        <span className="text-[15px] font-bold text-white">${price.toFixed(2)}</span>
        <button
          onClick={() => { haptic("medium"); onBuy(); }}
          disabled={outOfStock}
          className="flex items-center gap-1.5 btn-primary text-[12px] px-3 py-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <ShoppingCart size={13} />
          Buy
        </button>
      </div>
    </div>
  );
}
