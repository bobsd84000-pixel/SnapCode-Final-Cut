import base64,re,os
os.chdir(os.path.dirname(os.path.abspath(__file__))+"/..")
d="work/chat-images/"
b=lambda p:"data:image/jpeg;base64,"+base64.b64encode(open(d+p,"rb").read()).decode()
h=open("work/tpl.html").read().replace("__BR__",b("bracelet.jpg")).replace("__BG__",b("bague.jpg")).replace("__DRAPS__",b("main-draps.jpg")).replace("__HENNE__",b("henne.jpg")).replace("__ORANGE__",b("bague-orange.jpg")).replace("__KAFTAN__",b("kaftan.jpg")).replace("__PERLE__",b("perle.jpg")).replace("__COEUR__",b("coeur.jpg")).replace("__COURONNE__",b("couronne.jpg")).replace("__ONGLES__",b("ongles.jpg")).replace("__ETOILE__",b("etoile.jpg")).replace("__MER__",b("mer.jpg")).replace("__NOIRBLANC__",b("noirblanc.jpg")).replace("__MARCHE__",b("marche.jpg")).replace("__VERT__",b("vert.jpg"))
open("bijoux-video.html","w").write(h)
h=re.sub(r'<!DOCTYPE html>\s*<html[^>]*><head>','',h)
h=h.replace('<meta charset="utf-8">\n','').replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n','').replace('</head><body>','').replace('</body></html>','')
h=h.replace(':root{--fond',':root{color-scheme:dark;--fond',1).replace('html,body{height:100%;background:#000;overflow:hidden}','html,body{height:100%;background:#000;color:#f6f1e8;overflow:hidden}:root{padding:0}')
open("bijoux-artifact.html","w").write(h)
