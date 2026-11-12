import numpy as np
from proc import *
rs=np.random.RandomState(7)
def smooth(a,b,x):t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def bend(Q,px,py,phi,x0,wid,yb):
    Q=Q.copy()
    for s in (1,-1):
        ax=np.abs(Q[:,0]);m=(Q[:,0]*s>0)&(np.abs(Q[:,1]-py)<yb)
        w=smooth(x0,x0+wid,ax)*m
        dx=ax-px;dy=Q[:,1]-py;a=phi*w
        nx=dx*np.cos(a)+dy*np.sin(a);ny=-dx*np.sin(a)+dy*np.cos(a)
        Q[:,0]=np.where(w>0,s*(px+nx),Q[:,0]);Q[:,1]=np.where(w>0,py+ny,Q[:,1])
    return Q
def noise(Q,f):
    return .5+.5*(np.sin(Q[:,0]*f*1.7+Q[:,1]*f)+np.sin(Q[:,2]*f*2.3+Q[:,1]*f*.7))/2
def hexc(h):return np.array([int(h[i:i+2],16) for i in (1,3,5)],float)
def paint(Q,spec):
    y=Q[:,1];x=Q[:,0];z=Q[:,2];n=len(Q);C=np.zeros((n,3))
    hz=z[y>.8].mean()
    for i in range(n):pass
    clothes=hexc(spec['top']);C[:]=clothes
    C[y<spec['hem']]=hexc(spec['bottom'])
    sh=y<spec['shoe'];C[sh]=hexc(spec['shoes'])
    # sweater stripes
    if spec.get('stripe'):
        st=(y>spec['hem'])&(y<.52)&(np.sin(y*55)>.86);C[st]=hexc(spec['stripe'])
    # hands
    hand=np.abs(x)>spec['hand'];hy=hand&(y<.75);C[hy]=hexc(spec['skin'])
    # head
    face=(y>.74)&(y<.96)&(np.abs(x)<.09)&(z>hz+.025);neck=(y>.695)&(y<=.74)&(np.abs(x)<.065)&(z>hz-.05)
    hair=(y>.72)&~face
    C[hair]=hexc(spec['hair']);C[face]=hexc(spec['skin']);C[neck]=hexc(spec['skin'])*.92
    # lips/eyes tint
    eye=face&(y>.85)&(y<.875)&(np.abs(x)>.03)&(np.abs(x)<.075);C[eye]=C[eye]*.45
    lip=face&(y>.765)&(y<.785)&(np.abs(x)<.03);C[lip]=hexc('#9a5a58')
    # cloth variation + wear
    var=.86+.28*noise(Q,spec.get('nf',90))
    C*=var[:,None]
    C*=(.78+.22*smooth(-1,.2,y))[:,None]  # grime toward the ground
    C*=(1+(rs.rand(n)-.5)*.08)[:,None]
    return np.clip(C,0,255)
def pack(Q,T,C,name):
    q=np.round(Q*8000).astype(np.int16);col=np.clip(C,0,255).astype(np.uint8);idx=T.astype(np.uint16)
    b=q.tobytes()+col.tobytes()+idx.tobytes()
    import base64;return dict(nv=len(Q),nt=len(T),b=base64.b64encode(b).decode()),len(b)
def run(f,g,spec,bendp,out):
    P,I,col=get(f);Q,T,C=cluster(P,I,col,g)
    if spec:C=paint(Q,spec)
    if bendp:Q=bend(Q,*bendp)
    shade(Q,T,C,out+'.png',views=(0,30));return Q,T,C
if __name__=='__main__':
    spec2=dict(top='#6e2a34',bottom='#43597c',shoes='#d9d4c8',hem=.05,shoe=-.83,hand=.78,hair='#4a3020',skin='#d9b79c',stripe='#a8906c',nf=80)
    spec3=dict(top='#5a5238',bottom='#675b43',shoes='#201a16',hem=.24,shoe=-.74,hand=.58,hair='#c8a868',skin='#d6b496',nf=95)
    run('white_mesh',.012,spec2,(.22,.57,1.33,.24,.1,.2),'p2')
    run('white_mesh_1',.012,spec3,(.19,.6,.9,.2,.1,.22),'p3')
    run('textured_mesh',.014,None,(.25,.5,1.33,.26,.1,.2),'p1')
    from PIL import Image
    ims=[Image.open(f'p{i}.png') for i in (1,2,3)];W,H=ims[0].size;s=Image.new('RGB',(W,H*3))
    for i,im in enumerate(ims):s.paste(im,(0,H*i))
    s.resize((W*3//4,H*3*3//4)).save('pall.png')
