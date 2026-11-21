import re

script = open('script.js', encoding='utf-8').read()

# Remove comments
script = re.sub(r'//.*', '', script)
script = re.sub(r'/\*.*?\*/', '', script, flags=re.DOTALL)

# Remove strings
# crude regex for strings
script = re.sub(r'`[^`]*`', '""', script, flags=re.DOTALL)
script = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', script, flags=re.DOTALL)
script = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", script, flags=re.DOTALL)

# Now check braces
stack = []
for i, c in enumerate(script):
    if c in '{[(':
        stack.append(c)
    elif c in '}])':
        if not stack:
            print(f"Extra closing {c} at index {i}")
            break
        last = stack.pop()
        if (last == '{' and c != '}') or (last == '[' and c != ']') or (last == '(' and c != ')'):
            print(f"Mismatched {last} and {c} at index {i}")
            break
else:
    if stack:
        print(f"Unclosed {stack[-1]}")
    else:
        print("Braces match perfectly!")
