#-*-coding:utf8-*-
############模块导入############
import appuifw, key_codes, glcanvas, graphics,e32,time
from math import *
from gles import *
##############变量定义###########
curve,angle,running,turning_axis ,scale=127,360.0,1,0,10
vertice=[]
texcoord=[]
np=[]
E=[[0.0 for i in range(128)]for i in range(128)]#灰度矩阵
print "processing...please,wait"
im=graphics.Image.open("e:\\1.jpg")
w, h= im.size
startread =time.clock()
##########图像预处理############
for i in range(w):
    for j in range(h):
        r,g,b=im.getpixel([(i,j)])[0]
        np.append(r)
        np.append(g)
        np.append(b)
        np.append(255)
        E[i][j]=round(r*0.3+g*0.59+b*0.11)
endread=time.clock()
print "image pre-processing time:",(endread-startread),"s"

############高斯平滑############
def GaussianSmoothing(original,width,height):
    smooth=[[0 for i in range(128)]for i in range(128)]
    template=[1,2,1,2,4,2,1,2,1]
    for j in range(1,height-1):
        for i in range(1,width-1):
            total = 0
            index = 0
            for m in range(j-1,j+2):
                for n in range(i-1,i+2):
                    total+=original[m][n]*template[index]
                    index+=1
            total/= 16.0
            smooth[j][i]=total
    return smooth

############SFS-Tsai算法############
def sfs():
    global E,zmap
    iter,Sx,Sy,Sz=2,0.001,0.001,1.0
    szy,szx=128,128
    Zn=[[0 for i in range(128)]for i in range(128)]
    Zn1=[[0.0 for i in range(128)]for i in range(128)]
    Si1=[[1.0 for i in range(128)]for i in range(128)]
    Si=[[0 for i in range(128)]for i in range(128)]
    Wn = 0.001*0.001
    Ps = Sx/Sz
    Qs = Sy/Sz
    d= max(E)
    d = max(d)
    for I in range(iter):
        for i in range(szy):
            for j in range(szx):
                if  j<1 or i<1 or j==szx-1 or i==szy-1:
                    p=0.0
                    q=0.0
                else:
                    p = Zn1[i][j]-Zn1[i][j-1]
                    q = Zn1[i][j]-Zn1[i-1][j]
                pq = 1 + p*p + q*q
                PQs = 1 + Ps*Ps + Qs*Qs
                E[i][j]=E[i][j]/d
                fZ = -1.0*(E[i][j]-max(0.0,(1+p*Ps+q*Qs)/(sqrt(pq)*sqrt(PQs))))
                dfZ = -1.0 *max(1.0,((Ps+Qs)/(sqrt(pq)*sqrt(PQs))-((p+q)*(1+p*Ps+q*Qs)/(sqrt(pq*pq*pq)*sqrt(PQs)))))
                Y = fZ + dfZ*Zn1[i][j]
                k = Si1[i][j]*dfZ/(Wn+dfZ*Si1[i][j]*dfZ)
                Si[i][j]= (1 - k*dfZ)*Si1[i][j]
                Zn[i][j]= Zn1[i][j]+ k*(Y-dfZ*Zn1[i][j])
        for i in range(szy):
            for j in range(szx):
                Zn1[i][j]=Zn[i][j]
                Si1[i][j]=Si[i][j]
    return Zn1

############计时显示#############
startsfs =time.clock()
tzmap=sfs()
endsfs =time.clock()
print "sfstime:",endsfs-startsfs,"s"

startgs =time.clock()
zmap=GaussianSmoothing(tzmap,w,h)
endgs =time.clock()
print "GaussianSmoothing:",endgs-startgs,"s"

##########OpenGL初始化###########
def myinit():
    glEnable(GL_DEPTH_TEST)#深度测试
    glClearColor( 0, 0, 0, 1.0 )
    #glEnable( GL_CULL_FACE  )#背面消隐
    for i in range(-64,63):
        for j in range(-64,64):
            vertice.append(i/64.0)
            vertice.append(j/64.0)
            vertice.append(abs(zmap[i+64][j+64]))
            texcoord.append(0.5+i/128.0)
            texcoord.append(0.5+j/128.0)
            
            vertice.append((i+1)/64.0)
            vertice.append(j/64.0)
            vertice.append(abs(zmap[i+1+64][j+64]))
            texcoord.append(0.5+(i+1)/128.0)
            texcoord.append(0.5+j/128.0)
            
    vertices = array(GL_FLOAT, 3,vertice)
    texcoords = array(GL_FLOAT, 2, texcoord)
    texture = array(GL_UNSIGNED_BYTE, 4, np)
    texhandle = glGenTextures( 1 )
    glBindTexture(GL_TEXTURE_2D,texhandle)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 128, 128, 0, GL_RGBA, GL_UNSIGNED_BYTE,texture)
    glTexEnvx(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glMatrixMode( GL_MODELVIEW )
    glEnableClientState( GL_VERTEX_ARRAY )
    glVertexPointerf(vertices)
    glTexCoordPointerf(texcoords)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glEnable(GL_TEXTURE_2D)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
########OPENGL显示控制函数##########
def display(frame):
    global turning_axis,angle,scale,curve
    iFrame,cameraD,SCALE=frame,200,10.0
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glTranslatef(0,0,-100.0)
    glScalef(scale,scale,scale)
    glPushMatrix()
    if turning_axis==0:
        glRotatef(angle,1.0,0.0,0.0)
    if turning_axis==1:
        glRotatef(angle,0.0,1.0,0.0)
    if turning_axis==2:
        glRotatef(angle,0.0,0.0,1.0)
    if turning_axis==3:
        glRotatef(angle,1.0,1.0,0.0)
    glMatrixMode( GL_TEXTURE )
    glLoadIdentity()
    glMatrixMode( GL_MODELVIEW )
    for i in range(curve):
        glDrawArrays( GL_TRIANGLE_STRIP, 2*128*i,128*2)
    glPopMatrix()
    
#########回调定义投影变换##########
def reshape():
    glViewport(0, 0, 240, 320)#设置视口
    aspect = 4/3.0
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    glFrustumf( -1.0, 1.0, -1.0*aspect, 1.0*aspect, 5.0,300.0)#透视投影
#    glOrthof(-20.0,20.0,-20.0,20.0,-20.0,20.0)#正交投影

############退出函数#############
def set_exit():
    global running, canvas
    print "\nsuccess!"
#    graphics.screenshot().save("c:\\line1.png")
    canvas=None
    running = 0
    
############按键操作#############
def keys(event):
    global turning_axis,angle,scale,curve
    if event['keycode'] == key_codes.EKeyStar:
        scale+=2
    if event['keycode'] == key_codes.EKeyHash:
        scale-=2
    if event['keycode'] == key_codes.EKey5:
        angle=315
        turning_axis = 1
        curve-=1
        if curve<12:
            curve=12
    if event['keycode'] == key_codes.EKeyDownArrow:
        turning_axis = 1
        angle-=5.0
    elif event['keycode'] == key_codes.EKeyRightArrow:
        turning_axis = 2
        angle-=5.0
    elif event['keycode'] == key_codes.EKeyLeftArrow:
        turning_axis = 3
        angle-=5.0
    elif event['keycode'] == key_codes.EKeyUpArrow:
        turning_axis = 0
        angle-=5.0
        
#############主函数##############
def main():
    appuifw.app.exit_key_handler=set_exit
    appuifw.app.screen = 'full'
    canvas=glcanvas.GLCanvas(redraw_callback=display,event_callback=keys, resize_callback=reshape)
    appuifw.app.body=canvas
    myinit()
    while running:
        canvas.drawNow()
        e32.ao_sleep(1)
main()