import { NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "http://localhost:8080";

export async function GET() {
  try {
    const res = await fetch(`${BOT_API}/product`, { next: { revalidate: 30 } });
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({
      name: "Gemini Pro 18-Month Subscription",
      price: 4.99,
      stock: 0,
      sold: 69987,
      rating: 4.8,
      reviews: 0,
      image_url: "",
      description: "Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link.",
    });
  }
}
