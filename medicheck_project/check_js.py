import re
import subprocess

c = open('MediCheck.html', encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)

with open('script.js', 'w', encoding='utf-8') as f:
    for s in scripts:
        f.write(s + '\n')

res = subprocess.run(['node', '-c', 'script.js'], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
