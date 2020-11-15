#-*-coding:utf-8-*-

import appuifw
import graphics
import e32
import random
import os
import e32dbm
import copy
import time
from key_codes import *
class PictureSelect:
    def __init__(self):
        #import e32
        #import os
        #import appuifw
        self.appuifw=appuifw
        self.os=os
        self.e32=e32
        self.dir_stack=[]
        self.__picpath__=None
        self.lock=e32.Ao_lock()
        self.current_dir=['C','E']
    def  _encode(self,x):
        return x.encode('utf8')
    def _exit(self):
        self.lock.signal()
    def file_select(self):
        self.prev_screen=self.appuifw.app.screen
        self.prev_body=self.appuifw.app.body
        self.prev_exit=self.appuifw.app.exit_key_handler
        self.prev_title=self.appuifw.app.title

        self.appuifw.app.screen='normal'
        self.lb=self.appuifw.Listbox([chn(item) for item in self.current_dir],self.update)
        self.lb.bind(EKeyLeftArrow,lambda:self.update(-1))
        self.appuifw.app.title=chn('选择图片')
        self.appuifw.app.body=self.lb
        self.appuifw.app.exit_key_handler=self._exit
        self.lock.wait()
        
        self.lb.bind(EKeyLeftArrow,lambda:None)
        self.appuifw.app.screen=self.prev_screen
        self.appuifw.app.body=self.prev_body
        self.appuifw.app.exit_key_handler=self.prev_exit
        self.appuifw.app.title=self.prev_title
        if len(self.__picpath__)!=1:
            return self.__picpath__
        else:
            return None
    def join_path(self,current_path):
        return current_path[0]+':\\'+'\\'.join(current_path[1:])
    def list_dir(self,path_stack):
        path=self.join_path(path_stack)
        for dir_list in os.listdir(path):
            if os.path.isdir(path+'\\'+dir_list):
                self.current_dir.insert(0,dir_list)
            elif dir_list.find('.jpg')!=-1 or dir_list.find('.png')!=-1:
                self.current_dir.append(dir_list)    
    def update(self,i=None):
        if not i==None:
            index=i
        else:
            index=self.lb.current()
        if len(self.dir_stack)==0 and index!=-1:
            self.dir_stack.append(self.current_dir[index])
            self.current_dir=[]
            self.list_dir(self.dir_stack)
        elif index==-1:
            if len(self.dir_stack)>0:
                self.dir_stack.pop()
                if len(self.dir_stack)==0:
                    self.current_dir=['C','E']
                else:
                    self.current_dir=[]
                    self.list_dir(self.dir_stack)
        elif os.path.isdir(self.join_path(self.dir_stack)+'\\'+self.current_dir[index]):
            self.dir_stack.append(self._encode(chn(self.current_dir[index])))
            self.current_dir=[]
            self.list_dir(self.dir_stack)
        else:
            appuifw.note(chn('设置成功'),'info')
            dir_stack=[chn(i) for i in self.dir_stack]
            self.__picpath__=os.path.join(self.join_path(dir_stack),chn(self.current_dir[index]))
            self.lock.signal()
        items=[chn(s) for s in self.current_dir]
        if len(items)==0:
            items=[chn('(空)')]
        self.lb.set_list(items,0)
class IDAStar:
    def __init__(self,start):
        self.p=0
        self.INF=1000000
        self.start=start
        self.Sg=[0,1,2,3,4,5,6,7,8]
        self.__path__=[]
        self.__total__=0
    def fx(self,node):
        hx=0
        for i in range(9):
            if node[i]!=8:
                hx+=abs(node[i]//3-i//3)+abs(node[i]%3-i%3)
        f_x=hx+node[9]
        return f_x
    def get_path(self,solution):
        parent=solution[-1][11]
        while len(solution)!=0:
            temp=solution.pop()
            if temp[10]==0:
                break
            if temp[10]==parent:
                self.__path__.append(temp[:9])
                parent=temp[11]
        self.__path__.insert(0,self.Sg)
        self.__path__=self.__path__[:len(self.__path__)-1]
    def expand(self,node):
        s1=[]
        s2=[]
        s3=[]
        s4=[]
        snode=[]
        ij=node.index(8)
        if ij//3>0:
            Ntemp1=copy.deepcopy([node[0:3],node[3:6],node[6:9]])
            Ntemp1[ij//3][ij%3]=Ntemp1[ij//3-1][ij%3]
            Ntemp1[ij//3-1][ij%3]=8 
            for i in range(3):
                for j in range(3):
                    s1.append(Ntemp1[i][j])
            if s1!=node[:9]:
                self.p+=1
                s1.append(node[9]+1)
                s1.append(self.p)
                s1.append(node[10])
                snode.append(s1)
        if ij//3<2:
            Ntemp2=copy.deepcopy([node[0:3],node[3:6],node[6:9]])
            Ntemp2[ij//3][ij%3]=Ntemp2[ij//3+1][ij%3]
            Ntemp2[ij//3+1][ij%3]=8              
            for i in range(3):
                for j in range(3):
                    s2.append(Ntemp2[i][j])
            if s2!=node[:9]:
                self.p+=1
                s2.append(node[9]+1)
                s2.append(self.p)
                s2.append(node[10])
                snode.append(s2)
        if ij%3>0:
            Ntemp3=copy.deepcopy([node[0:3],node[3:6],node[6:9]])
            Ntemp3[ij//3][ij%3]=Ntemp3[ij//3][ij%3-1]
            Ntemp3[ij//3][ij%3-1]=8 
            for i in range(3):
                for j in range(3):
                    s3.append(Ntemp3[i][j])
            if s3!=node[:9]:
                self.p+=1
                s3.append(node[9]+1)
                s3.append(self.p)
                s3.append(node[10])
                snode.append(s3)
        if ij%3<2:
            Ntemp4=copy.deepcopy([node[0:3],node[3:6],node[6:9]])
            Ntemp4[ij//3][ij%3]=Ntemp4[ij//3][ij%3+1]
            Ntemp4[ij//3][ij%3+1]=8              
            for i in range(3):
                for j in range(3):
                    s4.append(Ntemp4[i][j])
            if s4!=node[:9]:
                self.p+=1
                s4.append(node[9]+1)
                s4.append(self.p)
                s4.append(node[10])
                snode.append(s4)
        return snode
    def main(self,root):
        solution=[]
        path=[]
        repeat=1
        bound=self.fx(root)
        while repeat:
            _end=time.clock()
            if _end-self.start>15:
                appuifw.note(chn('超时搜索失败'),'error')
                return
            path.append(root)
            next_bound=self.INF
            while len(path)!=0:
                node=path.pop()
                solution.append(node)
                if node[:9]==self.Sg:
                    #self.get_path(solution)
                    self.__total__=solution[-1][9]-1
                    repeat=0
                    return
                    break
                else:
                    for successor in self.expand(node):
                        if self.fx(successor)<=bound:
                            path.append(successor)      
                        else:
                            next_bound=min(next_bound,self.fx(successor))
            if len(path)==0 and next_bound==self.INF:
                appuifw.note(('搜索失败'),'error')
                break
            if len(path)==0 and next_bound!=self.INF:
                bound=next_bound
pos_x=0
pos_y=0
menu_y=1
setting_menu=0
isbackground=0
ispicture=0
black_white=0
isfinish=0
issee=0
step=0
search_step=0
level=4
difficulty=0
menu_visiable=0
start_posx=5
start_posy=10
dd=40
ziti=u'CombinedChinesePlain12'
picpath=None
pic_current=[[graphics.Image.new((40,40)) for i in range(4)] for i in range(4)]
pic_label_flag=[[0,0,0,0,0,0],[0,0,1,2,3,0],[0,4,5,6,7,0],[0,8,9,10,11,0],[0,12,13,14,15,0],[0,0,0,0,0,0]]
pic_label=[[0,0,0,0,0,0],[0,0,1,2,3,0],[0,4,5,6,7,0],[0,8,9,10,11,0],[0,12,13,14,15,0],[0,0,0,0,0,0]]
appuifw.app.body=canvas=appuifw.Canvas()
appuifw.app.screen="full"
def chn(x):
    return x.decode("utf8")
def move(x,y):
    global pos_x,pos_y,menu_y,setting_menu,level,bg,picpath,isbackground,bg_path,ispicture,pic_label,menu_visiable,search_step
    tpos_x=pos_x
    tpos_y=pos_y
    if y==0:
        pos_x+=x
        if pos_x<0 or pos_x==level:
            pos_x=tpos_x
    if x==0:
        pos_y+=y
        if pos_y<0 or pos_y==level:
            pos_y=tpos_y
    if x==0 and y==0:
        move_to()
    if y=="up":
        menu_y-=1
    if y=="down":
        menu_y+=1
    if menu_y==5 or menu_y<0:
        menu_y=0
    if y=="select":
        if menu_y==0:
          if ispicture==0:
            appuifw.note(chn('请选择游戏图片'),'info')
            try:
                ps1=PictureSelect()
                picpath=ps1.file_select()
                ispicture=1
            except:
                appuifw.note(chn("设置失败"),"error")
                ispicture=0
          search_step=0
          play()
        if menu_y==1:
            setting()
        if menu_y==2:
            _help()
        if menu_y==3:
            rank()
        if menu_y==4:
            os.abort()
    if x=="up":
        setting_menu-=1
    if x=="down":
        setting_menu+=1
    if setting_menu==4 or setting_menu<0:
        setting_menu=0
    if x=="select":
        if setting_menu==0:
            level=appuifw.query(chn("设置难度3或4或5"),"number")
            level=int(level)
            if level!=3 and level!=4 and level!=5:
                appuifw.note(chn("输入无效将使用默认值"),"error")
                level=3
        if setting_menu==1:
            if appuifw.query(chn("确定使用背景吗"),"query"):
              try:
                ps=PictureSelect()
                bg_path=ps.file_select()
                isbackground=1
              except:
                appuifw.note(chn("选择背景失败"),"error")
                bg=graphics.Image.new((canvas.size))
                isbackground=0
            else:
                bg=graphics.Image.new((canvas.size))
                isbackground=0
        if setting_menu==2:
            try:
                ps1=PictureSelect()
                picpath=ps1.file_select()
                ispicture=1
            except:
                appuifw.note(chn("设置失败"),"error")
                ispicture=0
        if setting_menu==3:
            appuifw.note(chn("设置已经保存"),"info")
    if x=="none" and y=="none":
        see_pic()
    if x=='#' and y=='#':
        if level==3:
            try:
                So=[0 for i in range(level*level+3)]
                for i in range(level*level):
                    So[i]=pic_label[i//level+1][i%level+1]
                start=time.clock()
                idas=IDAStar(start)
                idas.main(So)
                total_step=idas.__total__
                search_step=total_step
                appuifw.note(chn('还需'+str(total_step)+'步!'),'info')
            except:
                appuifw.note(chn('搜索失败'),'info')
        else:
            appuifw.note(chn('复杂度太大无法搜索'),'info')
def rank():
    canvas.bind(EKeySelect,lambda:None)
    img=graphics.Image.new(canvas.size)
    appuifw.app.exit_key_handler=menu
    try:
        db=e32dbm.open("e:\\System\\Apps\\Puzzle\\picrank.e32dbm","r")
        tdb=db.items()
        db.close()
    except:
        appuifw.note(chn("暂无排行"),"error")
    for i in range(len(tdb)-1):
        for j in range(len(tdb)-i-1):
            if int(tdb[j][1])>int(tdb[j+1][1]):
                t=tdb[j]
                tdb[j]=tdb[j+1]
                tdb[j+1]=t
    while 1:
        img.clear(0)
        for i  in  range(30,1,-1):
            img.ellipse((105-5*i/2,15-i/3,105+3*i/2,15+i),fill=(0,265-8*i,265-8*i))
        img.text((70,30),chn("排行榜"),0x0000ff,font=ziti)
        for i in  range(8):
            img.text((30,55+i*20),chn(tdb[i][0]),0x00ff00,font=ziti)
            img.text((100,55+i*20),chn("：      "+tdb[i][1]),0xff0000,font=ziti)
        canvas.blit(img)
        e32.ao_sleep(0.2)
        e32.ao_yield()
def setting():
    global black_white
    canvas.bind(EKeyUpArrow,lambda: move("up","none"))
    canvas.bind(EKeyDownArrow,lambda: move("down","none"))
    canvas.bind(EKeySelect,lambda: move("select","none"))
    setting_img=graphics.Image.new((176,208))
    try:
        menu_pic=graphics.Image.open("e:\\System\\Apps\\Puzzle\\menu_pic.jpg").resize((80,80))
        ismenu_pic=1
    except:
        menu_pic=graphics.Image.new((80,80))
        ismenu_pic=0
    appuifw.app.exit_key_handler=menu
    while 1:
        setting_img.clear(0)
        if ismenu_pic:
            setting_img.blit(menu_pic,target=(40,5))
        else:
            menu_pic.clear(0)
            menu_pic.rectangle((0,0,41,41),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            menu_pic.rectangle((40,0,80,41),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            menu_pic.rectangle((0,40,41,80),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            menu_pic.rectangle((40,40,80,80),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            setting_img.blit(menu_pic,target=(40,5))
        setting_img.line((80,5,80,83),0xffffff)
        setting_img.line((40,45,118,45),0xffffff)
        setting_img.rectangle((40,5,120,85),black_white)
        black_white^=0xffffff
        setting_img.rectangle((40,setting_menu*20+85,120,85+20*(setting_menu+0.8)), 0x99ccff, fill=(103,154,201))
        setting_img.text((50,100),chn("难度设置"),0x99ccff,font=ziti)
        setting_img.text((50,120),chn("背景设置"),0x99ccff,font=ziti)
        setting_img.text((50,140),chn("游戏图片"),0x99ccff,font=ziti)
        setting_img.text((50,160),chn("保存设置"),0x99ccff,font=ziti)
        setting_img.text((30,180),u'(c)', 0xffff00)
        setting_img.text((50,180),chn('手机网： iniwap.cn'), 0xff0000,font=ziti)
        canvas.blit(setting_img)
        e32.ao_sleep(0.4)
def _help():
    canvas.bind(EKeySelect,lambda: None)
    help_img=graphics.Image.new((176,208))
    appuifw.app.exit_key_handler=menu
    while 1:
        help_img.clear(0)
        help_img.rectangle((0,10,176,30),0x99ccff,fill=(103,154,201))
        help_img.text((20,25),chn('---游戏操作以及设置说明---'),0x99ccff,font=ziti)
        help_img.text((40,40),chn("2键：向上"),0x00ff00,font=ziti)
        help_img.text((40,60),chn("4键：向左"),0x00ff00,font=ziti)
        help_img.text((40,80),chn("5键：移动"),0x00ff00,font=ziti)
        help_img.text((40,100),chn("6键：向右"),0x00ff00,font=ziti)
        help_img.text((40,120),chn("8键：向下"),0x00ff00,font=ziti)
        help_img.text((40,140),chn("0键：查看原图"),0x00ff00,font=ziti)
        help_img.text((40,160),chn("右软键：返回菜单"),0x00ff00,font=ziti)
        help_img.text((10,175),chn("注意：设置不是必须的"),0xff0000,font=ziti)
        help_img.text((5,190),chn("如果不设置则为默认设置"),0xff0000,font=ziti)
        canvas.blit(help_img)
        e32.ao_yield()
def load():
    start_info=[chn("拼"),chn("图"),chn("是"),chn("一"),chn("款"),chn("非常"),chn("好玩"),chn("的"),chn("智力"),chn("游戏"),chn("游戏加载中…"),chn("拼图是一款非常好的智力游戏")]
    img=graphics.Image.new(canvas.size)
    img.clear(0)
    for i in range(10):
        img.text((random.randint(10,160),random.randint(10,190)),start_info[i],(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=ziti)
        canvas.blit(img)
        e32.ao_sleep(0.5)
    e32.ao_sleep(1)
    img.clear(0)
    img.text((10,100),start_info[11],0x00ff00,font=ziti)
    canvas.blit(img)
    e32.ao_sleep(1)
    img.clear(0)
    img.text((40,100),start_info[10],0xff000,font=ziti)
    canvas.blit(img)
    e32.ao_sleep(1)
def menu():
 global black_white,menu_visiable
 menu_visiable=1
 canvas.bind(EKeyUpArrow,lambda: move("none","up"))
 canvas.bind(EKeyDownArrow,lambda: move("none","down"))
 canvas.bind(EKeySelect,lambda: move("none","select"))
 img=graphics.Image.new((176,208))
 if not os.path.exists("e:\\System\\Apps\\Puzzle\\picrank.e32dbm"):
   try:
           db=e32dbm.open("e:\\System\\Apps\\Puzzle\\picrank.e32dbm","c")
           db["player1"]=str(30)
           db["player2"]=str(30)
           db["player3"]=str(30)
           db["player4"]=str(30)
           db["player5"]=str(30)
           db["player6"]=str(30)
           db["player7"]=str(30)
           db["player8"]=str(30)
           db.close()
   except:
           appuifw.note(chn("保存成绩失败"),"error")
 try:
     menu_pic=graphics.Image.open("e:\\System\\Apps\\Puzzle\\menu_pic.jpg").resize((80,80))
     ismenu_pic=1
 except:
     menu_pic=graphics.Image.new((80,80))
     ismenu_pic=0
 while menu_visiable:
  img.clear(0)
  if ismenu_pic:
      img.blit(menu_pic,target=(40,5))
  else:
      menu_pic.clear(0)
      menu_pic.rectangle((0,0,41,41),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      menu_pic.rectangle((40,0,80,41),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      menu_pic.rectangle((0,40,41,80),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      menu_pic.rectangle((40,40,80,80),outline=0xffffff,fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      img.blit(menu_pic,target=(40,5))
  img.line((80,5,80,83),0xffffff)
  img.line((40,45,118,45),0xffffff)
  img.rectangle((40,5,120,85),black_white)
  black_white^=0xffffff
  img.text((30,200),u'(c)', 0xffff00)
  img.text((50,200),chn('手机网 iniwap.cn'), 0xff0000,font=ziti)
  img.rectangle((40,menu_y*20+85,120,85+20*(menu_y+0.8)), 0x99ccff, fill=(103,154,201))
  img.text((55,100),chn("开始游戏"),0x99ccff,font=ziti)
  img.text((55,120),chn("游戏设置"),0x99ccff,font=ziti)
  img.text((55,140),chn("游戏帮助"),0x99ccff,font=ziti)
  img.text((55,160),chn("玩家排行"),0x99ccff,font=ziti)
  img.text((55,180),chn("退出游戏"),0x99ccff,font=ziti)
  canvas.blit(img)
  e32.ao_sleep(0.4)
def move_to():
    global pic_label,isfinish,step
    if pic_label[pos_y+1][pos_x+2]==level*level-1:
        pic_label[pos_y+1][pos_x+2]=pic_label[pos_y+1][pos_x+1]
        pic_label[pos_y+1][pos_x+1]=level*level-1
        step+=1
    if pic_label[pos_y+1][pos_x]==level*level-1:
        pic_label[pos_y+1][pos_x]=pic_label[pos_y+1][pos_x+1]
        pic_label[pos_y+1][pos_x+1]=level*level-1
        step+=1
    if pic_label[pos_y+2][pos_x+1]==level*level-1:
        pic_label[pos_y+2][pos_x+1]=pic_label[pos_y+1][pos_x+1]
        pic_label[pos_y+1][pos_x+1]=level*level-1
        step+=1
    if pic_label[pos_y][pos_x+1]==level*level-1:
        pic_label[pos_y][pos_x+1]=pic_label[pos_y+1][pos_x+1]
        pic_label[pos_y+1][pos_x+1]=level*level-1
        step+=1
    finish()
def division_line():
    global black_white
    for i in range(1,level):
        bg.line((start_posx+i*dd,start_posy,i*dd+start_posx,pic.size[1]+start_posy),0xffffff,width=1)
        bg.line((start_posx,start_posy+i*dd,start_posx+pic.size[0],start_posy+i*dd),0xffffff,width=1)
    bg.rectangle((start_posx,start_posy,start_posx+1+pic.size[0],start_posy+1+pic.size[1]),0xffffff)
    black_white^=0xffffff
    bg.rectangle((start_posx+pos_x*dd,start_posy+pos_y*dd,start_posx+1+(pos_x+1)*dd,start_posy+1+(pos_y+1)*dd),outline=black_white)
def level_3():
    global level,start_posx,start_posy,dd,pic,pic_label,pic_label_flag,picpath,ispicture,pos_x,pos_y
    level=3
    pos_x=0
    pos_y=0
    start_posx=15
    start_posy=10
    dd=50
    pic_current=[[graphics.Image.new((50,50)) for i in range(3)] for i in range(3)]
    pic_label_flag=[[0,0,0,0,0],[0,0,1,2,0],[0,3,4,5,0],[0,6,7,8,0],[0,0,0,0,0]]
    pic_label=[[0,0,0,0,0],[0,0,1,2,0],[0,3,4,5,0],[0,6,7,8,0],[0,0,0,0,0]]
    if ispicture==1:
        pic=graphics.Image.open(picpath).resize((150,150))
    else:
        try:
            pic=graphics.Image.open("e:\\System\\Apps\\Puzzle\\gamepic.jpg").resize((150,150))
        except:
            appuifw.note(chn("启动失败游戏图片不存在"),"error")
            appuifw.note(chn("请确认已设置游戏图片"),"info")            
def level_4():
    global level,start_posx,start_posy,dd,pic,pic_label,pic_label_flag,picpath,ispicture
    level=4
    pos_x=0
    pos_y=0
    start_posx=5
    start_posy=10
    dd=40
    pic_current=[[graphics.Image.new((40,40)) for i in range(4)] for i in range(4)]
    pic_label_flag=[[0,0,0,0,0,0],[0,0,1,2,3,0],[0,4,5,6,7,0],[0,8,9,10,11,0],[0,12,13,14,15,0],[0,0,0,0,0,0]]
    pic_label=[[0,0,0,0,0,0],[0,0,1,2,3,0],[0,4,5,6,7,0],[0,8,9,10,11,0],[0,12,13,14,15,0],[0,0,0,0,0,0]]
    if ispicture==1:
        pic=graphics.Image.open(picpath).resize((160,160))
    else:
        try:
            pic=graphics.Image.open("e:\\System\\Apps\\Puzzle\\gamepic.jpg").resize((160,160))
        except:
            appuifw.note(chn("启动失败"),"error")
            appuifw.note(chn("请确认已设置游戏图片"),"info")            
#pic.save("c:\haha.jpg",quality=100)
def level_5():
    global level,start_posx,start_posy,dd,pic,pic_label,pic_label_flag,picpath,ispicture
    
    pos_x=0
    pos_y=0
    level=5
    start_posx=15
    start_posy=10
    dd=30
    pic_current=[[graphics.Image.new((30,30)) for i in range(5)] for i in range(5)]
    pic_label_flag=[[0,0,0,0,0,0,0],[0,0,1,2,3,4,0],[0,5,6,7,8,9,0],[0,10,11,12,13,14,0],[0,15,16,17,18,19,0],[0,20,21,22,23,24,0],[0,0,0,0,0,0,0]]
    pic_label=[[0,0,0,0,0,0,0],[0,0,1,2,3,4,0],[0,5,6,7,8,9,0],[0,10,11,12,13,14,0],[0,15,16,17,18,19,0],[0,20,21,22,23,24,0],[0,0,0,0,0,0,0]]
    if ispicture==1:
        pic=graphics.Image.open(picpath).resize((150,150))
    else:
        try:
            pic=graphics.Image.open("e:\\System\\Apps\\Puzzle\\gamepic.jpg").resize((150,150))
        except:
            appuifw.note(chn("启动失败"),"error")
            appuifw.note(chn("请确认已设置游戏图片"),"info")            
def pic_division():
    global pic_current,pic
    pic_current=[[graphics.Image.new((dd,dd)) for i in range(level)] for i in range(level)]
    for i in range(level):
        for j in range(level):
            pic_current[j][i].blit(pic,target=(0,0),source=(i*dd,j*dd,(i+1)*dd,(j+1)*dd))
def expand(node):
    global level
    s1=[]
    s2=[]
    s3=[]
    s4=[]
    snode=[]
    ij=node.index(level*level-1)
    if ij//level>0:
        Ntemp1=[]
        for i in range(level):
            Ntemp1.append(node[level*i:level*(i+1)])
        Ntemp1[ij//level][ij%level]=Ntemp1[ij//level-1][ij%level]
        Ntemp1[ij//level-1][ij%level]=level*level-1 
        for i in range(level):
            for j in range(level):
                s1.append(Ntemp1[i][j])
        if len(s1)!=0 and s1!=node and s1 not in STEPS:
            snode.append(s1)
    if ij//level<level-1:
        Ntemp2=[]
        for i in range(level):
            Ntemp2.append(node[level*i:level*(i+1)])
        Ntemp2[ij//level][ij%level]=Ntemp2[ij//level+1][ij%level]
        Ntemp2[ij//level+1][ij%level]=level*level-1              
        for i in range(level):
            for j in range(level):
                s2.append(Ntemp2[i][j])
        if len(s2)!=0 and s2!=node and s2 not in STEPS:
            snode.append(s2)
    if ij%level>0:
        Ntemp3=[]
        for i in range(level):
            Ntemp3.append(node[level*i:level*(i+1)])
        Ntemp3[ij//level][ij%level]=Ntemp3[ij//level][ij%level-1]
        Ntemp3[ij//level][ij%level-1]=level*level-1 
        for i in range(level):
             for j in range(level):
                s3.append(Ntemp3[i][j])
        if len(s3)!=0 and s3!=node and s3 not in STEPS:
            snode.append(s3)
    if ij%level<level-1:
        Ntemp4=[]
        for i in range(level):
            Ntemp4.append(node[level*i:level*(i+1)])
        Ntemp4[ij//level][ij%level]=Ntemp4[ij//level][ij%level+1]
        Ntemp4[ij//level][ij%level+1]=level*level-1              
        for i in range(level):
             for j in range(level):
                s4.append(Ntemp4[i][j])
        if len(s4)!=0 and s4!=node and s4 not in STEPS  :
            snode.append(s4)
    return snode
def creat_pic():
    global STEPS,difficulty,pic_label,level
    difficulty=random.randint(level*3,level*6)
    STEPS=[]
    STEPS.append([i for i in range(level*level)])
    while len(STEPS)<=difficulty:
        successors=expand(STEPS[-1])
        s_index=random.randint(0,len(successors)-1)
        STEPS.append(successors[s_index])
    for i in range(1,level+1):
        for j in range(1,level+1):
            pic_label[j][i]=STEPS[-1][(j-1)*level+i-1]
def finish():
    global isfinish,pic_label,pic_label_flag
    if pic_label!=pic_label_flag:
        isfinish=0
    else:
        isfinish=1
def play():
  global level,start_posx,start_posy,dd,pic_current,pic,isfinish,step,isbackground,bg_path,bg,picpath,ispicture,issee,difficulty,search_step
  menu_visiable=0
  canvas.bind(53,lambda: move(0,0))
  canvas.bind(EKeySelect,lambda: move(0,0))
  canvas.bind(52,lambda: move(-1,0))
  canvas.bind(EKeyLeftArrow,lambda: move(-1,0))
  canvas.bind(48,lambda: move("none","none"))
  canvas.bind(35,lambda: move("#","#"))
  canvas.bind(54,lambda: move(1,0))
  canvas.bind(EKeyRightArrow,lambda: move(1,0))
  canvas.bind(56,lambda: move(0,1))
  canvas.bind(EKeyDownArrow,lambda: move(0,1))
  canvas.bind(50,lambda: move(0,-1))
  canvas.bind(EKeyUpArrow,lambda: move(0,-1))
  appuifw.app.exit_key_handler=menu
  step=0
  if isbackground==1 and issee==0:
      bg=graphics.Image.open(bg_path).resize(canvas.size)
  else:
      try:
          bg=graphics.Image.open("e:\\System\\Apps\\Puzzle\\background.jgp")
      except:
          bg=graphics.Image.new(canvas.size)
      bg.clear(0)
  if issee==0:
    if level==3:
      level_3()
      pic_division()
      creat_pic()
    if level==4:
      level_4()
      pic_division()
      creat_pic()
    if level==5:
      level_5()
      pic_division()
      creat_pic()
  issee=0
  hint=0
  hint_img=graphics.Image.new((160,13))
  some_hint=[chn('       温馨提醒'),chn('白色框中显示为已走步数'),chn('当前难度'+str(difficulty)+'步内可解决'),chn('0 键查看原图'),chn('#查看当前最少需几步'),chn('上次搜索结果:未搜或超时')]
  while 1:
    hint_img.clear(0xffffff)
    hint+=1
    for i in range(level):
        for j in range(level):
            if pic_label[j+1][i+1]!=level*level-1:
                bg.blit(pic_current[pic_label[j+1][i+1]/level][pic_label[j+1][i+1]%level],target=(start_posx+i*dd,start_posy+j*dd))
            if pic_label[j+1][i+1]==level*level-1:
                bg.blit(graphics.Image.new((dd,dd)),target=(start_posx+dd*i,start_posy+dd*j))
                bg.text((start_posx+dd*i,start_posy+dd*j+dd*1.5/2),str(step).decode("utf8"),0,font=u"Acb14")
        division_line()
        if hint==18:
            hint=0
        if search_step!=0:
            some_hint[5]=chn('上次搜索结果:'+str(search_step)+'步')
        hint_img.text((15,13),some_hint[hint//3],0x0000ff,font=ziti)
        hint_img.text((0,13),chn('【'),0x0000ff,font=ziti)
        hint_img.text((150,13),chn('】'),0x0000ff,font=ziti)
        bg.blit(hint_img,target=(10,180))
        canvas.blit(bg)
        if isfinish==1:
         appuifw.note(chn("恭喜你成功了"),"info")
         name=appuifw.query(chn("输入名字"),"text")
         try:
           db=e32dbm.open("e:\\System\\Apps\\Puzzle\\picrank.e32dbm","c")
           db[name]=str(step)
           db.close()
           isfinish=0
           appuifw.note(chn("保存成功"),"info")
         except:
           appuifw.note(chn("保存失败"),"error")
         break
        e32.ao_sleep(0.2)
def see_pic():
    global  pic,issee
    issee=1
    appuifw.app.exit_key_handler=play
    see_img=graphics.Image.new(canvas.size)
    while 1:
        see_img.clear(0)
        see_img.blit(pic,target=(5,10))
        see_img.text((20,190),chn("右软键返回游戏"),0x00ff00,font=ziti)
        canvas.blit(see_img)
        e32.ao_yield()
def game():
    load()
    menu()
game()
