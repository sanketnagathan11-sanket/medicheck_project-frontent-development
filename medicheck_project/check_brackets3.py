import re

c = open('MediCheck.html', encoding='utf-8').read()
script = re.search(r'<script>(.*?)</script>', c, re.DOTALL).group(1)

def check_brackets(text):
    stack = []
    in_string = False
    string_char = ''
    escape = False
    
    for i, char in enumerate(text):
        if not in_string:
            if char in ["'", '"', '`']:
                in_string = True
                string_char = char
            elif char in ['{', '[', '(']:
                stack.append((char, i))
            elif char in ['}', ']', ')']:
                if not stack:
                    return f"Unmatched {char} at index {i}:\n{text[max(0, i-50):i+50]}"
                top, _ = stack.pop()
                if (char == '}' and top != '{') or \
                   (char == ']' and top != '[') or \
                   (char == ')' and top != '('):
                    return f"Mismatched {char} at index {i}:\n{text[max(0, i-50):i+50]}"
        else:
            if escape:
                escape = False
            elif char == '\\':
                escape = True
            elif char == string_char:
                in_string = False

    if stack:
        idx = stack[-1][1]
        return f"Unclosed {stack[-1][0]} opened at index {idx}:\n{text[max(0, idx-100):idx+200]}"
    return "OK"

res = check_brackets(script)
with open('bracket_err.txt', 'w', encoding='utf-8') as f:
    f.write(res)
