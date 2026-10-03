import sys, re, subprocess, html
url=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else ''
body=subprocess.run([sys.executable,'-m','txprecinct.cat',url],capture_output=True,text=True,cwd='/home/user/DavidDataProjects').stdout
for m in re.finditer(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>',body,re.S|re.I):
    t=html.unescape(re.sub(r'<[^>]+>','',m.group(2))).strip()
    t=re.sub(r'\s+',' ',t)
    if re.search(pat,m.group(1)+' '+t,re.I): print(m.group(1),'|',t)
