import { NextRequest, NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "http://localhost:8080";

export async function GET(req: NextRequest) {
  const period = req.nextUrl.searchParams.get("period") || "alltime";
  try {
    const res = await fetch(`${BOT_API}/leaderboard?period=${period}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([]);
  }
}
