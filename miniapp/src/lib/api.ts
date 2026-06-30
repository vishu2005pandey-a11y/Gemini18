/**
 * API helper — calls the bot's backend API
 * The bot exposes a simple REST API for the Mini App
 */

const BASE = process.env.NEXT_PUBLIC_BOT_API || "";

export async function apiFetch(path: string, options?: RequestInit) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ── Product ──────────────────────────────────────────────────────────────────
export async function getProduct() {
  try {
    return await apiFetch("/api/product");
  } catch {
    // Fallback static data for demo / no backend
    return {
      name: "Gemini Pro 18-Month Subscription",
      price: 4.99,
      stock: 247,
      sold: 70234,
      rating: 4.8,
      reviews: 1420,
      description: "Premium Gemini AI Pro access for 18 months via instant redemption link.",
    };
  }
}

// ── Orders ───────────────────────────────────────────────────────────────────
export async function getOrders(userId: number) {
  try {
    return await apiFetch(`/api/orders?user_id=${userId}`);
  } catch {
    return [];
  }
}

// ── Wallet ───────────────────────────────────────────────────────────────────
export async function getWallet(userId: number) {
  try {
    return await apiFetch(`/api/wallet?user_id=${userId}`);
  } catch {
    return { balance: 0, deposits: [] };
  }
}

// ── User ─────────────────────────────────────────────────────────────────────
export async function getUser(userId: number) {
  try {
    return await apiFetch(`/api/user?user_id=${userId}`);
  } catch {
    return null;
  }
}

// ── Referral ─────────────────────────────────────────────────────────────────
export async function getReferral(userId: number) {
  try {
    return await apiFetch(`/api/referral?user_id=${userId}`);
  } catch {
    return { total_invited: 0, successful: 0, total_earnings: 0, available_balance: 0 };
  }
}
