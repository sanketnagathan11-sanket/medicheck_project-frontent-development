import re
c = open('MediCheck.html', encoding='utf-8').read()
script = re.search(r'<script>(.*?)</script>', c, re.DOTALL).group(1)
open('error_snippet.txt', 'w', encoding='utf-8').write(script[17000:17500])
