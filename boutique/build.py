import base64,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d="../brag-output/work/chat-images/"
b=lambda p:"data:image/jpeg;base64,"+base64.b64encode(open(d+p,"rb").read()).decode()
gal=["main-draps","perle","etoile","henne","couronne","mer","coeur","noirblanc","bague-orange","marche","kaftan","vert","ongles"]
g="\n        ".join('<figure><img src="%s" alt="Bijou porté, photo d\'ambiance" loading="lazy"></figure>'%b(x+".jpg") for x in gal)
h=open("tpl.html").read().replace("__BRACELET__",b("bracelet.jpg")).replace("__BAGUE__",b("bague-nette.jpg")).replace("__GALERIE__",g)
open("shop-bijoux.html","w").write(h);print(len(h))
