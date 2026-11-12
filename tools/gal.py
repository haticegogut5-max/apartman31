import sys,json,base64,io,struct;import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from proc import *
from bake import smooth
import numpy as np
from PIL import Image
P,I,col=get('textured_mesh')
j,bn=load('../assets/source_models/textured_mesh.glb')
def raw(i):
    bv=j['bufferViews'][j['images'][i]['bufferView']];return bn[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']]
pa=j['meshes'][0]['primitives'][0]['attributes']
N=acc(j,bn,pa['NORMAL']).astype(np.float64);UV=acc(j,bn,pa['TEXCOORD_0']).astype(np.float32)
x,y,z=P[:,0],P[:,1],P[:,2];n=len(P);hz=z[y>.8].mean()
cls=np.full(n,2)                        # 0 skin 1 hair 2 sweater 3 skirt 4 socks 5 shoes
cls[y<.045]=3;cls[y<-.60]=0;cls[y<-.745]=4;cls[y<-.80]=5
r,g,b=col[:,0],col[:,1],col[:,2]
hm=col[(y>.8)&(np.abs(x)<.2)].mean(0);dist=np.linalg.norm(col-hm,axis=1)
cls[(y>.4)&(y<=.72)&(np.abs(x)<.24)&(z>-.02)&(dist<60)]=1     # hair locks over chest (colour match to scalp hair)
head=y>.70;face=head&(y<.96)&(np.abs(x)<.1)&(z>hz);neck=(y>.64)&(y<=.70)&(np.abs(x)<.075)
cls[head]=1;cls[face|neck]=0
cls[(np.abs(x)>.74)&(y>.2)&(y<.8)]=0     # hands
tc=np.array([np.bincount(cls[t],minlength=6).argmax() for t in I])
print('vertex classes',np.bincount(cls,minlength=6),'tri classes',np.bincount(tc,minlength=6))
# lower arms (static pose, no rig): smooth weighted rotation about each shoulder
phi,px,py,x0,wid,yb=1.33,.25,.5,.26,.1,.2
Q=P.copy();Nn=N.copy()
for s in (1,-1):
    ax=np.abs(Q[:,0]);m=(Q[:,0]*s>0)&(np.abs(P[:,1]-py)<yb);w=smooth(x0,x0+wid,ax)*m;a=phi*w
    dx=ax-px;dy=Q[:,1]-py;nx=dx*np.cos(a)+dy*np.sin(a);ny=-dx*np.sin(a)+dy*np.cos(a)
    mm=w>0;Q[mm,0]=s*(px+nx[mm]);Q[mm,1]=py+ny[mm]
    nax=Nn[:,0]*s;nnx=nax*np.cos(a)+Nn[:,1]*np.sin(a);nny=-nax*np.sin(a)+Nn[:,1]*np.cos(a)
    Nn[mm,0]=s*nnx[mm];Nn[mm,1]=nny[mm]
Nn/=np.linalg.norm(Nn,axis=1,keepdims=True)+1e-9
order=np.argsort(tc,kind='stable');T=I[order];counts=np.bincount(tc,minlength=6)
q=np.round(Q*8000).astype(np.int16);nr=np.round(Nn*127).astype(np.int8)
buf=q.tobytes()+nr.tobytes()+T.astype(np.uint16).tobytes()+UV.astype(np.float32).tobytes()
bc=raw(0)  # original JPEG, untouched
mr=Image.open(io.BytesIO(raw(1))).convert('RGB');mr_b=io.BytesIO();mr.save(mr_b,'JPEG',quality=90,subsampling=0)
out=dict(nv=int(n),nt=int(len(T)),groups=[int(c) for c in counts],b=base64.b64encode(buf).decode(),bc=base64.b64encode(bc).decode(),mr=base64.b64encode(mr_b.getvalue()).decode(),bcw=2048,mrw=2048)
json.dump(out,open('galina.json','w'));print('mesh',len(buf)//1024,'KB  bc',len(bc)//1024,'KB  mr',len(mr_b.getvalue())//1024,'KB')
np.save('gal_Q.npy',Q);np.save('gal_N.npy',Nn);np.save('gal_T.npy',T);np.save('gal_UV.npy',UV);np.save('gal_cls.npy',cls)
open('base_bc.jpg','wb').write(bc);open('mr_pack.jpg','wb').write(mr_b.getvalue())
# class debug render
pal=np.array([[230,180,150],[150,60,30],[90,130,90],[70,70,200],[240,240,60],[30,30,30]],float)
shade(Q,T,pal[cls],'gal_cls.png',views=(0,),W=420,H=640)
