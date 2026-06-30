import { NextRequest, NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "";

export async function GET(req: NextRequest) {
  const userId = req.nextUrl.searchParams.get("user_id");
  if (!userId) return NextResponse.json({ balance: 0, deposits: [] });

  if (!BOT_API) return NextResponse.json({ balance: 0, deposits: [] });

  try {
    const res = await fetch(`${BOT_API}/wallet?user_id=${userId}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ balance: 0, deposits: [] });
  }
}
