import re,sys,subprocess
u=sys.argv[1]
h=subprocess.run(['python3','-m','txprecinct.cat',u],capture_output=True,text=True,cwd='/home/user/DavidDataProjects').stdout
for m in re.finditer(r'href="([^"]+)"[^>]*>(.*?)</a>',h,re.S):
    l,t=m.group(1),re.sub(r'<[^>]+>|\s+',' ',m.group(2)).strip()
    print(l,'|',t)
