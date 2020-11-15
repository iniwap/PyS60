import appuifw
import e32
from key_codes import *
from graphics import Image
def cpu_ai():
    global step_x,step_y
    x1=0
    x2=0
    y1=0
    y2=0
    temp=0
    ct=0
    chess_situation=[[[[[0 for i in range(2)] for i in range(8)] for i in range(15)] for i in range(15)] for i in range(2)]
    chess_s1=[[0 for i in range(15)] for i in range(15)]
    chess_s2=[[0 for i in range(15)] for i in range(15)]
    for k in range(2):
        for i in range(15):
            for j in range(15):
                if chesstray[i][j]==0:
                    for q in range(8):
                        if k==0:
                            cp=1
                        else:
                            cp=-1
########ÉÏ·½#######
                        if q==0 and j>0:
                            while 1:
                                if chesstray[i][j-temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i][j-temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
                        #######×óÉÏ########        
                        if q==1 and j>0 and i>0:
                            while 1:
                                if chesstray[i-temp][j-temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i-temp][j-temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
                        ##########×ó·½######
if q==2 and i>0:
                            while 1:
                                if chesstray[i-temp][j]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i-temp][j]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
                        ########×óÏÂ######## 
if q==3 and j<14 and i>0:
                            while j+temp<14:
                                if chesstray[i-temp][j+temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i-temp][j+temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
#########ÏÂ·½########
if q==4 and j<14:
                            while j+temp<14:
                                if chesstray[i][j+temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i][j+temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
########ÓÒÏÂ########
if q==5 and j<14 and i<14:
                            while i+temp<14 and j+temp<14:
                                if chesstray[i+temp][j+temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i+temp][j+temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
#######ÓÒ·½######
if q==6 and i<14:
                            while 1:
                                if chesstray[i+temp][j]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i+temp][j]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
########ÓÒÉÏ########
if q==7 and j>0 and i<14:
                            while 1:
                                if chesstray[i+temp][j-temp]==cp:
                                    ct+=1
                                    temp+=1
                                    continue
                                else:
                                    break
                            chess_situation[k][i][j][q][0]=ct
                            ct=0
                            if chesstray[i+temp][j-temp]==0:
                                chess_situation[k][i][j][q][1]=1
                                temp=1
                            else:
                                chess_situation[k][i][j][q][1]=0
                                temp=1
    ################ÆÀ·Ö#############
    for k in range(2):
        for i in range(15):
            for j in range(15):
if k==0:
    for q in range(4):
if chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==4 and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=16000
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==3) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=750
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==2) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=30
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==1) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=10
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==4) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=16000
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==3) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=50
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==2) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=5
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==1) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=2
    chess_s1[i][j]=ct
    ct=0
if k==1:
    for q in range(4):
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==4) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=8000
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==3) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=150
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==2) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=30
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==1) and chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==1:
    ct+=10
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==4) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=7750
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==3) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=50
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==2) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=5
if (chess_situation[k][i][j][q][0]+chess_situation[k][i][j][q+4][0]==1) and ((chess_situation[k][i][j][q][1]==1 and chess_situation[k][i][j][q+4][1]==0) or (chess_situation[k][i][j][q][1]==0 and chess_situation[k][i][j][q+4][1]==1)):
    ct+=1
    chess_s2[i][j]=ct
    ct=0
    for i in range(15):
for j in range(15):
    if chess_s1[i][j]>chess_s1[x1][y1]:
x1=i
y1=j
    for i in range(15):
for j in range(15):
    if chess_s2[i][j]>chess_s2[x2][y2]:
x2=i
y2=j
    if chess_s2[x2][y2]<chess_s1[x1][y1]:
step_x=10*x1+10
step_y=10*y1+10
    else:
step_x=10*x2+10
step_y=10*y2+10
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
            chesstray[step_x/10-1][step_y/10-1]=1
            judge(step_x,step_y)
            if jg==0:
                    step_x=20
                    step_y=180
                    flag=-1
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
start_info=[cn("㊣"),cn("㊣"),cn("进"),cn("入"),cn("在"),cn("游"),cn("正"),cn("戏"),cn("㊣"),cn("㊣")]
for y in range(9):
  img.clear(0)
  img.rectangle((0,y*10,176,10+(y*10)), 0x99ccff, fill=0x99ccff)
  img.rectangle((0,198-10*y,176,208-(y*10)), 0x99ccff, fill=0x99ccff)
  handle_redraw(())
  e32.ao_sleep(0.08)
  if y==8:
      for j in range(10):
          img.rectangle((88-10*j,78,88,88),0,fill=0)
          img.rectangle((88,78,88+10*j,88),0,fill=0)
          img.rectangle((88-10*j,120,88,130),0,fill=0)
          img.rectangle((88,120,88+10*j,130),0,fill=0)
          handle_redraw(())
          e32.ao_sleep(0.2)
          if j%2==0:
              img.text((80-8*j,105),start_info[j],0xff0000)
              handle_redraw(())
          else:
              img.text((80+8*j,105),start_info[j],0xff0000)
              handle_redraw(())
e32.ao_sleep(3)
running=1
while running:
    img.clear(0)
    init()
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
    if flag==-1:
        cpu_ai()
        chesstray[step_x/10-1][step_y/10-1]=-1
        judge(step_x,step_y)
        if jg==0:
            flag=1
            step_x=20
            step_y=180
    draw_chess(20,180,clrbr[1])
    draw_chess(150,180,clrbr[2])
    handle_redraw(())
    e32.ao_yield()