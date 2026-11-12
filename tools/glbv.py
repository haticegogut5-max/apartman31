import struct,json,numpy as np,io,sys
from PIL import Image
def load(f):
    b=open(f,'rb').read();cl,_=struct.unpack('<II',b[12:20]);j=json.loads(b[20:20+cl]);o=20+cl
    bl,_=struct.unpack('<II',b[o:o+8]);bin_=b[o+8:o+8+bl];return j,bin_
def acc(j,bin_,i):
    a=j['accessors'][i];bv=j['bufferViews'][a['bufferView']];ct={5126:np.float32,5123:np.uint16,5125:np.uint32}[a['componentType']]
    n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']];off=bv.get('byteOffset',0)+a.get('byteOffset',0)
    return np.frombuffer(bin_,dtype=ct,count=a['count']*n,offset=off).reshape(-1,n)
def render(f,out):
    j,bn=load(f);p=j['meshes'][0]['primitives'][0];P=acc(j,bn,p['attributes']['POSITION']).astype(np.float64);I=acc(j,bn,p['indices']).reshape(-1,3) if 'indices' in p else None
    col=np.full((len(P),3),200,np.uint8)
    if 'TEXCOORD_0' in p['attributes']:
        uv=acc(j,bn,p['attributes']['TEXCOORD_0']);bv=j['bufferViews'][j['images'][0]['bufferView']]
        img=Image.open(io.BytesIO(bn[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB');a=np.array(img);h,w=a.shape[:2]
        col=a[np.clip((uv[:,1]*h).astype(int),0,h-1),np.clip((uv[:,0]*w).astype(int)%w,0,w-1)]
        print(f,'tex',img.size)
    tiles=[]
    for ang in (0,90,180):
        t=np.radians(ang);R=np.array([[np.cos(t),0,np.sin(t)],[0,1,0],[-np.sin(t),0,np.cos(t)]]);Q=P@R.T
        W,H=360,540;im=np.zeros((H,W,3),np.uint8);zb=np.full((H,W),-1e9)
        x=((Q[:,0]/2.05+.5)*W).astype(int);y=((1-(Q[:,1]/2.05+.5))*H).astype(int);z=Q[:,2]
        m=(x>=0)&(x<W)&(y>=0)&(y<H)
        order=np.argsort(z[m]);xs,ys,zs,cs=x[m][order],y[m][order],z[m][order],col[m][order]
        for dx in (0,1):
            for dy in (0,1):
                im[np.clip(ys+dy,0,H-1),np.clip(xs+dx,0,W-1)]=cs
        tiles.append(im)
    Image.fromarray(np.hstack(tiles)).save(out)
for i,f in enumerate(sys.argv[1:]):render(f,f'v{i}.png')
