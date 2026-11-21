import re

script = open('script.js', encoding='utf-8').read()
original_script = script

script = re.sub(r'//.*', '', script)
script = re.sub(r'/\*.*?\*/', '', script, flags=re.DOTALL)
script = re.sub(r'`[^`]*`', '""', script, flags=re.DOTALL)
script = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '""', script, flags=re.DOTALL)
script = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "''", script, flags=re.DOTALL)

stack = []
for i, c in enumerate(script):
    if c in '{[(':
        stack.append(c)
    elif c in '}])':
        if not stack:
            print(f"Extra closing {c} at index {i}")
            # print surrounding context from the stripped script
            context = script[max(0, i-50):i+50]
            print("CONTEXT:")
            print(context)
            break
        last = stack.pop()
