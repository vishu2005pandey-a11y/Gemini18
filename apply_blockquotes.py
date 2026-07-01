import re

keys_to_wrap = [
    "force_join_not_member", "out_of_stock", "payment_pending", 
    "payment_expired", "payment_cancelled", "no_orders", 
    "leave_review_prompt", "review_saved", "maintenance", 
    "notifications_menu", "error_generic", "banned", 
    "custom_qty_prompt", "invalid_qty", "insufficient_stock", 
    "language_menu", "search_prompt", "order_not_found", 
    "upload_stock_prompt", "stock_uploaded", "price_set", 
    "broadcast_prompt", "broadcast_sent", "ban_prompt", 
    "ban_success", "unban_prompt", "unban_success", 
    "maintenance_on", "maintenance_off", "set_price_prompt", 
    "achievement_unlocked", "new_badge"
]

def wrap_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for key in keys_to_wrap:
        # We need to find: `    "key": (` or `    "key": f"` or `    "key": "`
        # And inject blockquotes.
        # It's easier to find the key line, and replace the content.
        
        # Pattern to match the key and its value
        # The value can be a string `f"..."` or a tuple of strings `(\n ... \n)`
        
        # Let's match `"key": f"..."` or `"key": "..."`
        pattern1 = r'([ \t]*"' + key + r'":\s*)(f?["\'])(.*?)(["\'],)'
        
        # Let's match `"key": (\n ... \n    ),`
        pattern2 = r'([ \t]*"' + key + r'": \(\n)(.*?)(\n[ \t]*\),)'
        
        # Also need to handle cases where there is no trailing comma, or single line tuple.
        
        # Let's just use a simpler approach. I will manually prepare the regexes or use Python to parse the file line by line.
        pass

# Since I know the exact lines, I'll just use the script to replace them exactly.
replacements_en = {
    '    "force_join_not_member": (\n        f"{E_WARNING} <b>Access Denied</b>\\n\\n"\n        "You haven\'t joined our channel and group yet.\\n"\n        "Please join both and try again."\n    ),': '    "force_join_not_member": (\n        "<blockquote>\\n"\n        f"{E_WARNING} <b>Access Denied</b>\\n\\n"\n        "You haven\'t joined our channel and group yet.\\n"\n        "Please join both and try again.\\n"\n        "</blockquote>"\n    ),',
    
    '    "out_of_stock": (\n        f"{E_CROSS} <b>Out of Stock</b>\\n\\n"\n        "We\'re restocking soon. Enable stock alerts in your profile!"\n    ),': '    "out_of_stock": (\n        "<blockquote>\\n"\n        f"{E_CROSS} <b>Out of Stock</b>\\n\\n"\n        "We\'re restocking soon. Enable stock alerts in your profile!\\n"\n        "</blockquote>"\n    ),',
    
    '    "payment_pending":    f"{E_CLOCK} Payment not confirmed yet. Please send exact amount and check again.",': '    "payment_pending":    f"<blockquote>\\n{E_CLOCK} Payment not confirmed yet. Please send exact amount and check again.\\n</blockquote>",',
    
    '    "payment_expired":    f"{E_CLOCK} <b>Payment Expired</b>\\n\\nYour invoice has expired. Please place a new order.",': '    "payment_expired":    f"<blockquote>\\n{E_CLOCK} <b>Payment Expired</b>\\n\\nYour invoice has expired. Please place a new order.\\n</blockquote>",',
    
    '    "payment_cancelled":  f"{E_CROSS} Order cancelled.",': '    "payment_cancelled":  f"<blockquote>\\n{E_CROSS} Order cancelled.\\n</blockquote>",',
    
    '    "no_orders": (\n        f"{E_PACKAGE} You haven\'t made any purchases yet.\\n\\n"\n        f"Head to {E_CART} Shop to get started!"\n    ),': '    "no_orders": (\n        "<blockquote>\\n"\n        f"{E_PACKAGE} You haven\'t made any purchases yet.\\n\\n"\n        f"Head to {E_CART} Shop to get started!\\n"\n        "</blockquote>"\n    ),',
    
    '    "leave_review_prompt": f"{E_STAR} <b>Leave a Review</b>\\n\\nRate your purchase from 1 to 5 stars:",': '    "leave_review_prompt": f"<blockquote>\\n{E_STAR} <b>Leave a Review</b>\\n\\nRate your purchase from 1 to 5 stars:\\n</blockquote>",',
    
    '    "review_saved":       f"{E_CHECK} Thank you for your review!",': '    "review_saved":       f"<blockquote>\\n{E_CHECK} Thank you for your review!\\n</blockquote>",',
    
    '    "maintenance": (\n        f"{E_WARNING} <b>Maintenance Mode</b>\\n\\n"\n        "We\'re currently updating the bot.\\n"\n        f"Please check back shortly. {E_CLOCK}\\n\\n"\n        "<i>We apologize for the inconvenience.</i>"\n    ),': '    "maintenance": (\n        "<blockquote>\\n"\n        f"{E_WARNING} <b>Maintenance Mode</b>\\n\\n"\n        "We\'re currently updating the bot.\\n"\n        f"Please check back shortly. {E_CLOCK}\\n\\n"\n        "<i>We apologize for the inconvenience.</i>\\n"\n        "</blockquote>"\n    ),',
    
    '    "notifications_menu": (\n        f"{E_BELL} <b>Notification Settings</b>\\n\\n"\n        "Toggle notifications below:"\n    ),': '    "notifications_menu": (\n        "<blockquote>\\n"\n        f"{E_BELL} <b>Notification Settings</b>\\n\\n"\n        "Toggle notifications below:\\n"\n        "</blockquote>"\n    ),',
    
    '    "achievement_unlocked": f"{E_TROPHY} <b>Achievement Unlocked!</b>\\n\\n{{label}}",': '    "achievement_unlocked": f"<blockquote>\\n{E_TROPHY} <b>Achievement Unlocked!</b>\\n\\n{{label}}\\n</blockquote>",',
    
    '    "new_badge":            f"{E_MEDAL} <b>New Badge!</b>\\n\\nYou\'ve earned: {{badge}}",': '    "new_badge":            f"<blockquote>\\n{E_MEDAL} <b>New Badge!</b>\\n\\nYou\'ve earned: {{badge}}\\n</blockquote>",',
    
    '    "error_generic":       f"{E_CROSS} Something went wrong. Please try again.",': '    "error_generic":       f"<blockquote>\\n{E_CROSS} Something went wrong. Please try again.\\n</blockquote>",',
    
    '    "banned":              "🚫 You have been banned from using this bot.",': '    "banned":              "<blockquote>\\n🚫 You have been banned from using this bot.\\n</blockquote>",',
    
    '    "custom_qty_prompt":   "✏️ Enter the quantity you want to buy (1–100):",': '    "custom_qty_prompt":   "<blockquote>\\n✏️ Enter the quantity you want to buy (1–100):\\n</blockquote>",',
    
    '    "invalid_qty":         f"{E_CROSS} Invalid quantity. Please enter a number between 1 and 100.",': '    "invalid_qty":         f"<blockquote>\\n{E_CROSS} Invalid quantity. Please enter a number between 1 and 100.\\n</blockquote>",',
    
    '    "insufficient_stock":  f"{E_CROSS} Not enough stock. Only {{stock}} link(s) available.",': '    "insufficient_stock":  f"<blockquote>\\n{E_CROSS} Not enough stock. Only {{stock}} link(s) available.\\n</blockquote>",',
    
    '    "language_menu":       "🌐 <b>Select Language</b>",': '    "language_menu":       "<blockquote>\\n🌐 <b>Select Language</b>\\n</blockquote>",',
    
    '    "search_prompt":       "🔍 Enter your Order ID to search:",': '    "search_prompt":       "<blockquote>\\n🔍 Enter your Order ID to search:\\n</blockquote>",',
    
    '    "order_not_found":     f"{E_CROSS} Order <code>{{order_id}}</code> not found.",': '    "order_not_found":     f"<blockquote>\\n{E_CROSS} Order <code>{{order_id}}</code> not found.\\n</blockquote>",',
    
    '    "upload_stock_prompt": f"{E_PACKAGE} Send a .txt file with one redemption link per line.",': '    "upload_stock_prompt": f"<blockquote>\\n{E_PACKAGE} Send a .txt file with one redemption link per line.\\n</blockquote>",',
    
    '    "stock_uploaded":      f"{E_CHECK} Uploaded <b>{{count}}</b> new links.\\n{E_CHART} Total stock: <b>{{total}}</b>",': '    "stock_uploaded":      f"<blockquote>\\n{E_CHECK} Uploaded <b>{{count}}</b> new links.\\n{E_CHART} Total stock: <b>{{total}}</b>\\n</blockquote>",',
    
    '    "price_set":           f"{E_CHECK} Price updated to <code>${{price}}</code> per link.",': '    "price_set":           f"<blockquote>\\n{E_CHECK} Price updated to <code>${{price}}</code> per link.\\n</blockquote>",',
    
    '    "broadcast_prompt":    "📢 Type your broadcast message:",': '    "broadcast_prompt":    "<blockquote>\\n📢 Type your broadcast message:\\n</blockquote>",',
    
    '    "broadcast_sent":      f"{E_CHECK} Broadcast sent to <b>{{count}}</b> users.",': '    "broadcast_sent":      f"<blockquote>\\n{E_CHECK} Broadcast sent to <b>{{count}}</b> users.\\n</blockquote>",',
    
    '    "ban_prompt":          "🚫 Enter the User ID to ban:",': '    "ban_prompt":          "<blockquote>\\n🚫 Enter the User ID to ban:\\n</blockquote>",',
    
    '    "ban_success":         f"{E_CHECK} User <code>{{user_id}}</code> has been banned.",': '    "ban_success":         f"<blockquote>\\n{E_CHECK} User <code>{{user_id}}</code> has been banned.\\n</blockquote>",',
    
    '    "unban_prompt":        "✅ Enter the User ID to unban:",': '    "unban_prompt":        "<blockquote>\\n✅ Enter the User ID to unban:\\n</blockquote>",',
    
    '    "unban_success":       f"{E_CHECK} User <code>{{user_id}}</code> has been unbanned.",': '    "unban_success":       f"<blockquote>\\n{E_CHECK} User <code>{{user_id}}</code> has been unbanned.\\n</blockquote>",',
    
    '    "maintenance_on":      f"🔧 Maintenance mode <b>enabled</b>.",': '    "maintenance_on":      f"<blockquote>\\n🔧 Maintenance mode <b>enabled</b>.\\n</blockquote>",',
    
    '    "maintenance_off":     f"{E_CHECK} Maintenance mode <b>disabled</b>.",': '    "maintenance_off":     f"<blockquote>\\n{E_CHECK} Maintenance mode <b>disabled</b>.\\n</blockquote>",',
    
    '    "set_price_prompt":    f"{E_MONEY} Enter new price per link (USD):",': '    "set_price_prompt":    f"<blockquote>\\n{E_MONEY} Enter new price per link (USD):\\n</blockquote>",',
}

replacements_es = {
    '    "force_join_not_member": (\n        f"{E_WARNING} <b>Acceso Denegado</b>\\n\\n"\n        "Aún no te has unido a nuestro canal y grupo.\\n"\n        "Por favor únete a ambos e intenta nuevamente."\n    ),': '    "force_join_not_member": (\n        "<blockquote>\\n"\n        f"{E_WARNING} <b>Acceso Denegado</b>\\n\\n"\n        "Aún no te has unido a nuestro canal y grupo.\\n"\n        "Por favor únete a ambos e intenta nuevamente.\\n"\n        "</blockquote>"\n    ),',
    
    '    "out_of_stock": (\n        f"{E_CROSS} <b>Sin Stock</b>\\n\\n"\n        "¡Pronto habrá reposición! Activa alertas de stock en tu perfil."\n    ),': '    "out_of_stock": (\n        "<blockquote>\\n"\n        f"{E_CROSS} <b>Sin Stock</b>\\n\\n"\n        "¡Pronto habrá reposición! Activa alertas de stock en tu perfil.\\n"\n        "</blockquote>"\n    ),',
    
    '    "payment_pending":    f"{E_CLOCK} Pago aún no confirmado. Envía el monto exacto e intenta nuevamente.",': '    "payment_pending":    f"<blockquote>\\n{E_CLOCK} Pago aún no confirmado. Envía el monto exacto e intenta nuevamente.\\n</blockquote>",',
    
    '    "payment_expired":    f"{E_CLOCK} <b>Pago Expirado</b>\\n\\nTu factura ha expirado. Por favor realiza un nuevo pedido.",': '    "payment_expired":    f"<blockquote>\\n{E_CLOCK} <b>Pago Expirado</b>\\n\\nTu factura ha expirado. Por favor realiza un nuevo pedido.\\n</blockquote>",',
    
    '    "payment_cancelled":  f"{E_CROSS} Pedido cancelado.",': '    "payment_cancelled":  f"<blockquote>\\n{E_CROSS} Pedido cancelado.\\n</blockquote>",',
    
    '    "no_orders": (\n        f"{E_PACKAGE} Aún no has realizado compras.\\n\\n"\n        f"¡Ve a {E_CART} Tienda para comenzar!"\n    ),': '    "no_orders": (\n        "<blockquote>\\n"\n        f"{E_PACKAGE} Aún no has realizado compras.\\n\\n"\n        f"¡Ve a {E_CART} Tienda para comenzar!\\n"\n        "</blockquote>"\n    ),',
    
    '    "leave_review_prompt": f"{E_STAR} <b>Dejar una Reseña</b>\\n\\nCalifica tu compra del 1 al 5:",': '    "leave_review_prompt": f"<blockquote>\\n{E_STAR} <b>Dejar una Reseña</b>\\n\\nCalifica tu compra del 1 al 5:\\n</blockquote>",',
    
    '    "review_saved":       f"{E_CHECK} ¡Gracias por tu reseña!",': '    "review_saved":       f"<blockquote>\\n{E_CHECK} ¡Gracias por tu reseña!\\n</blockquote>",',
    
    '    "maintenance": (\n        f"{E_WARNING} <b>Modo Mantenimiento</b>\\n\\n"\n        "Estamos actualizando el bot.\\n"\n        f"Por favor vuelve pronto. {E_CLOCK}\\n\\n"\n        "<i>Disculpa las molestias.</i>"\n    ),': '    "maintenance": (\n        "<blockquote>\\n"\n        f"{E_WARNING} <b>Modo Mantenimiento</b>\\n\\n"\n        "Estamos actualizando el bot.\\n"\n        f"Por favor vuelve pronto. {E_CLOCK}\\n\\n"\n        "<i>Disculpa las molestias.</i>\\n"\n        "</blockquote>"\n    ),',
    
    '    "notifications_menu":  f"{E_BELL} <b>Configuración de Notificaciones</b>\\n\\nActiva o desactiva:",': '    "notifications_menu":  f"<blockquote>\\n{E_BELL} <b>Configuración de Notificaciones</b>\\n\\nActiva o desactiva:\\n</blockquote>",',
    
    '    "achievement_unlocked": f"{E_TROPHY} <b>¡Logro Desbloqueado!</b>\\n\\n{{label}}",': '    "achievement_unlocked": f"<blockquote>\\n{E_TROPHY} <b>¡Logro Desbloqueado!</b>\\n\\n{{label}}\\n</blockquote>",',
    
    '    "new_badge":          f"{E_MEDAL} <b>¡Nueva Insignia!</b>\\n\\nHas ganado: {{badge}}",': '    "new_badge":          f"<blockquote>\\n{E_MEDAL} <b>¡Nueva Insignia!</b>\\n\\nHas ganado: {{badge}}\\n</blockquote>",',
    
    '    "error_generic":      f"{E_CROSS} Algo salió mal. Por favor intenta nuevamente.",': '    "error_generic":      f"<blockquote>\\n{E_CROSS} Algo salió mal. Por favor intenta nuevamente.\\n</blockquote>",',
    
    '    "banned":             "🚫 Has sido baneado de este bot.",': '    "banned":             "<blockquote>\\n🚫 Has sido baneado de este bot.\\n</blockquote>",',
    
    '    "custom_qty_prompt":  "✏️ Ingresa la cantidad que deseas comprar (1–100):",': '    "custom_qty_prompt":  "<blockquote>\\n✏️ Ingresa la cantidad que deseas comprar (1–100):\\n</blockquote>",',
    
    '    "invalid_qty":        f"{E_CROSS} Cantidad inválida. Ingresa un número entre 1 y 100.",': '    "invalid_qty":        f"<blockquote>\\n{E_CROSS} Cantidad inválida. Ingresa un número entre 1 y 100.\\n</blockquote>",',
    
    '    "insufficient_stock": f"{E_CROSS} Stock insuficiente. Solo hay {{stock}} enlace(s) disponibles.",': '    "insufficient_stock": f"<blockquote>\\n{E_CROSS} Stock insuficiente. Solo hay {{stock}} enlace(s) disponibles.\\n</blockquote>",',
    
    '    "language_menu":      "🌐 <b>Seleccionar Idioma</b>",': '    "language_menu":      "<blockquote>\\n🌐 <b>Seleccionar Idioma</b>\\n</blockquote>",',
    
    '    "search_prompt":      "🔍 Ingresa tu ID de Pedido para buscar:",': '    "search_prompt":      "<blockquote>\\n🔍 Ingresa tu ID de Pedido para buscar:\\n</blockquote>",',
    
    '    "order_not_found":    f"{E_CROSS} Pedido <code>{{order_id}}</code> no encontrado.",': '    "order_not_found":    f"<blockquote>\\n{E_CROSS} Pedido <code>{{order_id}}</code> no encontrado.\\n</blockquote>",',
    
    '    "upload_stock_prompt":f"{E_PACKAGE} Envía un archivo .txt con un enlace por línea.",': '    "upload_stock_prompt":f"<blockquote>\\n{E_PACKAGE} Envía un archivo .txt con un enlace por línea.\\n</blockquote>",',
    
    '    "stock_uploaded":     f"{E_CHECK} <b>{{count}}</b> nuevos links cargados.\\n{E_CHART} Stock total: <b>{{total}}</b>",': '    "stock_uploaded":     f"<blockquote>\\n{E_CHECK} <b>{{count}}</b> nuevos links cargados.\\n{E_CHART} Stock total: <b>{{total}}</b>\\n</blockquote>",',
    
    '    "price_set":          f"{E_CHECK} Precio actualizado a <code>${{price}}</code> por link.",': '    "price_set":          f"<blockquote>\\n{E_CHECK} Precio actualizado a <code>${{price}}</code> por link.\\n</blockquote>",',
    
    '    "broadcast_prompt":   "📢 Escribe tu mensaje de difusión:",': '    "broadcast_prompt":   "<blockquote>\\n📢 Escribe tu mensaje de difusión:\\n</blockquote>",',
    
    '    "broadcast_sent":     f"{E_CHECK} Difusión enviada a <b>{{count}}</b> usuarios.",': '    "broadcast_sent":     f"<blockquote>\\n{E_CHECK} Difusión enviada a <b>{{count}}</b> usuarios.\\n</blockquote>",',
    
    '    "ban_prompt":         "🚫 Ingresa el ID de usuario a banear:",': '    "ban_prompt":         "<blockquote>\\n🚫 Ingresa el ID de usuario a banear:\\n</blockquote>",',
    
    '    "ban_success":        f"{E_CHECK} Usuario <code>{{user_id}}</code> ha sido baneado.",': '    "ban_success":        f"<blockquote>\\n{E_CHECK} Usuario <code>{{user_id}}</code> ha sido baneado.\\n</blockquote>",',
    
    '    "unban_prompt":       "✅ Ingresa el ID de usuario a desbanear:",': '    "unban_prompt":       "<blockquote>\\n✅ Ingresa el ID de usuario a desbanear:\\n</blockquote>",',
    
    '    "unban_success":      f"{E_CHECK} Usuario <code>{{user_id}}</code> ha sido desbaneado.",': '    "unban_success":      f"<blockquote>\\n{E_CHECK} Usuario <code>{{user_id}}</code> ha sido desbaneado.\\n</blockquote>",',
    
    '    "maintenance_on":     f"🔧 Modo mantenimiento <b>activado</b>.",': '    "maintenance_on":     f"<blockquote>\\n🔧 Modo mantenimiento <b>activado</b>.\\n</blockquote>",',
    
    '    "maintenance_off":    f"{E_CHECK} Modo mantenimiento <b>desactivado</b>.",': '    "maintenance_off":    f"<blockquote>\\n{E_CHECK} Modo mantenimiento <b>desactivado</b>.\\n</blockquote>",',
    
    '    "set_price_prompt":   f"{E_MONEY} Ingresa el nuevo precio por link (USD):",': '    "set_price_prompt":   f"<blockquote>\\n{E_MONEY} Ingresa el nuevo precio por link (USD):\\n</blockquote>",',
}

def apply_replacements(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: Could not find exactly:\n{old}")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
apply_replacements('locales/en.py', replacements_en)
apply_replacements('locales/es.py', replacements_es)
print("Done.")
