import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
s=re.sub(r'<a [^>]*href="([^"]*)"[^>]*>',r' [LINK:\1] ',s)
s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S|re.I)
t=html.unescape(re.sub(r'<[^>]+>',' ',s))
t=re.sub(r'[ \t\r]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w').write(t)
