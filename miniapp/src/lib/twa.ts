/**
 * Telegram Web App helper — safely access window.Telegram.WebApp
 */

export function getTWA() {
  if (typeof window === "undefined") return null;
  return (window as any).Telegram?.WebApp ?? null;
}

export function getTWAUser() {
  const twa = getTWA();
  return twa?.initDataUnsafe?.user ?? null;
}

export function closeMiniApp() {
  getTWA()?.close();
}

export function haptic(type: "light" | "medium" | "heavy" | "success" | "error" = "light") {
  const twa = getTWA();
  if (!twa) return;
  if (type === "success") twa.HapticFeedback?.notificationOccurred("success");
  else if (type === "error") twa.HapticFeedback?.notificationOccurred("error");
  else twa.HapticFeedback?.impactOccurred(type);
}

export function openTelegramLink(url: string) {
  getTWA()?.openTelegramLink(url);
}
