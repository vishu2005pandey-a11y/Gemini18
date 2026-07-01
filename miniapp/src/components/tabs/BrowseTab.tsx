"use client";
import { ShoppingBag, Star, Package } from "lucide-react";
import { useState } from "react";
import BuyModal from "../BuyModal";
import { haptic } from "@/lib/twa";
import { Product } from "@/lib/api";
import Image from "next/image";

interface Props {
  products: Product[];
  userId: number | null;
  onBuySuccess: () => void;
}

export default function BrowseTab({ products, userId, onBuySuccess }: Props) {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  return (
    <div className="flex flex-col gap-4 pb-4">
      {/* Header */}
      <div className="bg-[#111118] px-4 pt-4 pb-4 border-b border-[#2a2a3a]">
        <h1 className="text-white font-bold text-xl">Browse</h1>
        <p className="text-[#555566] text-sm mt-0.5">All available products</p>
      </div>

      <div className="px-4 flex flex-col gap-4">
        {products.length > 0 ? (
          <>
            {/* Product list */}
            {products.map(product => (
              <div key={product.id} className="card p-5 flex flex-col gap-4">
                {/* Image */}
                <div className="w-full h-40 rounded-2xl bg-[#1a1a24] flex items-center justify-center overflow-hidden">
                  {product.image_url ? (
                    <Image
                      src={product.image_url}
                      alt={product.name}
                      width={200}
                      height={160}
                      className="object-contain w-full h-full"
                      unoptimized
                    />
                  ) : (
                    <span className="text-6xl">??</span>
                  )}
                </div>

                {/* Name + stock badge */}
                <div className="flex items-start justify-between gap-2">
                  <h2 className="text-white font-bold text-lg leading-tight flex-1">{product.name}</h2>
                  {product.stock > 0 ? (
                    <span className="flex-shrink-0 text-xs px-2.5 py-1 rounded-full bg-[#22d3a522] text-[#22d3a5] font-medium">
                      ? In Stock
                    </span>
                  ) : (
                    <span className="flex-shrink-0 text-xs px-2.5 py-1 rounded-full bg-[#ff4f6e22] text-[#ff4f6e] font-medium">
                      ? Out of Stock
                    </span>
                  )}
                </div>

                {/* Description */}
                {product.description && (
                  <p className="text-[#8888aa] text-sm leading-relaxed">{product.description}</p>
                )}

                {/* Stats row */}
                <div className="flex items-center gap-4 text-sm flex-wrap">
                  <div className="flex items-center gap-1">
                    <Star size={14} className="text-[#fbbf24]" fill="#fbbf24" />
                    <span className="text-white font-semibold">{product.rating}</span>
                    <span className="text-[#555566]">({product.reviews} reviews)</span>
                  </div>
                  <span className="text-[#555566]">•</span>
                  <span className="text-[#555566]">{product.sold.toLocaleString()} sold</span>
                  <span className="text-[#555566]">•</span>
                  <span className="text-[#555566]">{product.stock} in stock</span>
                </div>

                {/* Price + Buy */}
                <div className="flex items-center justify-between pt-1 border-t border-[#2a2a3a]">
                  <div>
                    <p className="text-[#555566] text-xs">Price per link</p>
                    <p className="text-white font-bold text-2xl">${product.price.toFixed(2)}</p>
                  </div>
                  <button
                    disabled={product.stock <= 0}
                    onClick={() => { haptic("medium"); setSelectedProduct(product); }}
                    className="btn-primary px-6 py-3 flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <ShoppingBag size={16} />
                    Buy Now
                  </button>
                </div>
              </div>
            ))}
          </>
        ) : (
          /* Empty state — no product uploaded yet */
          <div className="card p-10 flex flex-col items-center gap-4 text-center mt-4">
            <div className="w-16 h-16 rounded-2xl bg-[#1a1a24] flex items-center justify-center">
              <Package size={28} className="text-[#555566]" />
            </div>
            <div>
              <p className="text-white font-semibold">No Products Yet</p>
              <p className="text-[#555566] text-sm mt-1">
                Admin hasn't uploaded any products yet.
              </p>
            </div>
          </div>
        )}
      </div>

      {selectedProduct && (
        <BuyModal
          product={{ id: selectedProduct.id, name: selectedProduct.name, price: selectedProduct.price, stock: selectedProduct.stock }}
          userId={userId}
          onClose={() => setSelectedProduct(null)}
          onSuccess={() => { setSelectedProduct(null); onBuySuccess(); }}
        />
      )}
    </div>
  );
}
