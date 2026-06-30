"""Spanish locale strings."""

STRINGS = {
    # ── Welcome / Force Join ──────────────────────────────────────────────
    "force_join_title": (
        "👋 <b>¡Bienvenido a Alpha Shop!</b>\n\n"
        "🔐 <b>Por favor únete a nuestra comunidad para continuar:</b>\n\n"
        "📢 <b>Canal:</b> <a href='{channel_link}'>Alpha Oficial</a>\n"
        "💬 <b>Grupo:</b> <a href='{group_link}'>Alpha Comunidad</a>\n\n"
        "✅ <i>Después de unirte, toca <b>\"Me Uní\"</b> abajo.</i>"
    ),
    "force_join_not_member": (
        "⚠️ <b>Acceso Denegado</b>\n\n"
        "Aún no te has unido a nuestro canal y grupo.\n"
        "Por favor únete a ambos e intenta nuevamente."
    ),
    "btn_join_channel": "📢 Unirse al Canal",
    "btn_join_group": "💬 Unirse al Grupo",
    "btn_i_joined": "✅ Me Uní — Continuar",

    # ── Main Menu ─────────────────────────────────────────────────────────
    "welcome": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "¡Hola {name}! 👋\n\n"
        "✨ <b>Productos digitales premium — mejores precios.</b>\n"
        "Rápido • Seguro • Totalmente Automatizado\n\n"
        "┌──────────────────────────\n"
        "│ 🛍️  <b>Tienda</b> — Explorar y comprar\n"
        "│ 👤  <b>Perfil</b> — Tus stats e historial\n"
        "│ 🔗  <b>Referido</b> — Invitar y ganar\n"
        "│ 🆘  <b>Soporte</b> — Obtener ayuda\n"
        "└──────────────────────────\n\n"
        "📊 <b>{links_sold}+</b> links vendidos  •  <b>{stock}</b> disponibles\n\n"
        "Elige una opción 👇"
    ),
    "btn_shop": "🛍️  Tienda",
    "btn_profile": "👤  Mi Perfil",
    "btn_orders": "📦  Mis Pedidos",
    "btn_referral": "🔗  Referir & Ganar",
    "btn_support": "🆘  Soporte",
    "btn_leaderboard": "🏆  Clasificación",
    "btn_reviews": "⭐  Reseñas",
    "btn_back": "◀️  Volver",
    "btn_main_menu": "🏠  Menú Principal",

    # ── Shop / Product ────────────────────────────────────────────────────
    "shop_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛍️ <b>ALPHA TIENDA</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌟 <b>Producto Destacado</b>\n\n"
    ),
    "product_card": (
        "╔══════════════════════════╗\n"
        "  🤖 <b>{name}</b>\n"
        "╚══════════════════════════╝\n\n"
        "📋 <b>Descripción:</b>\n"
        "  Acceso premium a Gemini AI Pro por 18 meses.\n"
        "  Entrega instantánea via enlace de canje.\n\n"
        "💰 <b>Precio:</b>  <code>${price}</code> por enlace\n"
        "📦 <b>Stock:</b>   <code>{stock}</code> disponibles\n"
        "📊 <b>Vendido:</b> <code>{sold}+</code> enlaces\n\n"
        "⭐ <b>Rating:</b> {rating} ({review_count} reseñas)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Selecciona cantidad 👇"
    ),
    "out_of_stock": "❌ <b>Sin Stock</b>\n\n¡Pronto habrá reposición! Activa alertas de stock en tu perfil.",
    "btn_buy_1": "1× Enlace — ${price}",
    "btn_buy_3": "3× Enlaces — ${price}",
    "btn_buy_5": "5× Enlaces — ${price}",
    "btn_buy_10": "10× Enlaces — ${price}",
    "btn_custom_qty": "✏️  Cantidad Personalizada",

    # ── Terms & Conditions ────────────────────────────────────────────────
    "terms": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📜 <b>TÉRMINOS Y CONDICIONES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚠️ <b>Importante — Por favor lee detenidamente</b>\n\n"
        "✅ Esta garantía es <b>exclusivamente para los enlaces de Gemini</b> y tiene validez de <b>solo 24 horas</b> desde la entrega.\n\n"
        "📌 La garantía cubre <b>solo la activación del enlace</b>, no la duración de la suscripción después del canje.\n\n"
        "🚫 <b>No se harán reemplazos</b> después del período de 24 horas.\n\n"
        "⏰ Por favor activa tus enlaces <b>dentro del tiempo establecido</b>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Al continuar aceptas estos términos."
    ),
    "btn_agree": "✅  Aceptar y Continuar",
    "btn_decline": "❌  Rechazar",

    # ── Payment ───────────────────────────────────────────────────────────
    "payment_invoice": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>FACTURA DE PAGO</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛒 <b>Resumen del Pedido</b>\n"
        "  📦 Producto:   {product}\n"
        "  🔢 Cantidad:   {qty}× enlace(s)\n"
        "  💰 Total:      <code>${total}</code>\n\n"
        "💳 <b>Detalles de Pago</b>\n"
        "  💱 Moneda:     {currency}\n"
        "  🔑 Monto:      <code>{crypto_amount} {currency}</code>\n"
        "  📋 Dirección:  <code>{address}</code>\n\n"
        "⏳ <b>Expira en:</b> {timeout} minutos\n"
        "🆔 <b>ID de Pedido:</b>  <code>{order_id}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ Envía el monto exacto a la dirección.\n"
        "La entrega es instantánea tras confirmación."
    ),
    "btn_check_payment": "🔄  Verificar Pago",
    "btn_cancel_payment": "❌  Cancelar Pedido",
    "payment_pending": "⏳ Pago aún no confirmado. Envía el monto exacto e intenta nuevamente.",
    "payment_expired": "⌛ <b>Pago Expirado</b>\n\nTu factura ha expirado. Por favor realiza un nuevo pedido.",
    "payment_cancelled": "❌ Pedido cancelado.",

    # ── Delivery ──────────────────────────────────────────────────────────
    "delivery_success": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ <b>¡PAGO CONFIRMADO!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎉 ¡Gracias por tu compra!\n\n"
        "📦 <b>Tus Enlaces Gemini Pro:</b>\n\n"
        "{links}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⏰ <b>Garantía:</b> 24 horas desde ahora\n"
        "🆔 <b>ID de Pedido:</b> <code>{order_id}</code>\n\n"
        "⚠️ ¡Activa tus enlaces dentro de 24 horas!\n"
        "💬 ¿Problemas? Usa /support"
    ),

    # ── Profile ───────────────────────────────────────────────────────────
    "profile": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👤 <b>MI PERFIL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🪪 <b>ID Usuario:</b>      <code>{user_id}</code>\n"
        "📅 <b>Miembro desde:</b>  {join_date}\n"
        "🏅 <b>Insignia:</b>       {badge}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>Estadísticas</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 <b>Pedidos:</b>        {total_orders}\n"
        "🔗 <b>Links Comprados:</b> {links_bought}\n"
        "💰 <b>Total Gastado:</b>  <code>${total_spent}</code>\n"
        "🎁 <b>Ganancias Ref.:</b> <code>${referral_earnings}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 <b>Logros</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{achievements}\n\n"
        "🔔 <b>Notificaciones:</b>  {notifications}"
    ),
    "btn_toggle_notifications": "🔔  Notificaciones",
    "btn_change_language": "🌐  Idioma",

    # ── Orders ────────────────────────────────────────────────────────────
    "orders_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 <b>HISTORIAL DE PEDIDOS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Tienes <b>{count}</b> pedido(s).\n\n"
    ),
    "order_item": (
        "🆔 <code>{order_id}</code>\n"
        "📅 {date}  •  🔢 {qty}×  •  💰 ${amount}\n"
        "─────────────────────────\n"
    ),
    "no_orders": "📭 Aún no has realizado compras.\n\n¡Ve a 🛍️ Tienda para comenzar!",
    "btn_search_order": "🔍  Buscar Pedido",

    # ── Referral ──────────────────────────────────────────────────────────
    "referral_dashboard": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>REFERIR & GANAR</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💸 ¡Gana <b>${reward}</b> por cada amigo que haga su primera compra!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>Tus Stats</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 <b>Total Invitados:</b>    {total_invited}\n"
        "✅ <b>Exitosos:</b>           {successful}\n"
        "⏳ <b>Pendientes:</b>         {pending}\n"
        "💰 <b>Total Ganado:</b>       <code>${total_earnings}</code>\n"
        "💵 <b>Balance Disponible:</b> <code>${available_balance}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>Tu Enlace de Invitación:</b>\n"
        "<code>{referral_link}</code>\n\n"
        "<i>⚡ Las recompensas se acreditan solo tras la primera compra de tu amigo.</i>"
    ),
    "btn_copy_link": "📋  Copiar Enlace",
    "btn_withdraw": "💸  Retirar Ganancias",

    # ── Leaderboard ───────────────────────────────────────────────────────
    "leaderboard_weekly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 <b>TOP COMPRADORES SEMANALES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Actualizado: {updated}"
    ),
    "leaderboard_monthly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📅 <b>TOP COMPRADORES MENSUALES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Actualizado: {updated}"
    ),
    "leaderboard_alltime": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>TOP COMPRADORES DE TODOS LOS TIEMPOS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Actualizado: {updated}"
    ),
    "leaderboard_entry": "{rank}  {username}   🔗 {links} enlaces",
    "btn_weekly": "📅  Semanal",
    "btn_monthly": "🗓️  Mensual",
    "btn_alltime": "👑  Todo el Tiempo",

    # ── Reviews ───────────────────────────────────────────────────────────
    "reviews_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⭐ <b>RESEÑAS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Promedio: <b>{avg_rating}</b>/5  ({count} reseñas)\n\n"
        "{reviews}"
    ),
    "review_item": "⭐ {stars}  •  {username}\n<i>{comment}</i>\n─────────────────\n",
    "leave_review_prompt": "⭐ <b>Dejar una Reseña</b>\n\nCalifica tu compra del 1 al 5:",
    "btn_leave_review": "⭐  Dejar Reseña",
    "review_saved": "✅ ¡Gracias por tu reseña!",

    # ── Support ───────────────────────────────────────────────────────────
    "support": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 <b>SOPORTE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "¿Necesitas ayuda? Estamos aquí.\n\n"
        "📋 <b>¿Problema con pedido?</b>  Usa /search para encontrarlo.\n"
        "💬 <b>Soporte en vivo:</b> Contacta a un admin en el grupo.\n\n"
        "<i>Por favor incluye tu ID de Pedido al contactar soporte.</i>"
    ),

    # ── Maintenance ───────────────────────────────────────────────────────
    "maintenance": (
        "🔧 <b>Modo Mantenimiento</b>\n\n"
        "Estamos actualizando el bot.\n"
        "Por favor vuelve pronto.\n\n"
        "<i>Disculpa las molestias.</i>"
    ),

    # ── Notifications ─────────────────────────────────────────────────────
    "notifications_menu": (
        "🔔 <b>Configuración de Notificaciones</b>\n\n"
        "Activa o desactiva las notificaciones:"
    ),
    "notif_stock": "📦 Alertas de Stock",
    "notif_announcements": "📢 Anuncios",
    "notif_discounts": "🏷️ Alertas de Descuentos",

    # ── Admin ─────────────────────────────────────────────────────────────
    "admin_panel": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ <b>PANEL ADMIN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👥 <b>Usuarios:</b>       {total_users}\n"
        "📦 <b>Pedidos:</b>        {total_orders}\n"
        "💰 <b>Ingresos:</b>       <code>${total_revenue}</code>\n"
        "📈 <b>Hoy:</b>            <code>${today_revenue}</code>\n"
        "🔗 <b>Links Vendidos:</b> {links_sold}\n"
        "📊 <b>Stock:</b>          {stock} restantes\n\n"
        "Elige una acción 👇"
    ),
    "btn_upload_stock": "📤  Subir Stock",
    "btn_set_price": "💲  Fijar Precio",
    "btn_broadcast": "📢  Difundir",
    "btn_ban_user": "🚫  Banear Usuario",
    "btn_unban_user": "✅  Desbanear Usuario",
    "btn_view_users": "👥  Ver Usuarios",
    "btn_view_sales": "📊  Ver Ventas",
    "btn_maintenance": "🔧  Mantenimiento",
    "btn_referral_settings": "🎁  Config. Referidos",

    # ── Misc ──────────────────────────────────────────────────────────────
    "error_generic": "❌ Algo salió mal. Por favor intenta nuevamente.",
    "banned": "🚫 Has sido baneado de este bot.",
    "custom_qty_prompt": "✏️ Ingresa la cantidad que deseas comprar (1–100):",
    "invalid_qty": "❌ Cantidad inválida. Ingresa un número entre 1 y 100.",
    "insufficient_stock": "❌ Stock insuficiente. Solo hay {stock} enlace(s) disponibles.",
    "language_menu": "🌐 <b>Seleccionar Idioma</b>",
    "btn_lang_en": "🇬🇧 English",
    "btn_lang_es": "🇪🇸 Español",
    "search_prompt": "🔍 Ingresa tu ID de Pedido para buscar:",
    "order_not_found": "❌ Pedido <code>{order_id}</code> no encontrado.",
    "upload_stock_prompt": "📤 Envía un archivo .txt con un enlace por línea.",
    "stock_uploaded": "✅ <b>{count}</b> nuevos links cargados.\n📊 Stock total: <b>{total}</b>",
    "price_set": "✅ Precio actualizado a <code>${price}</code> por link.",
    "broadcast_prompt": "📢 Escribe tu mensaje de difusión:",
    "broadcast_sent": "✅ Difusión enviada a <b>{count}</b> usuarios.",
    "ban_prompt": "🚫 Ingresa el ID de usuario a banear:",
    "ban_success": "✅ Usuario <code>{user_id}</code> ha sido baneado.",
    "unban_prompt": "✅ Ingresa el ID de usuario a desbanear:",
    "unban_success": "✅ Usuario <code>{user_id}</code> ha sido desbaneado.",
    "maintenance_on": "🔧 Modo mantenimiento <b>activado</b>.",
    "maintenance_off": "✅ Modo mantenimiento <b>desactivado</b>.",
    "achievement_unlocked": "🏆 <b>¡Logro Desbloqueado!</b>\n\n{label}",
    "new_badge": "🎖️ <b>¡Nueva Insignia!</b>\n\nHas ganado: {badge}",
    "set_price_prompt": "💲 Ingresa el nuevo precio por link (USD):",
    "purchase_log": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛒 <b>NUEVA COMPRA</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>Usuario:</b>  @{username} (<code>{user_id}</code>)\n"
        "🆔 <b>ID Pedido:</b> <code>{order_id}</code>\n"
        "🔢 <b>Cantidad:</b>  {qty}× enlace(s)\n"
        "💰 <b>Monto:</b>     <code>${amount}</code>\n"
        "💱 <b>Método:</b>    {method}\n"
        "📅 <b>Fecha:</b>     {date}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
    "low_stock_alert": (
        "⚠️ <b>ALERTA: STOCK BAJO</b>\n\n"
        "¡Solo quedan <b>{stock}</b> links!\n"
        "Por favor sube más stock."
    ),
}
