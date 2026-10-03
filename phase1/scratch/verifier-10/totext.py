import sys,re,html
t=sys.stdin.read()
t=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S)
t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',lambda m:' [['+m.group(1)+']] ',t)
t=re.sub(r'<[^>]+>','\n',t); t=html.unescape(t)
print('\n'.join(l.strip() for l in t.split('\n') if l.strip()))
