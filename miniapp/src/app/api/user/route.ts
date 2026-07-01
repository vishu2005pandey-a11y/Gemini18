import { NextRequest, NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "http://localhost:8080";

export async function GET(req: NextRequest) {
  const userId = req.nextUrl.searchParams.get("user_id");
  if (!userId) return NextResponse.json({ error: "missing user_id" }, { status: 400 });
  try {
    const res = await fetch(`${BOT_API}/user?user_id=${userId}`);
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ error: "unavailable" }, { status: 503 });
  }
}
