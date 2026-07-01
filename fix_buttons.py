import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply button colors
    # 🔴 Red
    for k in ["btn_cancel_payment", "btn_back", "btn_decline", "btn_main_menu", "btn_ban_user"]:
        content = re.sub(r'("' + k + r'":\s*["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 ' + m.group(2).replace('🔴 ', '').replace('❌', '').replace('◀️', '').replace('🏠', '').replace('🚫', '').strip() + m.group(3), content)
    
    # 🟢 Green
    for k in ["btn_agree", "btn_check_payment", "btn_i_joined", "btn_buy_1", "btn_buy_3", "btn_buy_5", "btn_buy_10", "btn_custom_qty", "btn_unban_user", "btn_refresh_stock"]:
        content = re.sub(r'("' + k + r'":\s*["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 ' + m.group(2).replace('🟢 ', '').replace('✅', '').replace('🔄', '').strip() + m.group(3), content)
        
    # 🔵 Blue
    for k in [
        "btn_shop", "btn_profile", "btn_orders", "btn_referral", "btn_support", "btn_leaderboard", 
        "btn_reviews", "btn_join_channel", "btn_join_group", "btn_toggle_notifications", 
        "btn_change_language", "btn_search_order", "btn_copy_link", "btn_withdraw", 
        "btn_weekly", "btn_monthly", "btn_alltime", "btn_leave_review", "btn_upload_stock", 
        "btn_set_price", "btn_broadcast", "btn_view_users", "btn_view_sales", "btn_maintenance", 
        "btn_referral_settings", "btn_lang_en", "btn_lang_es"
    ]:
        content = re.sub(r'("' + k + r'":\s*["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔵 ' + m.group(2).replace('🔵 ', '').strip() + m.group(3), content)

    # Now for blockquotes. We want to wrap ALL string values (except keys starting with btn_ or status_ or leaderboard_entry or review_item or order_item)
    # The safest way is to parse the python AST, find the STRINGS dict, and rewrite the strings.
    # But doing so destroys formatting.
    # We can do this: Look for all keys in STRINGS:
    pass

import ast

def apply_blockquotes_safe(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process buttons first
    content = re.sub(r'("btn_cancel_payment":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 ❌ Cancel Order' + m.group(3), content)
    content = re.sub(r'("btn_back":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 ◀️ Back' + m.group(3), content)
    content = re.sub(r'("btn_decline":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 ❌ Decline' + m.group(3), content)
    content = re.sub(r'("btn_main_menu":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 🏠 Main Menu' + m.group(3), content)
    content = re.sub(r'("btn_ban_user":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🔴 🚫 Ban User' + m.group(3), content)

    content = re.sub(r'("btn_agree":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 ✅ Agree & Continue' + m.group(3), content)
    content = re.sub(r'("btn_check_payment":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🔄 Check Payment' + m.group(3), content)
    content = re.sub(r'("btn_i_joined":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 ✅ I Joined' + m.group(3), content)
    content = re.sub(r'("btn_unban_user":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 ✅ Unban User' + m.group(3), content)
    content = re.sub(r'("btn_refresh_stock":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🔄 Refresh Stock' + m.group(3), content)
    
    content = re.sub(r'("btn_buy_1":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🛍️ 1x Link' + m.group(3), content)
    content = re.sub(r'("btn_buy_3":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🛍️ 3x Links' + m.group(3), content)
    content = re.sub(r'("btn_buy_5":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🛍️ 5x Links' + m.group(3), content)
    content = re.sub(r'("btn_buy_10":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 🛍️ 10x Links' + m.group(3), content)
    content = re.sub(r'("btn_custom_qty":\s*f?["\'])(.*?)(["\'])', lambda m: m.group(1) + '🟢 ✏️ Custom Qty' + m.group(3), content)

    # We just write a simple script that modifies the file line by line for blockquotes!
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

apply_blockquotes_safe('locales/en.py')
apply_blockquotes_safe('locales/es.py')

print("Applied buttons.")
