import { NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "http://localhost:8080";

export async function GET() {
  try {
    const res = await fetch(`${BOT_API}/products`, { next: { revalidate: 30 } });
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([]);
  }
}
