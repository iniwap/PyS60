#-*-coding:utf-8-*-

import appuifw
import graphics
import e32
import random
import time
import e32dbm
import os
import audio
from key_codes import *
pos_x=0
pos_y=0
menu_x=0
menu_y=0
cursor=0
auto=0
level=16
shuffle_num=24
hint_num=24
start=0
current=0
totaltime=0
menu_start=0
menu_end=0
previous_current=[]
link=[]
linktime=0
playing=0
in_help=0
in_setting=0
in_rank=0
in_menu=0
ziti=u'CombinedChinesePlain12'
pic_ID=[[-1 for i in range(10)]for i in range(10)]
def chn(x):
    return x.decode('utf8')
def dchn(x):
    return x.encode('utf8')
canvas=appuifw.Canvas(event_callback=None,redraw_callback=None)
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
bg=graphics.Image.new((w,h))
pic_game=[graphics.Image.new((20,20)) for i in range(level+2)]
def move_cursor(x,y):
    global pos_x,pos_y,pic_ID,hint_num,shuffle_num,menu_y,menu_x,auto,start,menu_start,totaltime,in_help,in_setting,in_rank,level,playing
    if x=='hint':
        if hint_num>0:
            hint()
    if x=='shuffle':
        if shuffle_num>0:
            shuffle()
    if y==0:
        pos_x+=x
        if pos_x<0:
            pos_x=7
        if pos_x>7:
            pos_x=0
    if x==0:
        pos_y+=y
        if pos_y<0:
            pos_y=7
        if  pos_y>7:
            pos_y=0
    if x==0 and y==0:
        select()
    if x=="up":
        menu_x-=1
    if x=="down":
        menu_x+=1
    if menu_x==5 or menu_x<0:
        menu_x=0
    if x=='select':
        if menu_x==0:
            if appuifw.query(chn('初级入门'),'query'):
                level=12
        if menu_x==1:
            if appuifw.query(chn('中级上路'),'query'):
                shuffle_num=16
                hint_num=16
                level=20
        if menu_x==2:
            if appuifw.query(chn('高级挑战'),'query'):
                shuffle_num=12
                hint_num=12
                level=28
        if menu_x==3:
            if appuifw.query(chn('设置动态排列'),'query'):
                auto=1
        if menu_x==4:
            appuifw.note(chn('设置已保存'),'info')
    if y=="up":
        menu_y-=1
    if y=="down":
        menu_y+=1
    if menu_y==5 or menu_y<0:
        menu_y=0
    if y=='select' and playing!=1:
        if menu_y==0:
            if appuifw.query(chn('继续游戏'),'query'):
                if is_win():
                    game()
                else:
                    if start==0:
                        totaltime=0
                        start=time.clock()
                    else:
                        menu_end=time.clock()
                        start+=menu_end-menu_start
                    play()
            else:
                shuffle_num=24
                hint_num=24
                level=16
                game()
        if menu_y==1:
            in_setting=1
            setting()
        if menu_y==2:
            in_help=1
            _help()
        if menu_y==3:
            in_rank=1
            rank()
        if menu_y==4:
            os.abort()
def setting():
    global menu_x,in_setting
    zmdi=0
    in_menu=0
    t_face=0
    t_pic=0
    canvas.bind(EKeyUpArrow,lambda:move_cursor("up","none"))
    canvas.bind(EKeyDownArrow,lambda:move_cursor("down","none"))
    canvas.bind(EKeySelect,lambda:move_cursor("select","none"))
    canvas.bind(53,lambda: None)
    canvas.bind(52,lambda: None)
    canvas.bind(54,lambda: None)
    canvas.bind(56,lambda: None)
    canvas.bind(50,lambda: None)
    canvas.bind(42,lambda: None)
    canvas.bind(35,lambda: None)
    setting_img=graphics.Image.new(canvas.size)
    appuifw.app.exit_key_handler=menu
    while in_setting:
        zmdi+=1
        t_face+=1
        t_pic+=1
        setting_img.clear(0xffffff)
        if t_pic>3:
            t_pic=1
        setting_img.blit(menu_pic[t_pic-1],target=(50,30))
        if zmdi>148:
            zmdi=0
        setting_img.text((176-2*zmdi,200),chn('(c)'),0xffff00,font=ziti)
        setting_img.text((196-2*zmdi,200),chn('手机网 iniwap.cn'),0xff0000,font=u'CombinedChinesePlain12')
        if t_face>7:
            t_face=1
        setting_img.blit(face[t_face-1],target=(30,menu_x*20+85))
        for i in range(7):
            setting_img.line((0,i*20+85,176,i*20+85),0x0000ff)
        setting_img.text((55,100),chn('初级入门'),0x99ccff,font=ziti)
        setting_img.text((55,120),chn('中级上路'),0x99ccff,font=ziti)
        setting_img.text((55,140),chn('高级挑战'),0x99ccff,font=ziti)
        setting_img.text((55,160),chn('动态排列'),0x99ccff,font=ziti)
        setting_img.text((55,180),chn('保存设置'),0x99ccff,font=ziti)
        setting_img.rectangle((0,0,176,208),0x0000ff)
        canvas.blit(setting_img)
        e32.ao_sleep(0.1)
        e32.ao_yield()
def _help():
    global in_help
    zmdi=0
    zmd=0
    in_menu=0
    canvas.bind(EKeySelect,lambda:None)
    canvas.bind(EKeyUpArrow,lambda:None)
    canvas.bind(EKeyDownArrow,lambda:None)
    canvas.bind(53,lambda: None)
    canvas.bind(52,lambda: None)
    canvas.bind(54,lambda: None)
    canvas.bind(56,lambda: None)
    canvas.bind(50,lambda: None)
    canvas.bind(42,lambda: None)
    canvas.bind(35,lambda: None)
    help_img=graphics.Image.new(canvas.size)
    help_txt=[chn("        小提示"),chn("所连图必须相同才能消掉"),chn("连线不能超过两个弯"),chn("炸弹表示剩余提示道具"),chn("礼物表示剩余重列道具"),chn("         祝您愉快")]
    get_help_pic()
    appuifw.app.exit_key_handler=menu
    while in_help:
        help_img.clear(0xffffff)
        help_img.text((40,20),chn('游戏操作及提示'),0xff0000,font=ziti)
        for i in range(1,9):
            help_img.line((0,i*20+5,176,i*20+5),0x0000ff)
        help_img.text((5,40),chn('菜单：导航键控制移动及选中'),0x00ff00,font=ziti)
        help_img.text((10,60),chn('右软键返回主菜单'),0x00ff00,font=ziti)
        help_img.text((5,80),chn('游戏：2468键或导航键控制移动 '),0x00ff00,font=ziti)
        help_img.text((10,100),chn('5键一次选中，两次取消选中'),0x00ff00,font=ziti)
        help_img.text((10,120),chn('#使用重列道具'),0x00ff00,font=ziti)
        help_img.text((10,140),chn('*使用提示道具'),0x00ff00,font=ziti)
        help_img.text((15,160),help_txt[(zmdi//5)%6],0xff0000,font=ziti)
        help_img.text((10,160),chn('['),0x0000ff,font=ziti)
        help_img.text((160,160),chn(']'),0x0000ff,font=ziti)
        if zmdi>30:
            zmd+=1
            zmdi=0
        if zmd>6:
            zmd=0
            zmdi=0
        help_img.blit(help_pic[zmd],target=(-300+zmdi*10,170),source=(0,0,300,20))
        zmdi+=1
        help_img.rectangle((0,0,176,208),0x0000ff)
        canvas.blit(help_img)
        e32.ao_sleep(0.5)
def rank():
    global in_rank
    in_menu=0
    canvas.bind(EKeySelect,lambda:None)
    canvas.bind(EKeyUpArrow,lambda:None)
    canvas.bind(EKeyDownArrow,lambda:None)
    canvas.bind(53,lambda: None)
    canvas.bind(52,lambda: None)
    canvas.bind(54,lambda: None)
    canvas.bind(56,lambda: None)
    canvas.bind(50,lambda: None)
    canvas.bind(42,lambda: None)
    canvas.bind(35,lambda: None)
    rank_img=graphics.Image.new(canvas.size)
    appuifw.app.exit_key_handler=menu
    try:
        db=e32dbm.open("e:\\System\\Apps\\lllook\\llkrank.e32dbm","r")
        tdb=db.items()
        db.close()
    except:
        try:
            db=e32dbm.open("c:\\System\\Apps\\lllook\\llkrank.e32dbm","r")
            tdb=db.items()
            db.close()
        except:
            appuifw.note(chn("fail to open rank"),"error")
    for i in range(len(tdb)-1):
        for j in range(len(tdb)-i-1):
            if int(tdb[j][1])>int(tdb[j+1][1]):
                t=tdb[j]
                tdb[j]=tdb[j+1]
                tdb[j+1]=t
    while in_rank:
        rank_img.clear(0xffffff)
        rank_img.text((50,30),chn('玩家排行榜'),0xff0000,font=ziti)
        for i in range(11):
            rank_img.line((0,i*20+40,176,i*20+40),0x0000ff)
        rank_img.line((90,40,90,200),0x0000ff)
        for i in  range(8):
            rank_img.text((30,55+i*20),chn(tdb[i][0]),0x00ff00,font=ziti)
            rank_img.text((100,55+i*20),chn(tdb[i][1]),0xff0000,font=ziti)
        rank_img.rectangle((0,0,176,208),0x0000ff)
        canvas.blit(rank_img)
        e32.ao_sleep(0.2)
        e32.ao_yield()
def select():
    global previous_current,linktime,S
    linktime=0
    if len(previous_current)==0:
        if pic_ID[pos_y+1][pos_x+1]!=-1:
            previous_current.append((pos_x+1,pos_y+1))
    elif len(previous_current)==1 and pic_ID[pos_y+1][pos_x+1]!=-1:
        if (pos_x+1,pos_y+1)==previous_current[-1]:
            del(previous_current[-1])
        else:
            previous_current.append((pos_x+1,pos_y+1))
            x1=previous_current[0][0]
            y1=previous_current[0][1]
            x2=previous_current[1][0]
            y2=previous_current[1][1]
            if pic_ID[y1][x1]!=-1 and pic_ID[y2][x2]!=-1 and pic_ID[y1][x1]==pic_ID[y2][x2] and (x1!=x2 or y1!=y2):
                if search_xy((x1,y1),(x2,y2)):
                    linktime=0.5
                    if link[0][0]=='x':
                        bg.line((x1*20,y1*20,link[0][1]*20,y1*20),(51,204,255),width=8)
                        bg.line((link[0][1]*20,y1*20,link[0][1]*20,y2*20),(51,204,255),width=8)
                        bg.line((x2*20,y2*20,link[0][1]*20,y2*20),(51,204,255),width=8)
                        canvas.blit(bg)
                    if link[0][0]=='y':
                        bg.line((x1*20,y1*20,x1*20,link[0][1]*20),(51,204,255),width=8)
                        bg.line((x1*20,link[0][1]*20,x2*20,link[0][1]*20),(51,204,255),width=8)
                        bg.line((x2*20,y2*20,x2*20,link[0][1]*20),(51,204,255),width=8)
                        canvas.blit(bg)
                    try:
                        S.play()
                    except:
                        pass
                    e32.ao_sleep(0.5)
                    del(previous_current[0])
                    del(previous_current[0])
                else:
                    del(previous_current[0])
    elif len(previous_current)==2:
        if (pos_x+1,pos_y+1)==previous_current[-1]:
            del(previous_current[-1])
        else:
            del(previous_current[0])
            previous_current.append((pos_x+1,pos_y+1))
def get_pic():
    global pic_game,level,pic
    pic_game=[graphics.Image.new((20,20)) for i in range(level+2)]
    pic_list=[i for i in range(105)]
    random.shuffle(pic_list)
    pic_list=pic_list[:level]
    for i in range(level):
            pic_game[i].blit(pic,target=(0,0),source=((pic_list[i]%15)*20,(pic_list[i]//15)*20,(pic_list[i]%15+1)*20,(pic_list[i]//15+1)*20))
    pic_game[level].blit(pic,target=(0,0),source=(40,100,60,120))
    pic_game[level+1].blit(pic,target=(0,0),source=(200,80,220,100)) 
def play():
    global pic_ID,pic_game,pos_x,pos_y,cursor,current,shuffle_num,hint_num,level,linktime,start,totaltime,playing
    playing=1
    canvas.bind(EKeyUpArrow,lambda:move_cursor(0,-1))
    canvas.bind(EKeyDownArrow,lambda:move_cursor(0,1))
    canvas.bind(EKeyLeftArrow,lambda:move_cursor(-1,0))
    canvas.bind(EKeyRightArrow,lambda:move_cursor(1,0))
    canvas.bind(EKeySelect,lambda:move_cursor(0,0))
    canvas.bind(53,lambda: move_cursor(0,0))
    canvas.bind(52,lambda: move_cursor(-1,0))
    canvas.bind(54,lambda: move_cursor(1,0))
    canvas.bind(56,lambda: move_cursor(0,1))
    canvas.bind(50,lambda: move_cursor(0,-1))
    canvas.bind(42,lambda: move_cursor('hint','hint'))
    canvas.bind(35,lambda: move_cursor('shuffle','shuffle'))
    appuifw.app.exit_key_handler=menu
    color=0x00ff00
    while playing:
        bg.clear(0xffffff)
        for i in range(8):
            for j in range(8):
                if pic_ID[j+1][i+1]!=-1:
                    bg.blit(pic_game[pic_ID[j+1][i+1]],target=(i*20+8,j*20+9),source=(0,0,20,20))
                bg.line((i*20+8,9,i*20+8,169),(51,204,255))
                bg.line((8,j*20+9,168,j*20+9),(51,204,255))
        bg.rectangle((7,8,169,169),(51,204,255),width=2)
        bg.rectangle((pos_x*20+8,pos_y*20+9,pos_x*20+29,pos_y*20+30),cursor)
        bg.text((2,189),chn('时间'),font=ziti)
        bg.rectangle((24,179,145,189),0,width=2)
        current=time.clock()-linktime
        T=int(current-start)
        bg.text((150,191),chn(str(T)),0xff0000,font=ziti)
        if T<=120:
            if T>40:
                color=0xffff00
            if T>80:
                color=0xff0000
            bg.rectangle((25,181,145-T,188),fill=color)
        if T>120:
            appuifw.note(chn('闯关失败'),'info')
            playing=0
            menu()
        if is_win()==1:
            appuifw.note(chn('下一关'),'info')
            level+=2
            totaltime+=T
            if level>32:
                appuifw.note(chn("通关了"),"info")
                name=appuifw.query(chn("请输入您的名字"),"text")
                try:
                   db=e32dbm.open("e:\\System\\Apps\\lllook\\llkrank.e32dbm","c")
                   db[dchn(name)]=str(totaltime)
                   db.close()
                   appuifw.note(chn("记录已保存"),"info")
                except:
                 try:
                   db=e32dbm.open("c:\\System\\Apps\\lllook\\llkrank.e32dbm","c")
                   db[dchn(name)]=str(totaltime)
                   db.close()
                   appuifw.note(chn("记录已保存"),"info")
                 except:
                     appuifw.note(chn("保存失败"),"error")
                playing=0
                menu()
            else:
                game()
        bg.text((60,205),chn(str(hint_num)),font=ziti)
        bg.text((140,205),chn(str(shuffle_num)),font=ziti)
        bg.blit(pic_game[-1],target=(40,193),source=(5,5,20,20))
        bg.blit(pic_game[-2],target=(120,193),source=(3,5,18,20))
        if len(previous_current)!=0:
            for pic_select in previous_current:
                bg.rectangle((pic_select[0]*20-12,pic_select[1]*20-11,pic_select[0]*20+9,pic_select[1]*20+10),0xff0000)
        cursor^=0xffffffff
        linktime=0
        bg.rectangle((0,0,176,208),0x0000ff)
        canvas.blit(bg)
        e32.ao_sleep(0.2)
        e32.ao_yield()
def is_win():
    global pic_ID
    win=1
    for i in range(8):
        for j in range(8):
            if pic_ID[j+1][i+1]!=-1:
                win=0
                break
        if win==0:
            break
    return win
def initial_pic():
    global pic_ID,level
    for i in range(8):
       for j in range(8):
            pic_ID[i+1][j+1]=((i*8+j)//2)%level
    for i in range(1,9):
        for j in range(1,9):
            tempx=random.randint(1,8)
            tempy=random.randint(1,8)
            if tempx!=i or tempy!=j:
                pic_ID[j][i],pic_ID[tempy][tempx]=pic_ID[tempy][tempx],pic_ID[j][i]
def shuffle():
    global shuffle_num,pic_ID
    shuffle_num-=1
    for x in range(1,9):
        for y in range(1,9):
            tempx=random.randint(1,8)
            tempy=random.randint(1,8)
            if tempx!=x or tempy!=y:
                pic_ID[y][x],pic_ID[tempy][tempx]=pic_ID[tempy][tempx],pic_ID[y][x]
def hint():
    global hint_num
    for x1 in range(1,9):
        for y1 in range(1,9):
            for x2 in range(1,9):
                for y2 in range(1,9):
                    if pic_ID[y1][x1]==-1 or pic_ID[y2][x2]==-1:
                        continue
                    if pic_ID[y1][x1]!=pic_ID[y2][x2]:
                        continue
                    if x1==x2 and y1==y2:
                        continue
                    pic1=(x1,y1)
                    pic2=(x2,y2)
                    if search_xy(pic1,pic2):
                        hint_num-=1
                        return 0
def extend_pic(xy,direction):
    extend_direction_pic=[0,0]
    if direction=='x':
        for i in range(xy[0],0,-1):
            if pic_ID[xy[1]][i-1]==-1:
                extend_direction_pic[0]+=1
            else:
                break
        for i in range(xy[0]+1,10):
            if pic_ID[xy[1]][i]==-1:
                extend_direction_pic[1]+=1
            else:
                break
    if direction=='y':
        for i in range(xy[1],0,-1):
            if pic_ID[i-1][xy[0]]==-1:
                extend_direction_pic[0]+=1
            else:
                break
        for i in range(xy[1]+1,10):
            if pic_ID[i][xy[0]]==-1:
                extend_direction_pic[1]+=1
            else:
                break
    return extend_direction_pic
def have_link(pic1,pic2,mutual_part,direction):
    global link,pic_ID
    link=[]
    flag=0
    if direction=='x':
        temp1=min(pic1[1],pic2[1])
        temp2=max(pic1[1],pic2[1])+1
        for i in range(mutual_part[0],mutual_part[1]+1):
            for j in range(temp1,temp2):
                if pic_ID[j][i]!=-1 and (i,j)!=pic1 and (i,j)!=pic2:
                    flag=0
                    break
                else:
                    flag=1
            if flag==1:
                pic_ID[pic1[1]][pic1[0]]=-1
                pic_ID[pic2[1]][pic2[0]]=-1
                auto_arrange()
                link.append(('x',i))
                return 1
    if direction=='y':
        temp1=min(pic1[0],pic2[0])
        temp2=max(pic1[0],pic2[0])+1
        for i in range(mutual_part[0],mutual_part[1]+1):
            for j in range(temp1,temp2):
                if pic_ID[i][j]!=-1 and (j,i)!=pic1 and (j,i)!=pic2:
                    flag=0
                    break
                else:
                    flag=1
            if flag==1:
                pic_ID[pic1[1]][pic1[0]]=-1
                pic_ID[pic2[1]][pic2[0]]=-1
                auto_arrange()
                link.append(('y',i))
                return 1
    return 0             
def search_xy(pic1,pic2):
    for direction in ['x','y']:
        mutual_part=[0,0]
        extend_pic1=extend_pic(pic1,direction)
        extend_pic2=extend_pic(pic2,direction)
        if direction=='x':
            temp1=max(pic1[0]-extend_pic1[0],pic2[0]-extend_pic2[0])
            temp2=min(pic1[0]+extend_pic1[1],pic2[0]+extend_pic2[1])
        if direction=='y':
            temp1=max(pic1[1]-extend_pic1[0],pic2[1]-extend_pic2[0])
            temp2=min(pic1[1]+extend_pic1[1],pic2[1]+extend_pic2[1])
        mutual_part[0]=temp1
        mutual_part[1]=temp2
        if mutual_part[0]<=mutual_part[1]:
            if have_link(pic1,pic2,mutual_part,direction):
                return 1
    return 0
def load():
    global pic,pic_ID,pic_game,S
    load_img=graphics.Image.new(canvas.size)
    t=-1
    for i in range(100):
        txt=[chn('您将进入连连看世界'),chn('开发者iniwap.cn'),chn('     #键洗牌道具'),chn('    *键提示道具'),chn('5键两次取消选中')]
        load_img.clear(0)
        load_img.text((60,70),chn('游戏加载中...'),0x0000ff,font=ziti)
        load_img.rectangle((40,80,140,100),0x77777777)
        for j in range(10):
            load_img.rectangle((40,80+j,40+i,100-j),fill=(50+j*2,50+j*2,255-j*10))
        load_img.text((80,95),chn(str(i+1)+'%'),0x00ff00,font=ziti)
        if i%20==0:
            t+=1
        load_img.text((40,120),txt[t],0x00ff00,font=ziti)
        canvas.blit(load_img)
        e32.ao_sleep(0.05)
    try:
        pic=graphics.Image.open('e:\\System\\Apps\\lllook\\llk.png')
    except:
        try:
            pic=graphics.Image.open('c:\\System\\Apps\\lllook\\llk.png')
        except:
                appuifw.note(chn('资源文件不存在加载失败'),'error')
    get_pic()
    initial_pic()
    try:
        S=audio.Sound.open('e:\\System\\Apps\\lllook\\game.wav')
    except:
        try:
            S=audio.Sound.open('c:\\System\\Apps\\lllook\\game.wav')
        except:
            pass
def menu():
    global menu_y,menu_start,in_setting,in_help,in_rank,in_menu,playing
    menu_start=time.clock()
    in_setting=0
    in_help=0
    in_rank=0
    playing=0
    in_menu=1
    zmdi=0
    t_face=0
    t_pic=0
    canvas.bind(EKeyUpArrow,lambda:move_cursor("none","up"))
    canvas.bind(EKeyDownArrow,lambda:move_cursor("none","down"))
    canvas.bind(EKeySelect,lambda:move_cursor("none","select"))
    canvas.bind(53,lambda: None)
    canvas.bind(52,lambda: None)
    canvas.bind(54,lambda: None)
    canvas.bind(56,lambda: None)
    canvas.bind(50,lambda: None)
    canvas.bind(42,lambda: None)
    canvas.bind(35,lambda: None)
    menu_img=graphics.Image.new(canvas.size)
    get_menu_pic()
    if not os.path.exists("e:\\System\\Apps\\lllook\\llkrank.e32dbm") and not os.path.exists("c:\\System\\Apps\\lllook\\llkrank.e32dbm"):
       try:
           db=e32dbm.open("e:\\System\\Apps\\lllook\\llkrank.e32dbm","c")
           db["player1"]=str(100)
           db["player2"]=str(100)
           db["player3"]=str(100)
           db["player4"]=str(100)
           db["player5"]=str(100)
           db["player6"]=str(100)
           db["player7"]=str(100)
           db["player8"]=str(100)
           db.close()
       except:
           try:
               db=e32dbm.open("c:\\System\\Apps\\lllook\\llkrank.e32dbm","c")
               db["player1"]=str(100)
               db["player2"]=str(100)
               db["player3"]=str(100)
               db["player4"]=str(100)
               db["player5"]=str(100)
               db["player6"]=str(100)
               db["player7"]=str(100)
               db["player8"]=str(100)
               db.close()
           except:
               appuifw.note(chn('fail'),"error")
    while in_menu:
        zmdi+=1
        t_face+=1
        t_pic+=1
        menu_img.clear(0xffffff)
        if t_pic>3:
            t_pic=1
        menu_img.blit(menu_pic[t_pic-1],target=(50,30))
        if zmdi>148:
            if zmdi<207:
                menu_img.text((20,200),chn('  Email：wtx2zhm@126.com'),0x0000ff,font=ziti)
            else:
                menu_img.text((20,200),chn('       QQ：522765228'),0x00ff00,font=ziti)
        if zmdi>296:
            zmdi=0
        menu_img.text((176-2*zmdi,200),chn('(c)'),0xffff00,font=ziti)
        menu_img.text((196-2*zmdi,200),chn('手机网 iniwap.cn'),0xff0000,font=ziti)
        if t_face>7:
            t_face=1
        menu_img.blit(face[t_face-1],target=(30,menu_y*20+85))
        for i in range(7):
            menu_img.line((0,i*20+85,176,i*20+85),0x0000ff)
        menu_img.text((55,100),chn('开始游戏'),0x99ccff,font=ziti)
        menu_img.text((55,120),chn('难度设置'),0x99ccff,font=ziti)
        menu_img.text((55,140),chn('游戏帮助'),0x99ccff,font=ziti)
        menu_img.text((55,160),chn('玩家排行'),0x99ccff,font=ziti)
        menu_img.text((55,180),chn('退出游戏'),0x99ccff,font=ziti)
        menu_img.rectangle((0,0,176,208),0x0000ff)
        canvas.blit(menu_img)
        e32.ao_sleep(0.1)
def get_menu_pic():
    global menu_pic,face
    menu_pic=[graphics.Image.new((30,30))for i in range(3)]
    for i in range(3):
        try:
            path="e:\\System\\Apps\\lllook\\pic\\"+str(i+1)+".jpg"
        except:
            try:
                path="c:\\System\\Apps\\lllook\\pic\\"+str(i+1)+".jpg"
            except:
                appuifw.note(chn('资源文件不存在加载失败'),'error')
        menu_pic[i]=graphics.Image.open(path)
    face=[graphics.Image.new((20,20))for i in range(7)]
    for i in range(7):
        try:
            path="e:\\System\\Apps\\lllook\\pic\\cursor"+str(i+1)+".jpg"
        except:
            try:
                path="c:\\System\\Apps\\lllook\\pic\\cursor"+str(i+1)+".jpg"
            except:
                appuifw.note(chn('资源文件不存在加载失败'),'error')
        face[i]=graphics.Image.open(path).resize((20,20))
def get_help_pic():
    global help_pic,pic
    help_pic=[graphics.Image.new((300,20)) for i in range(7)]
    for i in range(7):
       help_pic[i].blit(pic,target=(0,0),source=(0,i*20,300,(i+1)*20))
def auto_arrange():
    global auto
    if auto==1:
        for x in range(1,9):
            for y in range(1,9):
                if pic_ID[y][x]==-1:
                    for ty in range(y,1,-1):
                        pic_ID[ty][x]=pic_ID[ty-1][x]
                    pic_ID[1][x]=-1
def game():
    global pos_x,pos_y,shuffle_num,hint_num,pic_ID,start,totaltime
    totaltime=0
    pos_x=0
    pos_y=0
    initial_pic()
    get_pic()
    start=time.clock()
    play()
load()
menu()