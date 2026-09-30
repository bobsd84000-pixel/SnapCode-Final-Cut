import base64,re,os
os.chdir(os.path.dirname(os.path.abspath(__file__))+"/..")
d="work/chat-images/"
b=lambda p:"data:image/jpeg;base64,"+base64.b64encode(open(d+p,"rb").read()).decode()
h=open("work/tpl.html").read().replace("__BR__",b("bracelet.jpg")).replace("__BG__",b("bague.jpg"))
open("bijoux-video.html","w").write(h)
h=re.sub(r'<!DOCTYPE html>\s*<html[^>]*><head>','',h)
h=h.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n','').replace('</head><body>','').replace('</body></html>','')
h=h.replace(':root{--fond',':root{color-scheme:dark;--fond',1).replace('html,body{height:100%;background:#000;overflow:hidden}','html,body{height:100%;background:#000;color:#f6f1e8;overflow:hidden}:root{padding:0}')
open("bijoux-artifact.html","w").write(h)
