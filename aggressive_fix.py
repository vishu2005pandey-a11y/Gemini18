import os

# Let's write a targeted script that will modify locales/en.py and locales/es.py

# Buttons to modify
button_modifications = {
    # 🔴 Red: Cancel, Back, Decline, Main Menu
    "btn_cancel_payment": lambda s: s.replace('❌', '🔴 ❌'),
    "btn_back": lambda s: s.replace('◀️', '🔴 ◀️'),
    "btn_decline": lambda s: s.replace('❌', '🔴 ❌'),
    "btn_main_menu": lambda s: s.replace('🏠', '🔴 🏠'),
    "btn_ban_user": lambda s: s.replace('🚫', '🔴 🚫'),

    # 🟢 Green: Agree, Buy, Check Payment, I Joined, etc
    "btn_agree": lambda s: s.replace('✅', '🟢 ✅'),
    "btn_check_payment": lambda s: s.replace('🔄', '🟢 🔄'),
    "btn_i_joined": lambda s: s.replace('✅', '🟢 ✅'),
    "btn_buy_1": lambda s: '🟢 🛍️ ' + s,
    "btn_buy_3": lambda s: '🟢 🛍️ ' + s,
    "btn_buy_5": lambda s: '🟢 🛍️ ' + s,
    "btn_buy_10": lambda s: '🟢 🛍️ ' + s,
    "btn_custom_qty": lambda s: '🟢 ' + s,
    "btn_unban_user": lambda s: s.replace('✅', '🟢 ✅'),
    "btn_refresh_stock": lambda s: '🟢 🔄' + s.split('🔄')[1] if '🔄' in s else '🟢 🔄 ' + s,

    # 🔵 Blue: Nav, Info, Menus, Profile, Support, etc
    "btn_shop": lambda s: s.replace('🛍️', '🔵 🛍️'),
    "btn_profile": lambda s: s.replace('👤', '🔵 👤'),
    "btn_orders": lambda s: s.replace('📦', '🔵 📦'),
    "btn_referral": lambda s: s.replace('🔗', '🔵 🔗'),
    "btn_support": lambda s: s.replace('🆘', '🔵 🆘'),
    "btn_leaderboard": lambda s: s.replace('🏆', '🔵 🏆'),
    "btn_reviews": lambda s: s.replace('⭐', '🔵 ⭐'),
    "btn_join_channel": lambda s: s.replace('📢', '🔵 📢'),
    "btn_join_group": lambda s: s.replace('💬', '🔵 💬'),
    "btn_toggle_notifications": lambda s: s.replace('🔔', '🔵 🔔'),
    "btn_change_language": lambda s: s.replace('🌐', '🔵 🌐'),
    "btn_search_order": lambda s: s.replace('🔍', '🔵 🔍'),
    "btn_copy_link": lambda s: s.replace('📋', '🔵 📋'),
    "btn_withdraw": lambda s: s.replace('💸', '🔵 💸'),
    "btn_weekly": lambda s: s.replace('📅', '🔵 📅'),
    "btn_monthly": lambda s: s.replace('🗓️', '🔵 🗓️'),
    "btn_alltime": lambda s: s.replace('👑', '🔵 👑'),
    "btn_leave_review": lambda s: s.replace('⭐', '🔵 ⭐'),
    "btn_upload_stock": lambda s: s.replace('📤', '🔵 📤'),
    "btn_set_price": lambda s: s.replace('💲', '🔵 💲'),
    "btn_broadcast": lambda s: s.replace('📢', '🔵 📢'),
    "btn_view_users": lambda s: s.replace('👥', '🔵 👥'),
    "btn_view_sales": lambda s: s.replace('📊', '🔵 📊'),
    "btn_maintenance": lambda s: s.replace('🔧', '🔵 🔧'),
    "btn_referral_settings": lambda s: s.replace('🎁', '🔵 🎁'),
    "btn_lang_en": lambda s: s.replace('🇬🇧', '🔵 🇬🇧'),
    "btn_lang_es": lambda s: s.replace('🇪🇸', '🔵 🇪🇸'),
}

# The blockquotes for large messages.
# I will do a regex replacement to inject <blockquote>\n after the first line and \n</blockquote> at the very end
keys_to_wrap = [
    "welcome", "shop_header", "shop_list_header", "product_card", "terms", 
    "payment_invoice", "delivery_success", "profile", "orders_header", 
    "referral_dashboard", "leaderboard_weekly", "leaderboard_monthly", 
    "leaderboard_alltime", "reviews_header", "support", "admin_panel", 
    "purchase_log", "low_stock_alert", "force_join_title"
]

import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_dict = False
    current_key = None
    output = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if we are inside STRINGS
        if line.startswith("STRINGS = {"):
            in_dict = True
            output.append(line)
            i += 1
            continue
            
        if in_dict and line.startswith("}"):
            in_dict = False
            output.append(line)
            i += 1
            continue
            
        if in_dict:
            # Check for keys
            match = re.match(r'^[ \t]*"([^"]+)":\s*(.*)', line)
            if match:
                key = match.group(1)
                rest = match.group(2)
                
                # Check button modifications
                if key in button_modifications:
                    # Usually "btn_key": "Emoji Text",
                    if rest.startswith('"') or rest.startswith("f\""):
                        # Extract string content
                        content_match = re.search(r'([f]?["\'])(.*?)(["\'],?)', rest)
                        if content_match:
                            prefix = content_match.group(1)
                            content = content_match.group(2)
                            suffix = content_match.group(3)
                            
                            new_content = button_modifications[key](content)
                            new_rest = rest.replace(prefix + content + suffix, prefix + new_content + suffix)
                            line = line.replace(rest, new_rest)
                            
                # Check blockquote wrapper
                if key in keys_to_wrap:
                    # We inject blockquote
                    # A multiline string looks like:
                    # "key": (
                    #    "line1\n"
                    #    "line2"
                    # ),
                    if rest.startswith("("):
                        output.append(line)
                        output.append('        "<blockquote>\\n"\n')
                        
                        i += 1
                        # Continue reading until the closing parenthesis
                        while i < len(lines) and not lines[i].strip().startswith("),"):
                            output.append(lines[i])
                            i += 1
                            
                        # Now lines[i] is `    ),`
                        output.append('        "</blockquote>"\n')
                        output.append(lines[i])
                        i += 1
                        continue
                        
        output.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(output)

process_file('locales/en.py')
process_file('locales/es.py')

print("Applied full fixes.")
