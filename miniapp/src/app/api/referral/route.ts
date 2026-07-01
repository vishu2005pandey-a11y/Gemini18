import { NextRequest, NextResponse } from "next/server";

const BOT_API = process.env.BOT_BACKEND_URL || "http://localhost:8080";

export async function GET(req: NextRequest) {
  const userId = req.nextUrl.searchParams.get("user_id");
  if (!userId) return NextResponse.json({});
  try {
    const res = await fetch(`${BOT_API}/referral?user_id=${userId}`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ total_invited: 0, successful: 0, pending: 0, total_earnings: 0, available_balance: 0 });
  }
}
