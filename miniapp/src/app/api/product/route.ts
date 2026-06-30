import { NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "";

export async function GET() {
  if (!BOT_API) {
    // Return static fallback — useful for local dev without backend
    return NextResponse.json({
      name: "Gemini Pro 18-Month Subscription",
      price: 4.99,
      stock: 0,
      sold: 69987,
      rating: 4.8,
      reviews: 0,
      description: "Premium Gemini AI Pro access for 18 months via instant redemption link.",
    });
  }

  try {
    const res = await fetch(`${BOT_API}/product`, { next: { revalidate: 30 } });
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ error: "unavailable" }, { status: 503 });
  }
}
