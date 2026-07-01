import re

def wrap_with_blockquote(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    output = []
    i = 0
    in_strings = False
    
    # Keys that should NOT be wrapped
    exclude_keys = [
        "btn_", "status_", "order_item", "leaderboard_entry", "review_item", 
        "language_menu"
    ]
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith("STRINGS = {"):
            in_strings = True
            output.append(line)
            i += 1
            continue
            
        if in_strings and line.startswith("}"):
            in_strings = False
            output.append(line)
            i += 1
            continue
            
        if in_strings:
            match = re.match(r'^[ \t]*"([^"]+)":\s*(.*)', line)
            if match:
                key = match.group(1)
                rest = match.group(2)
                
                exclude = any(key.startswith(exc) for exc in exclude_keys)
                
                if not exclude:
                    # Inject blockquote
                    if rest.startswith("("):
                        output.append(line)
                        output.append('        "<blockquote>\\n"\n')
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith("),"):
                            output.append(lines[i])
                            i += 1
                        output.append('        "</blockquote>"\n')
                        output.append(lines[i])
                        i += 1
                        continue
                    elif rest.startswith('f"') or rest.startswith('"'):
                        # single line string
                        # e.g. f"{E_CROSS} Something went wrong.",
                        content_match = re.search(r'([f]?["\'])(.*?)(["\'],?)', rest)
                        if content_match:
                            prefix = content_match.group(1)
                            content = content_match.group(2)
                            suffix = content_match.group(3)
                            
                            # Avoid double blockquote if already there
                            if "<blockquote>" not in content:
                                new_content = f"<blockquote>\\n{content}\\n</blockquote>"
                                new_rest = rest.replace(prefix + content + suffix, prefix + new_content + suffix)
                                line = line.replace(rest, new_rest)
                                
        # Also process buttons colors in this pass
        if in_strings and match:
            key = match.group(1)
            rest = match.group(2)
            if key.startswith("btn_"):
                # Apply color prefixes
                if any(x in key for x in ["cancel", "back", "decline", "main_menu", "ban_user"]):
                    color = "🔴"
                elif any(x in key for x in ["agree", "buy", "check_payment", "i_joined", "unban_user", "refresh_stock", "custom_qty"]):
                    color = "🟢"
                else:
                    color = "🔵"
                    
                content_match = re.search(r'([f]?["\'])(.*?)(["\'],?)', rest)
                if content_match:
                    prefix = content_match.group(1)
                    content = content_match.group(2)
                    suffix = content_match.group(3)
                    
                    if not content.startswith(color):
                        # Add color, preserve emoji
                        # Find first emoji or character
                        parts = content.split(" ", 1)
                        if len(parts) > 1 and len(parts[0]) <= 2: # heuristic for emoji
                            new_content = f"{color} {content}"
                        else:
                            new_content = f"{color} {content}"
                        
                        # Just append color at the beginning
                        new_content = f"{color} {content}"
                        # clean up if we accidentally doubled
                        new_content = new_content.replace(f"{color} {color}", color)
                        
                        new_rest = rest.replace(prefix + content + suffix, prefix + new_content + suffix)
                        line = line.replace(rest, new_rest)
        
        output.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(output)

wrap_with_blockquote('locales/en.py')
wrap_with_blockquote('locales/es.py')

print("Done wrapping blockquotes and adding buttons.")
