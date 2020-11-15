import appuifw,e32
from key_codes import *
from graphics import Image
def cn(x):
    return x.decode("utf8")
step_x=20
step_y=180
flag=1
jg=0
win=0
clrbr=[0xffffff,0x0000ff,0xff0000]
chesstray=[[0 for  i in range(15)]for j in range(15)]
def init():    
    canvas.bind(EKeyUpArrow,lambda: move(0,-1))
    canvas.bind(EKeyDownArrow,lambda: move(0,1))
    canvas.bind(EKeySelect,lambda: move(0,0))
    canvas.bind(EKeyLeftArrow,lambda: move(-1,0))
    canvas.bind(EKeyRightArrow,lambda: move(1,0))
    img.text((35,185),cn("蓝方"),clrbr[1])
    img.text((120,185),cn("红方"),clrbr[2])
    for  i in range(1,16):
        img.line((i*10,10,i*10,150),0xffffff)
        img.line((10,i*10,150,i*10),0xffffff)
def draw_chess(x,y,clr):
    img.point((x,y),clr,width=10)
def move(x,y):
    global step_x,step_y,flag,win
    if x==-1 and y==0:
            step_x=step_x-10
    if x==1 and y==0:
        step_x=step_x+10
    if x==0 and y==-1:
        step_y=step_y-10
    if x==0 and y==1:
        step_y=step_y+10
    if x==0 and y==0:
      if step_x>0 and step_x<160 and step_y>0 and step_y<160:
        if chesstray[step_x/10-1][step_y/10-1]==0:
            chesstray[step_x/10-1][step_y/10-1]=flag
            judge(step_x,step_y)
            if jg==0:
                if flag==-1:
                    step_x=20
                    step_y=180
                if flag==1:
                    step_x=150
                    step_y=180
                flag=-flag
def judge(x,y):
        global jg
        #左右#
        jg1=0
        jg2=0
        for i in range(10,x,10):
            if chesstray[(x-i)/10-1][y/10-1]==flag:
                jg1+=1
            else:
                break
        for i  in range(x+10,160,10):
            if  chesstray[i/10-1][y/10-1]==flag:
                jg2+=1
            else:
                break
        if jg1+jg2==4:
            jg=1
        ##上下##
        jg1=0
        jg2=0
        for i in range(10,y,10):
            if chesstray[x/10-1][(y-i)/10-1]==flag:
                jg1+=1
            else:
                break
        for i  in range(y+10,160,10):
            if  chesstray[x/10-1][i/10-1]==flag:
                jg2+=1
            else:
                break
        if jg1+jg2==4:
            jg=1        
        ##左上右下##
        jg1=0
        jg2=0
        m1=min(x,y)
        m2=max(x,y)
        for i in range(10,m1,10):
                if chesstray[(x-i)/10-1][(y-i)/10-1]==flag:
                    jg1+=1
                else:
                    break
        for i  in range(10,160-m2,10):
                if  chesstray[(x+i)/10-1][(y+i)/10-1]==flag:
                    jg2+=1
                else:
                    break
        if jg1+jg2==4:
            jg=1
        
        ##右上左下##
        jg1=0
        jg2=0
        m3=min(x,160-y)
        m4=min(160-x,y)
        for i in range(10,m3,10):
                if chesstray[(x-i)/10-1][(y+i)/10-1]==flag:
                    jg1+=1
                else:
                    break
        for i  in range(10,m4,10):
                if  chesstray[(x+i)/10-1][(y-i)/10-1]==flag:
                    jg2+=1
                else:
                    break
        if jg1+jg2==4:
            jg=1
def quit():
    global running
    running=0
def handle_redraw(rect):
    canvas.blit(img)
appuifw.app.screen='full'
img=Image.new((176,208))
canvas=appuifw.Canvas(event_callback=None,redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.exit_key_handler=quit
running=1
while running:
    img.clear(0)
    init()
    if flag==1:
        draw_chess(20,180,clrbr[flag])
        draw_chess(150,180,clrbr[0])
    if flag==-1:
        draw_chess(20,180,clrbr[0])
        draw_chess(150,180,clrbr[flag]) 
    if jg==0:
        draw_chess(step_x,step_y,clrbr[flag])
    if jg==1:
        if flag==1:
            img.text((70,180),cn("蓝方胜"),0x00ff00)
        else:
            img.text((70,180),cn("红方胜"),0x00ff00)
    for i in range(15):
        for  j in range(15):
            if chesstray[i][j]==-1:
                draw_chess(i*10+10,j*10+10,clrbr[-1])
            if chesstray[i][j]==1:
                draw_chess(i*10+10,j*10+10,clrbr[1])
    handle_redraw(())
    e32.ao_yield()