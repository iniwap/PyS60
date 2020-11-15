#-*-coding:utf-8-*-

import appuifw
import graphics
import e32
import random
import e32dbm
import os
from key_codes import *
Level_Score=500
r_s=random.randint(0,27)
rs=random.randint(0,27)
menu_y=0
menu_s=0
fulline=0
isdeath=0
sett=0
current_x=3
game_array=[[0 for i in range(11)] for i in range(21)]
current_y=0
flag=0
speed=0
stop=1
score=0
level=5
playing=0
ziti=u'CombinedChinesePlain12'
def handle_redraw(rect):
    canvas.blit(img)
canvas=appuifw.Canvas(event_callback=None,redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
img=graphics.Image.new((w,h))
color_box=[[(51,255,255),(51,102,255),(51,102,102),(204,102,102)],[(51,255,102),(255,255,51),(0,51,255),(204,204,255)],[(255,51,204),(255,51,51),(255,153,153),(153,0,204)],[(202,0,0),(0,153,0),(255,153,0),(0,204,153)]]
Stick1=[[1,0,0,0],                                [1,0,0,0],                               [1,0,0,0],                               [1,0,0,0]]
Stick2=[[1,1,1,1],                                [0,0,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Stick3=[[1,0,0,0],                                [1,0,0,0],                               [1,0,0,0],                               [1,0,0,0]]
Stick4=[[1,1,1,1],                                [0,0,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Triada1=[[0,1,0,0],                                [1,1,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Triada2=[[1,0,0,0],                                [1,1,0,0],                               [1,0,0,0],                               [0,0,0,0]]
Triada3=[[1,1,1,0],                                [0,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Triada4=[[0,1,0,0],                                [1,1,0,0],                               [0,1,0,0],                               [0,0,0,0]]
Lcorner1=[[1,0,0,0],                                [1,0,0,0],                               [1,1,0,0],                               [0,0,0,0]]
Lcorner2=[[1,1,1,0],                                [1,0,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Lcorner3=[[1,1,0,0],                                [0,1,0,0],                               [0,1,0,0],                               [0,0,0,0]]
Lcorner4=[[0,0,1,0],                                [1,1,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Rcorner1=[[1,1,0,0],                                [1,0,0,0],                               [1,0,0,0],                               [0,0,0,0]]
Rcorner2=[[1,1,1,0],                                [0,0,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Rcorner3=[[0,1,0,0],                                [0,1,0,0],                               [1,1,0,0],                               [0,0,0,0]]
Rcorner4=[[1,0,0,0],                                [1,1,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Lzigzag1=[[1,0,0,0],                                [1,1,0,0],                               [0,1,0,0],                               [0,0,0,0]]
Lzigzag2=[[0,1,1,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Lzigzag3=[[1,0,0,0],                                [1,1,0,0],                               [0,1,0,0],                               [0,0,0,0]]
Lzigzag4=[[0,1,1,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Rzigzag1=[[0,1,0,0],                                [1,1,0,0],                               [1,0,0,0],                               [0,0,0,0]]
Rzigzag2=[[1,1,0,0],                                [0,1,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Rzigzag3=[[0,1,0,0],                                [1,1,0,0],                               [1,0,0,0],                               [0,0,0,0]]
Rzigzag4=[[1,1,0,0],                                [0,1,1,0],                               [0,0,0,0],                               [0,0,0,0]]
Box1=[[1,1,0,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Box2=[[1,1,0,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Box3=[[1,1,0,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
Box4=[[1,1,0,0],                                [1,1,0,0],                               [0,0,0,0],                               [0,0,0,0]]
All_shape=[[Stick1,1,4],[Stick2,4,1],[Stick3,1,4],[Stick4,4,1],[Triada1,3,2],[Triada2,2,3],[Triada3,3,2],[Triada4,2,3],[Lcorner1,2,3],[Lcorner2,3,2],[Lcorner3,2,3],[Lcorner4,3,2],[Rcorner1,2,3],[Rcorner2,3,2],[Rcorner3,2,3],[Rcorner4,3,2],[Lzigzag1,2,3],[Lzigzag2,3,2],[Lzigzag3,2,3],[Lzigzag4,3,2],[Rzigzag1,2,3],[Rzigzag2,3,2],[Rzigzag3,2,3],[Rzigzag4,3,2],[Box1,2,2],[Box2,2,2],[Box3,2,2],[Box4,2,2]]
def move(x):
    global current_x,rs,speed,stop,menu_y,running,playing,level,sett,menu_s
    cxtemp=current_x
    rstemp=rs
    if x=="setup":
        menu_s-=1
    if x=="setdown":
        menu_s+=1
    if (menu_s==4 or menu_s<0) and sett!=0:
        menu_s=0
    if x=="setselect":
        if menu_s==0:
            if appuifw.query(chn('初级'),'query'):
                level=1
        if menu_s==1:
            if appuifw.query(chn('中级'),'query'):
                level=4
        if menu_s==2:
            if appuifw.query(chn('高级'),'query'):
                level=8
        if menu_s==3:
            appuifw.note(chn('设置完成'),'info')
    if x=="up":
        menu_y-=1
    if x=="down":
        menu_y+=1
    if menu_y==6 or menu_y<0:
        menu_y=0
    if x=="select":
        if menu_y==0:
            new_play()
        if menu_y==1:
            play()
        if menu_y==2:
            setting()
        if menu_y==3:
            help()
        if menu_y==4:
            rank()
        if menu_y==5:
            os.abort()
    if x==0:
        if (rs+1)%4==0:
            rs=4*(rs/4)
        else:
            rs+=1    
    if x==1 or x==-1:
        current_x+=x
    if x==2:
        speed=1
    if x==3:
        stop=-stop
    if All_shape[rs][1]+current_x>10 or current_x<0 or game_array[current_y][current_x+All_shape[rs][1]-1]==1 or game_array[current_y][current_x]==1:
            current_x=cxtemp
            rs=rstemp
def chn(x):
    return x.decode("utf8")
def dchn(x):
    return x.encode("utf8")
def init():
    global score,level
    img.clear(0x333333)
    img.text((130,80),chn("分数"),fill=0xff0000,font="title")
    img.text((130,100),chn(str(score)),fill=0x00ff00,font=u'Acb14')
    img.text((130,120),chn("难度"),fill=0xff0000,font="title")
    img.text((130,140),chn(str(level)),fill=0x00ff00,font=u'Acb14')
    for i in range(11):
        img.line((4+10*i,0,4+10*i,208),0xaaaaaa,width=2)
    img.line((106,0,106,208),0xaaaaaa)
    for i in range(21):
        img.line((0,4+10*i,110,4+10*i),0xaaaaaa,width=2)
    for i in range(6):
        img.rectangle((i,i,112-i,210-i),(i*40,i*40,i*40))
    for i in range(5):
        img.line((120+10*i,10,120+10*i,50),0xaaaaaa,width=2)
    for i in range(5):
        img.line((120,10+10*i,160,10+10*i),0xaaaaaa,width=2)
    handle_redraw(())
def game_board():
    for i in range(10):
        for j in range(20):
            if game_array[j][i]==1:
                img.rectangle((6+i*10,6+j*10,14+i*10,14+j*10),color_box[i%4][j%4],color_box[i%4][j%4])
    for i in range(4):
        for j in range(4):
            if All_shape[rs][0][j][i]==1:
                img.rectangle((10*(current_x+i)+6,current_y*10+6+10*j,10*(current_x+i)+14,current_y*10+14+10*j),color_box[i][j],color_box[i][j])
    for i in range(4):
        for j in range(4):
            if All_shape[r_s][0][j][i]==1:
                img.rectangle((10*i+122,12+10*j,10*i+130,20+10*j),color_box[i][j],color_box[i][j])
def judge_move():
    global current_y,rs,current_x,flag  
    for i in range(All_shape[rs][1]):
        for j in range(All_shape[rs][2]):
            if All_shape[rs][0][j][i]*game_array[current_y+j][current_x+i]==1:
                flag=1
                break
def clear_line():
    global fulline,score,level
    i=19
    add=0
    while i>3:
        for j in range(10):
            if game_array[i][j]==0:
                fulline=0
                break
            else:
                fulline=1
        if fulline==1:
            for k in range(i,3,-1):
                for t in range(10):
                    game_array[k][t]=game_array[k-1][t]
            i+=1
            add+=1
        i-=1
    if add==1:
        score+=1
    if add>1:
        score+=2*add-1
    if (score+1)%Level_Score==0:
        level+=1
    if level>10:
        level=10
def start():
    start_info=[chn("㊣"),chn("㊣"),chn("进"),chn("入"),chn("在"),chn("游"),chn("正"),chn("戏"),chn("㊣"),chn("㊣")]
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
              img.text((80-8*j,105),start_info[j],0xff0000,font=ziti)
              handle_redraw(())
          else:
              img.text((80+8*j,105),start_info[j],0xff0000,font=ziti)
              handle_redraw(())
    e32.ao_sleep(1)
    for i in range(20):
        img.clear(0)
        img.rectangle((0,0,176,18+(i*10)), 0x99ccff, fill=(153-(i/4)*50,204-(i/4)*50,255-(i/4)*50))
        handle_redraw(())
        e32.ao_sleep(0.02)
def setting():
    global trs,sett,menu_s
    trs=0
    sett=1
    canvas.bind(EKeyUpArrow,lambda: move("setup"))
    canvas.bind(EKeyDownArrow,lambda: move("setdown"))
    canvas.bind(EKeySelect,lambda: move("setselect"))
    appuifw.app.exit_key_handler=menu
    while 1:
        trs+=1
        img.clear(0)
        for i in range(5):
            img.line((60+10*i,20,60+10*i,60),0x333333,width=2)
        for i in range(5):
            img.line((60,20+10*i,100,20+10*i),0x333333,width=2)
        img.rectangle((0,0,176,208), 0x99ccff)
        for i in range(4):
            for j in range(4):
                if All_shape[trs%27][0][j][i]==1:
                    img.rectangle((10*i+62,22+10*j,10*i+70,30+10*j),color_box[i][j],color_box[i][j])
                    e32.ao_sleep(0.1)
        img.rectangle((50,menu_s*20+68,120,68+20*(menu_s+0.8)), 0x99ccff, fill=(103,154,201))
        img.text((60,80),chn("初级速度"),0x99ccff,font=ziti)
        img.text((60,100),chn("中级速度"),0x99ccff,font=ziti)
        img.text((60,120),chn("高级速度"),0x99ccff,font=ziti)
        img.text((60,140),chn("保存设置"),0x99ccff,font=ziti)
        img.text((30,160),chn('QQ 522765228'),0x00ff00,font=ziti)
        img.text((30,180),u'(c)', 0xffff00)
        img.text((60,180),chn('手机网 iniwap.cn'),0xff0000,font=ziti)
        handle_redraw(())
        e32.ao_sleep(0.08)
def menu():
 global sett
 sett=0
 trs=0
 canvas.bind(EKeyUpArrow,lambda: move("up"))
 canvas.bind(EKeyDownArrow,lambda: move("down"))
 canvas.bind(EKeySelect,lambda: move("select"))
 while 1:
  trs+=1
  img.clear(0)
  for i in range(5):
        img.line((60+10*i,20,60+10*i,60),0x333333,width=2)
  for i in range(5):
        img.line((60,20+10*i,100,20+10*i),0x333333,width=2)
  img.rectangle((0,0,176,208), 0x99ccff)
  for i in range(4):
        for j in range(4):
            if All_shape[trs%27][0][j][i]==1:
                img.rectangle((10*i+62,22+10*j,10*i+70,30+10*j),color_box[i][j],color_box[i][j])
                e32.ao_sleep(0.1)
  img.text((30,200),u'(c)', 0xffff00)
  img.text((50,200),chn('手机网 iniwap.cn'), 0xff0000,font=ziti)
  img.rectangle((50,menu_y*20+68,120,68+20*(menu_y+0.8)), 0x99ccff, fill=(103,154,201))
  img.text((60,80),chn("开始游戏"),0x99ccff,font=ziti)
  img.text((60,100),chn("继续游戏"),0x99ccff,font=ziti)
  img.text((60,120),chn("难度设置"),0x99ccff,font=ziti)
  img.text((60,140),chn("游戏帮助"),0x99ccff,font=ziti)
  img.text((60,160),chn("玩家排行"),0x99ccff,font=ziti)
  img.text((60,180),chn("退出游戏"),0x99ccff,font=ziti)
  handle_redraw(())
  e32.ao_sleep(0.08)
def new_play():
    global game_array,current_y,current_x,level,score,isdeath
    isdeath=0
    current_y=0
    current_x=3
    score=0
    game_array=[[0 for i in range(11)] for i in range(21)]
    play()
def play():
  global flag,current_y,current_x,speed,stop,rs,r_s,isdeath,score,level,playing
  playing=1
  canvas.bind(53,lambda: move(0))
  canvas.bind(52,lambda: move(-1))
  canvas.bind(54,lambda: move(1))
  canvas.bind(56,lambda: move(2))
  canvas.bind(50,lambda: move(3))
  canvas.bind(EKeyUpArrow,lambda: move(3))
  canvas.bind(EKeyDownArrow,lambda: move(2))
  canvas.bind(EKeySelect,lambda: move(0))
  canvas.bind(EKeyRightArrow,lambda: move(1))
  canvas.bind(EKeyLeftArrow,lambda: move(-1))
  appuifw.app.exit_key_handler=menu
  while 1:
   if isdeath==1:
       appuifw.note(chn("游戏结束"),"info")
       name=appuifw.query(chn("请输入您的名字"),"text")
       try:
           db=e32dbm.open("c:\\ranklist.e32dbm","c")
           db[dchn(name)]=str(score)
           db.close()
       except:
           appuifw.note(chn("保存失败"),"error")
       menu()
       break
   else:
    init()
    judge_move()
    if flag==1 or current_y+All_shape[rs][2]==21:
        for i in range(All_shape[rs][1]):
            for j in range(All_shape[rs][2]):
              if All_shape[rs][0][j][i]==1:
                game_array[current_y+j-1][current_x+i]=1
        clear_line()
        death()
        current_y=0
        current_x=3
        flag=0
        speed=0
        rs=r_s
        r_s=random.randint(0,27)
    game_board()
    if stop==1:
        current_y+=1
    if speed==0:  
        e32.ao_sleep(1-level/10.0)
    e32.ao_yield()
def help():
    help_txt=[chn("游戏基本操作"),chn("2键：暂停"),chn("4键：向左"),chn("5键：变形"),chn("6键：向右"),chn("8键：加速下落"),chn("右软键：主菜单")]
    appuifw.app.exit_key_handler=menu
    while 1:
        img.clear(0)
        img.rectangle((0,0,176,208),outline=color_box[random.randint(0,3)][random.randint(0,3)])
        img.text((30,30),help_txt[0],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,50),help_txt[1],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,70),help_txt[2],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,90),help_txt[3],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,110),help_txt[4],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,130),help_txt[5],fill=color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        img.text((10,150),help_txt[6],color_box[random.randint(0,3)][random.randint(0,3)],font=ziti)
        handle_redraw(())
        e32.ao_sleep(0.3)
def death():
    global isdeath
    for i in range(11):
        if game_array[2][i]==1:
            isdeath=1
            break
        else:
            isdeath=0            
def rank():
    appuifw.app.exit_key_handler=menu
    try:
        db=e32dbm.open("c:\\ranklist.e32dbm","r")
        tdb=db.items()
        db.close()
    except:
        appuifw.note(chn("暂无排行榜"),"error")
    for i in range(len(tdb)-1):
        for j in range(len(tdb)-i-1):
            if int(tdb[j][1])<int(tdb[j+1][1]):
                t=tdb[j]
                tdb[j]=tdb[j+1]
                tdb[j+1]=t
    while 1:
        img.clear(0)
        img.rectangle((0,0,176,208),outline=color_box[random.randint(0,3)][random.randint(0,3)])
        img.text((20,20),chn("排---------行-------榜"),0xff0000,font=ziti)
        img.text((20,190),chn("排--------行---------榜"),0xff0000,font=ziti)
        for i in  range(8):
            img.text((30,30+i*20),chn(tdb[i][0]),0x0000ff)
            img.text((140,30+i*20),chn(tdb[i][1]),0x00ff00)
        handle_redraw(())
        e32.ao_sleep(0.2)
        e32.ao_yield()
def game():
    start()
    menu()
game()