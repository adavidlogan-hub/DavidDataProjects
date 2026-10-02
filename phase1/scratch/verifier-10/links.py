import sys,re,html
t=sys.stdin.read()
for a in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',t,re.S):
  h=a.group(1)
  if re.search(r'\.(css|js)(\?|$)|wp-includes|#content|gmpg|xmlrpc|oembed',h): continue
  print(html.unescape(h),'|',html.unescape(re.sub(r'<[^>]+>','',a.group(2))).strip()[:110])
