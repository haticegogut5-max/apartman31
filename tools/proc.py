import sys;import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np,io
from glbv import load,acc
from PIL import Image,ImageDraw
def get(f):
    j,bn=load(f'../assets/source_models/{f}.glb');p=j['meshes'][0]['primitives'][0]
    P=acc(j,bn,p['attributes']['POSITION']).astype(np.float64);I=acc(j,bn,p['indices']).reshape(-1,3).astype(np.int64)
    col=None
    if 'TEXCOORD_0' in p['attributes']:
        uv=acc(j,bn,p['attributes']['TEXCOORD_0']).astype(np.float64);bv=j['bufferViews'][j['images'][0]['bufferView']]
        a=np.array(Image.open(io.BytesIO(bn[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB'));h,w=a.shape[:2]
        col=a[np.clip((uv[:,1]*h).astype(int),0,h-1),np.clip((uv[:,0]*w).astype(int)%w,0,w-1)].astype(np.float64)
    return P,I,col
def cluster(P,I,col,g):
    mn=P.min(0);c=np.floor((P-mn)/g).astype(np.int64);key=c[:,0]*1000003+c[:,1]*1009+c[:,2]
    u,inv=np.unique(key,return_inverse=True);n=len(u);cnt=np.bincount(inv,minlength=n)[:,None]
    Q=np.zeros((n,3));np.add.at(Q,inv,P);Q/=cnt
    C=None
    if col is not None:C=np.zeros((n,3));np.add.at(C,inv,col);C/=cnt
    T=inv[I];ok=(T[:,0]!=T[:,1])&(T[:,1]!=T[:,2])&(T[:,0]!=T[:,2]);T=T[ok]
    s=np.sort(T,1);_,ui=np.unique(s,axis=0,return_index=True);T=T[ui]
    return Q,T,C
def shade(Q,T,C,out,views=(0,35),W=420,H=640,zoom=1.0,cy=0.0):
    tiles=[]
    for ang in views:
        t=np.radians(ang);R=np.array([[np.cos(t),0,np.sin(t)],[0,1,0],[-np.sin(t),0,np.cos(t)]]);V=Q@R.T
        im=Image.new('RGB',(W,H),(20,20,24));d=ImageDraw.Draw(im)
        A=V[T[:,0]];B=V[T[:,1]];Cc=V[T[:,2]];N=np.cross(B-A,Cc-A);nl=np.linalg.norm(N,axis=1)+1e-9;N/=nl[:,None]
        z=(A[:,2]+B[:,2]+Cc[:,2])/3;order=np.argsort(z)
        L=np.array([.3,.5,.8]);L/=np.linalg.norm(L);sh=np.clip(N@L,0,1)*.8+.25
        sx=H/2.1*zoom
        for i in order:
            if N[i,2]<-0.05:continue
            tri=[(W/2+V[k,0]*sx,H/2-(V[k,1]-cy)*sx) for k in T[i]]
            base=np.array([205,205,205]) if C is None else C[T[i]].mean(0)
            d.polygon(tri,fill=tuple(np.clip(base*sh[i],0,255).astype(int)))
        tiles.append(im)
    r=Image.new('RGB',(W*len(tiles),H));[r.paste(t,(i*W,0)) for i,t in enumerate(tiles)];r.save(out)
if __name__=='__main__':
    for f,g in [('textured_mesh',.014),('white_mesh',.012),('white_mesh_1',.012),('white_mesh__1_',.014)]:
        P,I,col=get(f);Q,T,C=cluster(P,I,col,g);print(f,len(P),'->',len(Q),'verts',len(T),'tris');shade(Q,T,C,f'{f}_s.png')
