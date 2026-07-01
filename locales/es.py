"""Spanish locale strings — with Telegram Premium Emoji."""
from locales.en import (
    E_LIGHTNING, E_STAR, E_DIAMOND, E_CROWN, E_TROPHY, E_ROCKET,
    E_MONEY, E_FIRE, E_SHIELD, E_SPARKLES, E_CHART, E_CART,
    E_PACKAGE, E_LOCK, E_CHECK, E_WAVE, E_GIFT, E_LINK, E_KEY,
    E_BELL, E_TARGET, E_MEDAL, E_CLOCK, E_WARNING, E_CROSS,
    E_CARD, E_REVIEW, E_SUPPORT, E_ROBOT, E_CROWN2,
    E_BRONZE, E_SILVER, E_GOLD
)

STRINGS = {
    # ── Welcome / Force Join ─────────────────────────────────────────────
    "force_join_title": (
        f"{E_WAVE} <b>¡Bienvenido a Alpha Shop!</b>\n\n"
        f"{E_LOCK} <b>Por favor únete a nuestra comunidad para continuar:</b>\n\n"
        "📢 <b>Canal:</b> <a href='{channel_link}'>Alpha Oficial</a>\n"
        "💬 <b>Grupo:</b> <a href='{group_link}'>Alpha Comunidad</a>\n\n"
        f"{E_CHECK} <i>Después de unirte, toca <b>\"Me Uní\"</b> abajo.</i>"
    ),
    "force_join_not_member": (
        f"{E_WARNING} <b>Acceso Denegado</b>\n\n"
        "Aún no te has unido a nuestro canal y grupo.\n"
        "Por favor únete a ambos e intenta nuevamente."
    ),
    "btn_join_channel": "📢 Unirse al Canal",
    "btn_join_group":   "💬 Unirse al Grupo",
    "btn_i_joined":     "✅ Me Uní — Continuar",

    # ── Main Menu ────────────────────────────────────────────────────────
    "welcome": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LIGHTNING} <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"¡Hola {{name}}! {E_WAVE}\n\n"
        f"{E_SPARKLES} <b>Productos digitales premium — mejores precios.</b>\n"
        f"{E_ROCKET} Rápido  {E_SHIELD} Seguro  {E_CHECK} Totalmente Automatizado\n\n"
        "┌──────────────────────────\n"
        f"│ {E_CART}  <b>Tienda</b> — Explorar y comprar\n"
        f"│ {E_DIAMOND}  <b>Perfil</b> — Tus stats e historial\n"
        f"│ {E_GIFT}  <b>Referido</b> — Invitar y ganar\n"
        f"│ {E_SUPPORT}  <b>Soporte</b> — Obtener ayuda\n"
        "└──────────────────────────\n\n"
        f"{E_CHART} <b>{{links_sold}}+</b> links vendidos  •  <b>{{stock}}</b> disponibles\n\n"
        f"Elige una opción {E_FIRE}"
    ),
    "btn_shop":        "🛍️  Tienda",
    "btn_profile":     "👤  Mi Perfil",
    "btn_orders":      "📦  Mis Pedidos",
    "btn_referral":    "🔗  Referir & Ganar",
    "btn_support":     "🆘  Soporte",
    "btn_leaderboard": "🏆  Clasificación",
    "btn_reviews":     "⭐  Reseñas",
    "btn_back":        "◀️  Volver",
    "btn_main_menu":   "🏠  Menú Principal",

    # ── Shop ─────────────────────────────────────────────────────────────
    "shop_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>ALPHA TIENDA</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_STAR} <b>Producto Destacado</b>\n\n"
    ),
    "product_card": (
        "╔══════════════════════════╗\n"
        f"  {E_ROBOT} <b>{{name}}</b>\n"
        "╚══════════════════════════╝\n\n"
        f"{E_PACKAGE} <b>Descripción:</b>\n"
        "  Acceso premium a Gemini AI Pro por 18 meses.\n"
        "  Entrega instantánea via enlace de canje.\n\n"
        f"{E_MONEY} <b>Precio:</b>  <code>${{price}}</code> por enlace\n"
        f"{E_PACKAGE} <b>Stock:</b>   <code>{{stock}}</code> disponibles\n"
        f"{E_CHART} <b>Vendido:</b> <code>{{sold}}+</code> enlaces\n\n"
        f"{E_STAR} <b>Rating:</b> {{rating}} ({{review_count}} reseñas)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Selecciona cantidad {E_FIRE}"
    ),
    "out_of_stock": (
        f"{E_CROSS} <b>Sin Stock</b>\n\n"
        "¡Pronto habrá reposición! Activa alertas de stock en tu perfil."
    ),
    "btn_buy_1":      "1× Enlace — ${price}",
    "btn_buy_3":      "3× Enlaces — ${price}",
    "btn_buy_5":      "5× Enlaces — ${price}",
    "btn_buy_10":     "10× Enlaces — ${price}",
    "btn_custom_qty": "✏️  Cantidad Personalizada",

    # ── Terms ────────────────────────────────────────────────────────────
    "terms": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_SHIELD} <b>TÉRMINOS Y CONDICIONES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_WARNING} <b>Importante — Por favor lee detenidamente</b>\n\n"
        f"{E_CHECK} Garantía <b>exclusivamente para los enlaces</b> — válida <b>solo 24 horas</b> desde la entrega.\n\n"
        f"{E_KEY} Cubre <b>solo la activación del enlace</b>, no la duración de la suscripción.\n\n"
        f"{E_CROSS} <b>No se harán reemplazos</b> después del período de 24 horas.\n\n"
        f"{E_CLOCK} Activa tus enlaces <b>dentro del tiempo establecido</b>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Al continuar aceptas estos términos."
    ),
    "btn_agree":   "✅  Aceptar y Continuar",
    "btn_decline": "❌  Rechazar",

    # ── Payment ──────────────────────────────────────────────────────────
    "payment_invoice": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CARD} <b>FACTURA DE PAGO</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_CART} <b>Resumen del Pedido</b>\n"
        "  📦 Producto:   {product}\n"
        "  🔢 Cantidad:   {qty}× enlace(s)\n"
        f"  {E_MONEY} Total:      <code>${{total}}</code>\n\n"
        f"{E_CARD} <b>Detalles de Pago</b>\n"
        "  💱 Moneda:     {currency}\n"
        f"  {E_KEY} Monto:      <code>{{crypto_amount}} {{currency}}</code>\n"
        "  📋 Dirección:  <code>{address}</code>\n\n"
        f"{E_CLOCK} <b>Expira en:</b> {{timeout}} minutos\n"
        "🆔 <b>ID de Pedido:</b>  <code>{order_id}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LIGHTNING} Envía el monto exacto a la dirección.\n"
        "Entrega instantánea tras confirmación."
    ),
    "btn_check_payment":  "🔄  Verificar Pago",
    "btn_cancel_payment": "❌  Cancelar Pedido",
    "payment_pending":    f"{E_CLOCK} Pago aún no confirmado. Envía el monto exacto e intenta nuevamente.",
    "payment_expired":    f"{E_CLOCK} <b>Pago Expirado</b>\n\nTu factura ha expirado. Por favor realiza un nuevo pedido.",
    "payment_cancelled":  f"{E_CROSS} Pedido cancelado.",

    # ── Delivery ─────────────────────────────────────────────────────────
    "delivery_success": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHECK} <b>¡PAGO CONFIRMADO!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_SPARKLES} ¡Gracias por tu compra!\n\n"
        f"{E_PACKAGE} <b>Tus Enlaces Gemini Pro:</b>\n\n"
        "{{links}}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} <b>Garantía:</b> 24 horas desde ahora\n"
        "🆔 <b>ID de Pedido:</b> <code>{{order_id}}</code>\n\n"
        f"{E_WARNING} ¡Activa tus enlaces dentro de 24 horas!\n"
        f"{E_SUPPORT} ¿Problemas? Usa /support"
    ),

    # ── Profile ──────────────────────────────────────────────────────────
    "profile": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_DIAMOND} <b>MI PERFIL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🪪 <b>ID Usuario:</b>      <code>{user_id}</code>\n"
        "📅 <b>Miembro desde:</b>  {join_date}\n"
        f"{E_MEDAL} <b>Insignia:</b>       {{badge}}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHART} <b>Estadísticas</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_PACKAGE} <b>Pedidos:</b>        {{total_orders}}\n"
        f"{E_LINK} <b>Links Comprados:</b> {{links_bought}}\n"
        f"{E_MONEY} <b>Total Gastado:</b>  <code>${{total_spent}}</code>\n"
        f"{E_GIFT} <b>Ganancias Ref.:</b> <code>${{referral_earnings}}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_TROPHY} <b>Logros</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{{achievements}}\n\n"
        f"{E_BELL} <b>Notificaciones:</b>  {{notifications}}"
    ),
    "btn_toggle_notifications": "🔔  Notificaciones",
    "btn_change_language":      "🌐  Idioma",

    # ── Orders ───────────────────────────────────────────────────────────
    "orders_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_PACKAGE} <b>HISTORIAL DE PEDIDOS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Tienes <b>{count}</b> pedido(s).\n\n"
    ),
    "order_item": (
        "🆔 <code>{order_id}</code>\n"
        "📅 {date}  •  🔢 {qty}×  •  💰 ${amount}\n"
        "─────────────────────────\n"
    ),
    "no_orders": (
        f"{E_PACKAGE} Aún no has realizado compras.\n\n"
        f"¡Ve a {E_CART} Tienda para comenzar!"
    ),
    "btn_search_order": "🔍  Buscar Pedido",

    # ── Referral ─────────────────────────────────────────────────────────
    "referral_dashboard": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_GIFT} <b>REFERIR & GANAR</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_MONEY} ¡Gana <b>${{reward}}</b> por cada amigo que haga su primera compra!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHART} <b>Tus Stats</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 <b>Total Invitados:</b>    {total_invited}\n"
        f"{E_CHECK} <b>Exitosos:</b>           {{successful}}\n"
        f"{E_CLOCK} <b>Pendientes:</b>         {{pending}}\n"
        f"{E_MONEY} <b>Total Ganado:</b>       <code>${{total_earnings}}</code>\n"
        f"{E_DIAMOND} <b>Balance Disponible:</b> <code>${{available_balance}}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LINK} <b>Tu Enlace de Invitación:</b>\n"
        "<code>{referral_link}</code>\n\n"
        f"<i>{E_LIGHTNING} Recompensas solo tras la primera compra de tu amigo.</i>"
    ),
    "btn_copy_link": "📋  Copiar Enlace",
    "btn_withdraw":  "💸  Retirar Ganancias",

    # ── Leaderboard ──────────────────────────────────────────────────────
    "leaderboard_weekly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_TROPHY} <b>TOP COMPRADORES SEMANALES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Actualizado: {{updated}}"
    ),
    "leaderboard_monthly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_STAR} <b>TOP COMPRADORES MENSUALES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Actualizado: {{updated}}"
    ),
    "leaderboard_alltime": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CROWN} <b>TOP COMPRADORES DE TODOS LOS TIEMPOS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Actualizado: {{updated}}"
    ),
    "leaderboard_entry": "{{rank}}  {{username}}   {E_LINK} {{links}} enlaces",
    "btn_weekly":  "📅  Semanal",
    "btn_monthly": "🗓️  Mensual",
    "btn_alltime": "👑  Todo el Tiempo",

    # ── Reviews ──────────────────────────────────────────────────────────
    "reviews_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_STAR} <b>RESEÑAS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Promedio: <b>{avg_rating}</b>/5  ({count} reseñas)\n\n"
        "{reviews}"
    ),
    "review_item":         f"{E_STAR} {{stars}}  •  {{username}}\n<i>{{comment}}</i>\n─────────────────\n",
    "leave_review_prompt": f"{E_STAR} <b>Dejar una Reseña</b>\n\nCalifica tu compra del 1 al 5:",
    "btn_leave_review":    "⭐  Dejar Reseña",
    "review_saved":        f"{E_CHECK} ¡Gracias por tu reseña!",

    # ── Support ──────────────────────────────────────────────────────────
    "support": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_SUPPORT} <b>SOPORTE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_SHIELD} ¿Necesitas ayuda? Estamos aquí.\n\n"
        f"{E_PACKAGE} <b>¿Problema con pedido?</b>  Usa /search.\n"
        "💬 <b>Soporte en vivo:</b> Contacta a un admin en el grupo.\n\n"
        "<i>Por favor incluye tu ID de Pedido al contactar soporte.</i>"
    ),

    # ── Maintenance ──────────────────────────────────────────────────────
    "maintenance": (
        f"{E_WARNING} <b>Modo Mantenimiento</b>\n\n"
        "Estamos actualizando el bot.\n"
        f"Por favor vuelve pronto. {E_CLOCK}\n\n"
        "<i>Disculpa las molestias.</i>"
    ),

    # ── Notifications ────────────────────────────────────────────────────
    "notifications_menu":  f"{E_BELL} <b>Configuración de Notificaciones</b>\n\nActiva o desactiva:",
    "notif_stock":         "📦 Alertas de Stock",
    "notif_announcements": "📢 Anuncios",
    "notif_discounts":     "🏷️ Alertas de Descuentos",

    # ── Admin ────────────────────────────────────────────────────────────
    "admin_panel": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ <b>PANEL ADMIN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>Usuarios:</b>       {{total_users}}\n"
        f"{E_PACKAGE} <b>Pedidos:</b>        {{total_orders}}\n"
        f"{E_MONEY} <b>Ingresos:</b>       <code>${{total_revenue}}</code>\n"
        f"{E_CHART} <b>Hoy:</b>            <code>${{today_revenue}}</code>\n"
        f"{E_LINK} <b>Links Vendidos:</b> {{links_sold}}\n"
        f"{E_CHART} <b>Stock:</b>          {{stock}} restantes\n\n"
        "Elige una acción 👇"
    ),
    "btn_upload_stock":      "📤  Subir Stock",
    "btn_set_price":         "💲  Fijar Precio",
    "btn_broadcast":         "📢  Difundir",
    "btn_ban_user":          "🚫  Banear Usuario",
    "btn_unban_user":        "✅  Desbanear Usuario",
    "btn_view_users":        "👥  Ver Usuarios",
    "btn_view_sales":        "📊  Ver Ventas",
    "btn_maintenance":       "🔧  Mantenimiento",
    "btn_referral_settings": "🎁  Config. Referidos",

    # ── Misc ─────────────────────────────────────────────────────────────
    "error_generic":      f"{E_CROSS} Algo salió mal. Por favor intenta nuevamente.",
    "banned":             "🚫 Has sido baneado de este bot.",
    "custom_qty_prompt":  "✏️ Ingresa la cantidad que deseas comprar (1–100):",
    "invalid_qty":        f"{E_CROSS} Cantidad inválida. Ingresa un número entre 1 y 100.",
    "insufficient_stock": f"{E_CROSS} Stock insuficiente. Solo hay {{stock}} enlace(s) disponibles.",
    "language_menu":      "🌐 <b>Seleccionar Idioma</b>",
    "btn_lang_en":        "🇬🇧 English",
    "btn_lang_es":        "🇪🇸 Español",
    "search_prompt":      "🔍 Ingresa tu ID de Pedido para buscar:",
    "order_not_found":    f"{E_CROSS} Pedido <code>{{order_id}}</code> no encontrado.",
    "upload_stock_prompt":f"{E_PACKAGE} Envía un archivo .txt con un enlace por línea.",
    "stock_uploaded":     f"{E_CHECK} <b>{{count}}</b> nuevos links cargados.\n{E_CHART} Stock total: <b>{{total}}</b>",
    "price_set":          f"{E_CHECK} Precio actualizado a <code>${{price}}</code> por link.",
    "broadcast_prompt":   "📢 Escribe tu mensaje de difusión:",
    "broadcast_sent":     f"{E_CHECK} Difusión enviada a <b>{{count}}</b> usuarios.",
    "ban_prompt":         "🚫 Ingresa el ID de usuario a banear:",
    "ban_success":        f"{E_CHECK} Usuario <code>{{user_id}}</code> ha sido baneado.",
    "unban_prompt":       "✅ Ingresa el ID de usuario a desbanear:",
    "unban_success":      f"{E_CHECK} Usuario <code>{{user_id}}</code> ha sido desbaneado.",
    "maintenance_on":     f"🔧 Modo mantenimiento <b>activado</b>.",
    "maintenance_off":    f"{E_CHECK} Modo mantenimiento <b>desactivado</b>.",
    "achievement_unlocked": f"{E_TROPHY} <b>¡Logro Desbloqueado!</b>\n\n{{label}}",
    "new_badge":          f"{E_MEDAL} <b>¡Nueva Insignia!</b>\n\nHas ganado: {{badge}}",
    "set_price_prompt":   f"{E_MONEY} Ingresa el nuevo precio por link (USD):",
    "purchase_log": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>NUEVA COMPRA</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>Usuario:</b>  @{{username}} (<code>{{user_id}}</code>)\n"
        "🆔 <b>ID Pedido:</b> <code>{{order_id}}</code>\n"
        "🔢 <b>Cantidad:</b>  {{qty}}× enlace(s)\n"
        f"{E_MONEY} <b>Monto:</b>     <code>${{amount}}</code>\n"
        "💱 <b>Método:</b>    {{method}}\n"
        "📅 <b>Fecha:</b>     {{date}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
    "low_stock_alert": (
        f"{E_WARNING} <b>ALERTA: STOCK BAJO</b>\n\n"
        f"¡Solo quedan <b>{{stock}}</b> links! {E_FIRE}\n"
        "Por favor sube más stock."
    ),
}
