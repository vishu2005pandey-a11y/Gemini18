import re

def remove_circles(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the circles
    content = content.replace('🔴 ', '')
    content = content.replace('🟢 ', '')
    content = content.replace('🔵 ', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

remove_circles('locales/en.py')
remove_circles('locales/es.py')

print("Removed circles.")
