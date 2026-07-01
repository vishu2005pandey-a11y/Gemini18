/**
 * API helper — calls the bot's backend API via Next.js proxy routes
 */

// In browser → use /api proxy routes (Next.js handles the backend URL server-side)
// In SSR → use BOT_BACKEND_URL directly (not used client-side)
const BASE = "/api";

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
  sold: number;
  rating: number;
  reviews: number;
  image_url: string;
  description: string;
}

export interface Order {
  order_id: string;
  quantity: number;
  amount_usd: number;
  currency: string;
  status: string;
  paid_at: string;
  links: string[];
}

export interface Wallet {
  balance: number;
  deposits: Deposit[];
}

export interface Deposit {
  amount: number;
  date: string;
}

export interface UserInfo {
  user_id: number;
  username: string | null;
  first_name: string;
  join_date: string;
  language: string;
  badge: string;
  total_orders: number;
  links_bought: number;
  total_spent: number;
  referral_balance: number;
}

export interface ReferralStats {
  total_invited: number;
  successful: number;
  pending: number;
  total_earnings: number;
  available_balance: number;
}

export interface LeaderboardEntry {
  username: string | null;
  first_name: string;
  total_links: number;
}

export interface Review {
  id: number;
  user_id: number;
  order_id: string;
  rating: number;
  comment: string | null;
  created_at: string;
  username: string | null;
}

export interface CreateOrderResult {
  order_id: string;
  address: string;
  crypto_amount: number;
  currency: string;
  payment_url: string;
  timeout: number;
  amount_usd: number;
}

export interface PaymentStatus {
  status: "paid" | "pending" | "expired" | "cancelled";
  links: string[];
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ── Product ──────────────────────────────────────────────────────────────────
export async function getProducts(): Promise<Product[]> {
  try {
    return await apiFetch<Product[]>("/products");
  } catch {
    return [{
      id: 1,
      name: "Premium Gemini AI Pro access",
      price: 4.99,
      stock: 0,
      sold: 69987,
      rating: 4.8,
      reviews: 0,
      image_url: "",
      description: "Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link.",
    }];
  }
}

// ── Orders ───────────────────────────────────────────────────────────────────
export async function getOrders(userId: number): Promise<Order[]> {
  try {
    return await apiFetch<Order[]>(`/orders?user_id=${userId}`);
  } catch {
    return [];
  }
}

// ── Wallet ───────────────────────────────────────────────────────────────────
export async function getWallet(userId: number): Promise<Wallet> {
  try {
    return await apiFetch<Wallet>(`/wallet?user_id=${userId}`);
  } catch {
    return { balance: 0, deposits: [] };
  }
}

// ── User ─────────────────────────────────────────────────────────────────────
export async function getUser(userId: number): Promise<UserInfo | null> {
  try {
    return await apiFetch<UserInfo>(`/user?user_id=${userId}`);
  } catch {
    return null;
  }
}

// ── Referral ─────────────────────────────────────────────────────────────────
export async function getReferral(userId: number): Promise<ReferralStats> {
  try {
    return await apiFetch<ReferralStats>(`/referral?user_id=${userId}`);
  } catch {
    return { total_invited: 0, successful: 0, pending: 0, total_earnings: 0, available_balance: 0 };
  }
}

// ── Leaderboard ──────────────────────────────────────────────────────────────
export async function getLeaderboard(period: string): Promise<LeaderboardEntry[]> {
  try {
    return await apiFetch<LeaderboardEntry[]>(`/leaderboard?period=${period}`);
  } catch {
    return [];
  }
}

// ── Reviews ──────────────────────────────────────────────────────────────────
export async function getReviews(): Promise<Review[]> {
  try {
    return await apiFetch<Review[]>("/reviews");
  } catch {
    return [];
  }
}

// ── Create Order ─────────────────────────────────────────────────────────────
export async function createOrder(
  userId: number,
  productId: number,
  qty: number,
  initData: string
): Promise<CreateOrderResult> {
  return apiFetch<CreateOrderResult>("/create_order", {
    method: "POST",
    body: JSON.stringify({ user_id: userId, product_id: productId, qty, tg_init_data: initData }),
  });
}

// ── Check Payment ─────────────────────────────────────────────────────────────
export async function checkPayment(orderId: string): Promise<PaymentStatus> {
  return apiFetch<PaymentStatus>("/check_payment", {
    method: "POST",
    body: JSON.stringify({ order_id: orderId }),
  });
}

// ── Cancel Order ─────────────────────────────────────────────────────────────
export async function cancelOrder(orderId: string): Promise<{ ok: boolean }> {
  try {
    return await apiFetch<{ ok: boolean }>("/cancel_order", {
      method: "POST",
      body: JSON.stringify({ order_id: orderId }),
    });
  } catch {
    return { ok: false };
  }
}

// ── Add Review ───────────────────────────────────────────────────────────────
export async function addReview(
  userId: number,
  orderId: string,
  rating: number,
  comment: string
): Promise<{ ok: boolean }> {
  try {
    return await apiFetch<{ ok: boolean }>("/add_review", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, order_id: orderId, rating, comment }),
    });
  } catch {
    return { ok: false };
  }
}
