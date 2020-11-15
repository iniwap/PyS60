#-*-coding:utf-8-*-
import appuifw,e32,copy
from key_codes import *
from graphics import Image
step_x=20
step_y=180
bestMove=(0,0)
flag=1
jg=0
win=0
searchDepth=5
clrbr=[0xffffff,0x0000ff,0xff0000]
chesstray=[[0 for  i in range(15)]for j in range(15)]
lock=e32.Ao_lock()
def cn(x):
    return x.decode("utf8")
def get_evaluation(i,j,who):
    #第一维标示四方向，最后一维标示冲(0)活(1)死(-1)型以及几子
    chess_situation=[[0 for index in range(2)] for index in range(4)]
    #水平
    temp=0
    counter=0
    #<--●
    while j-temp>-1:
        if chesstray[i][j-temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if j-temp!=-1:
        if chesstray[i][j-temp]==0:
            chess_situation[0][0]=1
        else:
            chess_situation[0][0]=0
    #●-->
    temp=1
    while j+temp<15:
        if chesstray[i][j+temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if j+temp!=15:
        if chesstray[i][j+temp]==0:
            chess_situation[0][1]=1
        else:
            chess_situation[0][1]=0
            
    if chess_situation[0][0]==1 and chess_situation[0][1]==1:
        chess_situation[0][0]=1
        chess_situation[0][1]=counter
    elif chess_situation[0][0]==0 and chess_situation[0][1]==0:
        chess_situation[0][0]=-1
        chess_situation[0][1]=counter
    else:
        chess_situation[0][0]=0
        chess_situation[0][1]=counter
        
    #垂直
    temp=0
    counter=0
    #<--●
    while i-temp>-1:
        if chesstray[i-temp][j]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if i-temp!=-1:
        if chesstray[i-temp][j]==0:
            chess_situation[1][0]=1
        else:
            chess_situation[1][0]=0
    #●-->
    temp=1
    while i+temp<15:
        if chesstray[i+temp][j]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if i+temp!=15:
        if chesstray[i+temp][j]==0:
            chess_situation[1][1]=1
        else:
            chess_situation[1][1]=0
            
    if chess_situation[1][0]==1 and chess_situation[1][1]==1:
        chess_situation[1][0]=1
        chess_situation[1][1]=counter
    elif chess_situation[1][0]==0 and chess_situation[1][1]==0:
        chess_situation[1][0]=-1
        chess_situation[1][1]=counter
    else:
        chess_situation[1][0]=0
        chess_situation[1][1]=counter

    #\---45----\
    temp=0
    counter=0
    #<--●
    while j+temp<15 and i-temp>-1:
        if chesstray[i-temp][j+temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if j+temp!=15 and i-temp!=-1:
        if chesstray[i-temp][j+temp]==0:
            chess_situation[2][0]=1
        else:
            chess_situation[2][0]=0
    #●-->
    temp=1
    while i+temp<15 and j-temp>-1:
        if chesstray[i+temp][j-temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if i+temp!=15 and j-temp!=-1:
        if chesstray[i+temp][j-temp]==0:
            chess_situation[2][1]=1
        else:
            chess_situation[2][1]=0
            
    if chess_situation[2][0]==1 and chess_situation[2][1]==1:
        chess_situation[2][0]=1
        chess_situation[2][1]=counter
    elif chess_situation[2][0]==0 and chess_situation[2][1]==0:
        chess_situation[2][0]=-1
        chess_situation[2][1]=counter
    else:
        chess_situation[2][0]=0
        chess_situation[2][1]=counter

    #/---135----/
    temp=0
    counter=0
    #<--●
    while j-temp>-1 and i-temp>-1:
        if chesstray[i-temp][j-temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if j-temp!=-1 and i-temp!=-1:
        if chesstray[i-temp][j-temp]==0:
            chess_situation[3][0]=1
        else:
            chess_situation[3][0]=0
    #●-->
    temp=1
    while i+temp<15 and j+temp<15:
        if chesstray[i+temp][j+temp]==who:
            counter+=1
            temp+=1
            continue
        else:
            break
    if i+temp!=15 and j+temp!=15:
        if chesstray[i+temp][j+temp]==0:
            chess_situation[3][1]=1
        else:
            chess_situation[3][1]=0
            
    if chess_situation[3][0]==1 and chess_situation[3][1]==1:
        chess_situation[3][0]=1
        chess_situation[3][1]=counter
    elif chess_situation[3][0]==0 and chess_situation[3][1]==0:
        chess_situation[3][0]=-1
        chess_situation[3][1]=counter
    else:
        chess_situation[3][0]=0
        chess_situation[3][1]=counter
           
    Max=get_grade(chess_situation)
    return Max
def get_grade(chess_situation):
    total_score=0
    for k in range(4):
        chess_type=chess_situation[k][0]
        chess_num=chess_situation[k][1]
        if chess_num>4:
            total_score+=100000
        else:
            #活型
            if chess_type==1:
                if chess_num==4:
                    total_score+=30000
                if chess_num==3:
                    total_score+=5000
                if chess_num==2:
                    total_score+=3000
                if chess_num==1:
                    total_score+=50
            #冲型
            if chess_type==0:
                if chess_num==4:
                    total_score+=10000
                if chess_num==3:
                    total_score+=1000
                if chess_num==2:
                    total_score+=200
                if chess_num==1:
                    total_score+=3
            #死型
            if chess_type==-1:
                if chess_num==4:
                    total_score+=500
                if chess_num==3:
                    total_score+=100
                if chess_num==2:
                    total_score+=10
    return total_score
def judge(x,y):
        global jg
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
def move(x,y):
    global step_x,step_y,flag,win,jg,chesstray
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
                flag=-1
    handle_redraw(())
def alpha_beta(depth,alpha,beta,isMyTurn,x,y):
    global chesstray,bestMove,searchDepth
    moveLegal=[]
    if depth==0:
        CS=get_evaluation(x,y,-isMyTurn)
        return CS
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i>14 or y+j>14 or x+i<0 or y+j<0:
                continue
            elif chesstray[i+x][j+y]==0:
                    moveLegal.append((i+x,j+y))
    for i in range(-2,3):
        for j in range(-2,3):
            if abs(i)!=2 and abs(j)!=2:
                continue
            elif x+i>14 or y+j>14 or x+i<0 or y+j<0:
                continue
            elif chesstray[i+x][j+y]==0:
                moveLegal.append((i+x,j+y))
    for i in range(len(moveLegal)):
        (x,y)=moveLegal[i]
        chesstray[x][y]=isMyTurn
        score=-alpha_beta(depth-1,-beta,-alpha,-isMyTurn,x,y)
        if score>alpha:
            alpha=score
            if depth==searchDepth:
                bestMove=(x,y)
        chesstray[x][y]=0
        if alpha>=beta:
            break
    return alpha            
def handle_redraw(x):
    global step_x,step_y,flag,win,jg,chesstray,bestMove,searchDepth
    img.clear(0)
    img.text((35,185),cn("Blue"),clrbr[1])
    img.text((120,185),cn("Red"),clrbr[2])
    img.point((20,180),clrbr[1],width=10)
    img.point((150,180),clrbr[2],width=10)
    for  i in range(1,16):
        img.line((i*10,10,i*10,150),0xffffff)
        img.line((10,i*10,150,i*10),0xffffff)
    if jg==0:
        img.point((step_x,step_y),clrbr[flag],width=10)
    if jg==1:
        if flag==1:
            img.text((70,180),cn("Blue Win"),0x00ff00)
        else:
            img.text((70,180),cn("Red Win"),0x00ff00)
    if flag==-1:
        alpha_beta(searchDepth,-1000000,1000000,-1,step_x/10-1,step_y/10-1)
        chesstray[bestMove[0]][bestMove[1]]=-1
        judge(bestMove[0]*10+10,bestMove[1]*10+10)
        if jg==0:
            flag=1
    for i in range(15):
        for  j in range(15):
            if chesstray[i][j]==-1:
                img.point((i*10+10,j*10+10),clrbr[-1],width=10)
            if chesstray[i][j]==1:
                img.point((i*10+10,j*10+10),clrbr[1],width=10)
    canvas.blit(img)
   
img=Image.new((240,320))
canvas=appuifw.Canvas(redraw_callback=handle_redraw)
canvas.bind(EKeyUpArrow,lambda: move(0,-1))
canvas.bind(EKeyDownArrow,lambda: move(0,1))
canvas.bind(EKeySelect,lambda: move(0,0))
canvas.bind(EKeyLeftArrow,lambda: move(-1,0))
canvas.bind(EKeyRightArrow,lambda: move(1,0))
appuifw.app.body=canvas
appuifw.app.screen='full'
appuifw.app.exit_key_handler=lock.signal
lock.wait()