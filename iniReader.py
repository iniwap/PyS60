#-*-coding: utf8-*-

__version__=2.0
__doc__='iniReader Powered by iniwaper@gmail.com'

import appuifw
import graphics
import e32
import math
import random
import os
import shutil
import time
from key_codes import *
class MenuCanvas:
    def __init__(self,prevcanvas,firststart):
        self.prevCanvas=prevcanvas
        self.menuPage=1
        self.cPosition=0
        if firststart:
            self.isStart=True
            self.firstView=False
            self.softInfo=['i','n','i','R','e','a','d','e','r']
        else:
            self.isStart=False
            self.firstView=True
            self.softInfo=['i','n','i','w','a','p','教','程','系','列']
        self.secondView=False
        self.pencilControl=0
        self.isPencil=True
        self.isEraser=False
        self.lessonExist=True
        self.isHelp=False
        self.canvas=appuifw.Canvas(event_callback=self.choseOne)
        appuifw.app.body=self.canvas
        self.menuList=['课堂教学','课外阅读','复习功课','操作技巧']
        self.softColor=[(255,0,0),(255,153,0),(255,255,0),(0,255,0),(0,204,0),(0,51,255),(255,0,255),(0,255,255),(255,153,255)]
        self.whichCh=[False for i in range(10)]
        self.font=(u"Sans MT 936_S60",16)
        appuifw.app.screen="full"
        self.menuImage=graphics.Image.new((240,320))
        self.menuListImage=graphics.Image.new((200,120))
        self.noteInfoCanvas=graphics.Image.new((160,80))
        self.eraserImage=graphics.Image.new((20,30))
        appuifw.app.exit_key_handler=self.goBack
    def chn(self,x):
        return x.decode('utf8')
    def goBack(self):
        if self.isHelp:
            self.isHelp=False
        else:
            self.menuPage=0
            os.abort()
    def choseOne(self,keycode):
        if self.secondView:
          if keycode["type"]==2:
            if keycode['scancode']==16:
                x='up'
            elif keycode['scancode']==17:
                x='down'
            elif keycode['scancode']==167:
                x="select"
        elif keycode['scancode']==15:
            x='pass'
        if x=='pass':
            self.softInfo=['i','n','i','w','a','p','教','程','系','列']
            self.isPencil=False
            self.isEraser=False
            self.firstView=False
            self.secondView=True
            self.isStart=False
            self.pencilControl=0
            self.createMenuImage()
        else:
            cp=self.cPosition
            self.createMenuList()
            if x=='up':
                self.cPosition-=1
            if x=='down':
                self.cPosition+=1
            if self.cPosition<0 or self.cPosition>3:
                self.cPosition=0
            if x=='select':
                if self.cPosition==0:
                    if not os.path.exists('E:\\iniwaplesson\\2D\\'):
                        self.lessonExist=False
                    else:
                        self.menuPage=0
                        appuifw.app.exit_key_handler=None
                        self.canvas.bind(EKeyUpArrow,lambda:None)
                        self.canvas.bind(EKeyDownArrow,lambda:None)
                        self.canvas.bind(EKeySelect,lambda:None)
                        lr=LessonReader('E:\\iniwaplesson\\2D\\',self.menuImage,True)
                        lr.lessonCanvas()
                elif self.cPosition==1:
                    self.menuPage=0
                    appuifw.app.exit_key_handler=None
                    self.canvas.bind(EKeyUpArrow,lambda:None)
                    self.canvas.bind(EKeyDownArrow,lambda:None)
                    self.canvas.bind(EKeySelect,lambda:None)
                    fm=FileManager(self.menuImage)
                    fm.fileCanvas()
                elif self.cPosition==2:
                    try:
                        f=open('c:\\iniBookMark.bk','r')
                        bk=f.read().split('#')
                        bkdir=bk[0]
                        bklesson=int(bk[1])
                        bkpage=int(bk[2])
                        f.close()
                        self.menuPage=0
                        appuifw.app.exit_key_handler=None
                        self.canvas.bind(EKeyUpArrow,lambda:None)
                        self.canvas.bind(EKeyDownArrow,lambda:None)
                        self.canvas.bind(EKeySelect,lambda:None)
                        lr=LessonReader(bkdir,self.menuImage,True,bklesson,bkpage)
                        lr.lessonCanvas()
                    except:
                        if not os.path.exists('E:\\iniwaplesson\\2D\\'):
                            self.lessonExist=False
                        else:
                            self.menuPage=0
                            appuifw.app.exit_key_handler=None
                            self.canvas.bind(EKeyUpArrow,lambda:None)
                            self.canvas.bind(EKeyDownArrow,lambda:None)
                            self.canvas.bind(EKeySelect,lambda:None)
                            lr=LessonReader('E:\\iniwaplesson\\2D\\',self.menuImage,True)
                            lr.lessonCanvas()
                elif self.cPosition==3:
                    self.isHelp=True
    def createEraser(self):
        coloroffset=0
        self.eraserImage.clear((200,200,200))
        for i in range(15):
            coloroffset+=4
            self.eraserImage.rectangle((i*2/3,i,20-i*2/3,30-i),(200-3*coloroffset,200-3*coloroffset,200-3*coloroffset))
    def createNoteInfoImage(self,noteBar,noteContr,noteSize=(160,80)):
        w=noteSize[0]
        h=noteSize[1]
        self.noteInfoCanvas.clear((200,200,200))
        self.noteInfoCanvas.rectangle((w/2-1+noteBar,h/2-1+noteBar/2,w/2-1-noteBar,h/2-1-noteBar/2),outline=0,width=2)
        
        self.noteInfoCanvas.text((8,22),self.chn('E:\\iniwaplesson\\2D\\'),font=self.font)
        self.noteInfoCanvas.text((8,38),self.chn('无教程存在,请到'),font=self.font)
        self.noteInfoCanvas.text((8,54),self.chn('iniwap.cn下载'),font=self.font)
        self.menuImage.blit(self.noteInfoCanvas,target=((240-w/4)/2+noteBar,(320-h/4)/2+noteBar/2+20),source=(w/2+noteBar,h/2+noteBar/2,w/2-noteBar,h/2-noteBar/2))
    def createMenuImage(self):
        if self.isStart:
            self.menuImage.clear((0,0,0))
            for i in range(9):
                if self.whichCh[i]:
                    self.menuImage.text((70+i*12,160),self.chn(self.softInfo[i]),self.softColor[i],font=(u"Sans MT 936_S60",24,graphics.FONT_BOLD))
        if not self.isStart:
            self.menuImage.clear((200,200,200))
            coloroffset=0
            for i in range(10):
                coloroffset+=4
                self.menuImage.rectangle((15+i,40+i,225-i,120-i),outline=(4*coloroffset+20,50+4*coloroffset,4*coloroffset))
                self.menuImage.line((5,119-i,15,119-i),(4*coloroffset+20,50+4*coloroffset,4*coloroffset))
                self.menuImage.line((225,119-i,235,119-i),(4*coloroffset+20,50+4*coloroffset,4*coloroffset))
                
                self.menuImage.line((70,295-i,170,295-i),(5*coloroffset,5*coloroffset,5*coloroffset))
                self.menuImage.line((90+i,295,90+i,315),(5*coloroffset,5*coloroffset,5*coloroffset))
                self.menuImage.line((150-i,295,150-i,315),(5*coloroffset,5*coloroffset,5*coloroffset))
                if i<5:
                    self.menuImage.line((90,220+i,150,220+i),(5*coloroffset+50,5*coloroffset+50,5*coloroffset+50))
                    self.menuImage.line((85+i,220,85+i,270),(5*coloroffset+50,5*coloroffset+50,5*coloroffset+50))
                    self.menuImage.line((154-i,220,154-i,270),(5*coloroffset+50,5*coloroffset+50,5*coloroffset+50))
                    self.menuImage.line((90,265+i,110,265+i),(5*coloroffset+50,5*coloroffset+50,5*coloroffset+50))
                    self.menuImage.line((130,265+i,150,265+i),(5*coloroffset+50,5*coloroffset+50,5*coloroffset+50))
                    
                    self.menuImage.line((110+i,265,110+i,285),(5*coloroffset,5*coloroffset,5*coloroffset))
                    self.menuImage.line((130-i,265,130-i,285),(5*coloroffset,5*coloroffset,5*coloroffset))

                    self.menuImage.line((115+i,260,90+i,280),(5*coloroffset,5*coloroffset,5*coloroffset))
                    self.menuImage.line((125-i,260,150-i,280),(5*coloroffset,5*coloroffset,5*coloroffset))
                    self.menuImage.line((110+i,295,100+i,310),(5*coloroffset,5*coloroffset,5*coloroffset))
                    self.menuImage.line((130-i,295,140-i,310),(5*coloroffset,5*coloroffset,5*coloroffset))
            self.menuImage.point((120,250),outline=0,fill=0,width=30)
        if self.firstView:
            xoffset=self.pencilControl%5-5
            self.menuImage.text((50,30),self.chn('好好学习 天天向上'),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
            if self.isPencil:
                self.menuImage.polygon(((30+self.pencilControl,74-xoffset),(54+self.pencilControl,50-xoffset),(60+self.pencilControl,56-xoffset),(36+self.pencilControl,80-xoffset),(30+self.pencilControl,80-xoffset)),outline=0,width=2,fill=(255,51,0))
                self.menuImage.line((30+self.pencilControl,74-xoffset,36+self.pencilControl,80-xoffset),0,width=2)
                self.menuImage.line((56+self.pencilControl,52-xoffset,32+self.pencilControl,76-xoffset),0)
                self.menuImage.line((58+self.pencilControl,54-xoffset,34+self.pencilControl,78-xoffset),0)
            for i in range(int(self.pencilControl/14)):
                self.menuImage.text((30+14*i,90),self.chn(self.softInfo[i]),self.softColor[i%9],font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
    def createMenuList(self):
        coloroffset=0
        self.menuListImage.clear((255,255,255))
        for i in range(5):
            coloroffset+=4
            self.menuListImage.rectangle((i,i,200-i,120-i),(5*coloroffset,5*coloroffset,5*coloroffset))
        if self.isHelp:
            self.menuListImage.text((5,40),self.chn('导航键切换目录，移动光'),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
            self.menuListImage.text((5,60),self.chn('标，翻页，选择。另导航'),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
            self.menuListImage.text((5,80),self.chn('键左收回菜单，左软键弹'),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
            self.menuListImage.text((5,100),self.chn('出菜单，右软键键返回'),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
        else:
            coloroffset=0
            for i in range(16):
                coloroffset+=4
                self.menuListImage.line((30,self.cPosition*20+i+16,170,self.cPosition*20+i+16),(3*coloroffset+50,3*coloroffset+50,3*coloroffset+50))
            for i in range(4):
                self.menuListImage.text((60,30+20*i),self.chn(self.menuList[i]),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
    def menuCanvas(self):
        speed=0.0
        gravity=0.03
        currentposition=0
        currentpositionch=[0 for i in range(9)]
        speedch=[random.random()*2 for i in range(9)]
        whichch=0
        noteBar=0
        noteContr=-1
        self.createEraser()
        while self.menuPage:
            if self.isStart:
                self.createMenuImage()
                if whichch<9:
                    for i in range(9):
                        if not self.whichCh[i]:
                            self.menuImage.text((70+i*12,currentpositionch[i]),self.chn(self.softInfo[i]),self.softColor[i],font=(u"Sans MT 936_S60",24,graphics.FONT_BOLD))
                            speedch[i]*=0.999
                            sd1=speedch[i]
                            speedch[i]+=gravity
                            sd2=speedch[i]
                            currentpositionch[i]+=speedch[i]
                            if currentpositionch[i]>160:
                                currentpositionch[i]=160-(currentpositionch[i]-160)
                                speedch[i]=-0.70*speedch[i]
                            if sd1*sd2<=0.0 and abs(currentpositionch[i]-160)<1:
                                if not self.whichCh[i]:
                                    whichch+=1
                                self.whichCh[i]=True
                else:
                    currentposition+=1
                    self.menuImage.text((180,140),self.chn('®'),(250,0,0),font=self.font)
                    self.menuImage.line((120,160,120-currentposition,160),(200,200,200),width=4)
                    self.menuImage.line((120,160,120+currentposition,160),(200,200,200),width=4)
                    self.menuImage.text((-20+currentposition,180),self.chn('PyS60开源社区'),(200,200,200),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
                    self.menuImage.text((220-currentposition,200),self.chn('iniwap.cn'),(200,200,200),font=(u"Sans MT 936_S60",16,graphics.FONT_BOLD))
                    if currentposition>100:
                        currentposition=0
                        speed=0.0
                        e32.ao_sleep(2)
                        self.softInfo=['i','n','i','w','a','p','教','程','系','列']
                        self.prevCanvas=None
                        self.isStart=False
                        self.firstView=True
            if self.firstView:
                self.createMenuImage()
                if self.isPencil:
                    self.pencilControl+=1
                    if self.pencilControl>145:
                        self.pencilControl=145
                        self.isPencil=False
                        self.isEraser=True
                        e32.ao_sleep(1)
                if self.isEraser:
                    self.pencilControl-=1
                    self.menuImage.blit(self.eraserImage,target=(self.pencilControl+30,68))
                    if self.pencilControl<0:
                        self.isPencil=False
                        self.isEraser=False
                        self.firstView=False
                        self.secondView=True
                        self.pencilControl=0
            if self.secondView:
                self.createMenuList()
                if not self.lessonExist:
                    noteBar+=4*noteContr
                    self.createNoteInfoImage(noteBar,noteContr,noteSize=(160,80))
                    if noteBar==-80:
                        e32.ao_sleep(4)
                        noteContr=-1
                        self.lessonExist=True
                        self.firstView=True
                        self.isPencil=True
                        self.secondView=False
                        noteBar=0
                speed*=0.99
                speed+=gravity
                currentposition+=speed
                if currentposition>120:
                    currentposition=120-(currentposition-120)
                    speed=-0.80*speed
                if abs(speed)<0.001:
                    currentposition=120
                self.menuImage.blit(self.menuListImage,target=(20,0),source=(0,120-currentposition,200,120))
                
            self.canvas.blit(self.menuImage)
            e32.ao_yield()
class LessonReader:
    def __init__(self,whichDirPath,prevcanvas,isreadlesson,lessonindex=1,currentpage=1):
        self.firstRead=True
        self.lessonReader=1
        self.isReadLesson=isreadlesson
        self.currentPage=currentpage
        self.backGroundColor=[1,1,1]
        self.lastPageLen=0
        self.isPrevNext=False
        self.lessonIndex=lessonindex
        self.isMenuInfo=False
        self.isFirstPage=True
        self.isLastPage=False
        self.labelBackFront=1
        self.isNoPrev=False
        self.isNoNext=False
        self.noteInfo=""
        self.whichDirPath=whichDirPath
        self.prevCanvas=prevcanvas
        self.pageInfo=[self.chn("上一页"),self.chn("下一页")]

        self.isMenuCreate=False
        self.cPosition=0
        self.menuControl=1
        self.menuSize=(70,80)
        self.menuList=['运行源码','添加书签','阅读其他','返回主单']
        self.menuImage=graphics.Image.new(self.menuSize)
        self.isBookMark=False
        self.isSeeCode=False
        self.haveCode=False
        
        self.canvas=appuifw.Canvas(event_callback=self.keyEvents)
        appuifw.app.body=self.canvas
        appuifw.app.screen="full"
        self.canvas.blit(self.prevCanvas)
        self.currentLesson=graphics.Image.new(self.canvas.size)
        self.prevNextLesson=graphics.Image.new(self.canvas.size)
        self.noteInfoCanvas=graphics.Image.new((64,32))
        appuifw.app.exit_key_handler=self.viewBack
        self.font=(u"Sans MT 936_S60",12)
        if self.isReadLesson:
            self.currentPath=self.whichDirPath+self.chn(str(self.lessonIndex))+".txt"
            self.totalLesson=len(os.listdir(self.whichDirPath))
        else:
            self.currentPath=self.whichDirPath
            self.totalLesson=1
        f=open(self.currentPath,"r")
        self.currentTxt=(self.chn(f.read())).split("\r\n")
        self.lessonTitle=self.currentTxt[0]
        f.close()
        self.prevNextTxt=""
        self.totalLine=len(self.currentTxt)
        self.totalPage=0
        self.currentTxt=self.howManyPage(self.currentTxt)

    def chn(self,x):
        return x.decode('utf8')
    def dchn(self,x):
        return x.encode('utf8')
    def keyEvents(self,keycode):
      if keycode["type"]==2:
        if keycode['scancode']==16:
            x='pageback'
        elif keycode['scancode']==17:
            x='pageup'
        elif keycode['scancode']==14:
            x='prevlesson'
        elif keycode['scancode']==15:
            x='nextlesson'
        elif keycode['scancode']==167:
            x='menuselect'
        elif  keycode['scancode']==164:
            x='menupage'
        elif keycode['scancode']==49:
            x='color'
        if self.isMenuCreate:
            if x=='pageback':
                self.cPosition-=1
            if x=='pageup':
                self.cPosition+=1
            if self.cPosition<0 or self.cPosition>len(self.menuList)-1:
                self.cPosition=0
            if x=='prevlesson':#取消
                self.menuControl=-1
            if x=='menuselect':
                self.menuControl=-1
                if self.cPosition==0:
                    self.seeCode()
                elif self.cPosition==1:
                    self.bookMark()
                elif self.cPosition==2:
                    self.viewOther()
                elif self.cPosition==3:
                    self.viewBack()
                
        else:
            cp=self.currentPage
            if x=="pageback":
                self.currentPage-=1
            elif x=="pageup":
                self.currentPage+=1
            elif x=="color":
                self.backGroundColor=[random.randint(0,1),random.randint(0,1),random.randint(0,1)]
                if self.backGroundColor==[0,0,0]:
                    self.backGroundColor=[1,1,1]
            if self.currentPage>self.totalPage or self.currentPage<1:
                self.currentPage=cp
            if self.currentPage==1:
                self.isFirstPage=True
            elif self.currentPage==self.totalPage:
                self.isLastPage=True
            else:
                if self.totalPage==1:
                    self.isFirstPage=True
                    self.isLastPage=True
                else:
                    self.isFirstPage=False
                    self.isLastPage=False
            if x=="prevlesson":
                if self.isFirstPage or self.totalPage==1:
                    if self.lessonIndex>1:
                        self.labelBackFront=-1
                        self.lessonIndex-=1
                        self.isPrevNext=True
                    else:
                        self.isNoPrev=True
                        self.noteInfo=self.chn("已是首页")
            if x=="nextlesson":
                if self.isLastPage or self.totalPage==1:
                    if self.lessonIndex<self.totalLesson:
                        self.labelBackFront=1
                        self.lessonIndex+=1
                        self.isPrevNext=True
                    else:
                        self.isNoNext=True
                        self.noteInfo=self.chn("已是尾页")
            if x=="menupage":
                self.isMenuCreate=True
            #MenuInfo类用于其中的操作，如执行代码，返回主单，添加书签，快速翻页
            self.howManyLines()
            if self.isPrevNext:
                self.currentPage=1
                f=open(self.whichDirPath+self.chn(str(self.lessonIndex))+".txt","r")
                self.prevNextTxt=(self.chn(f.read())).split("\r\n")
                self.lessonTitle=self.prevNextTxt[0]
                f.close()
                
                self.totalLine=len(self.prevNextTxt)
                self.totalPage=0
                self.prevNextTxt=self.howManyPage(self.prevNextTxt)
                self.prevNextLesson=self.createImage(self.prevNextTxt)
            else:
                self.currentLesson=self.createImage(self.currentTxt)
    def bookMark(self):
        self.isBookMark=True
        try:
            f=open('C:\\iniBookMark.bk','w')#主程序文件夹下
            f.write(self.whichDirPath)
            f.write('#')
            f.write(str(self.lessonIndex))
            f.write('#')
            f.write(str(self.currentPage))
            f.close()
            self.noteInfo=self.chn("书签已存")
        except:
            self.noteInfo=self.chn("保存失败")
    def viewOther(self):
        self.lessonReader=0
        appuifw.app.exit_key_handler=None
        self.canvas.bind(EKeyUpArrow,lambda:None)
        self.canvas.bind(EKeyDownArrow,lambda:None)
        self.canvas.bind(EKeyLeftArrow,lambda:None)
        self.canvas.bind(EKeyRightArrow,lambda:None)
        self.canvas.bind(EKeySelect,lambda:None)
        self.canvas.bind(EKeyLeftSoftkey,lambda:None)
        fm=FileManager(self.currentLesson)
        fm.fileCanvas()
    def seeCode(self):
        self.isSeeCode=True
        if os.path.exists(self.whichDirPath+self.chn(str(self.lessonIndex))+"_s.py"):
            self.haveCode=True
            self.noteInfo=self.chn("返回键退出")
            self.noteInfoCanvas=graphics.Image.new((80,40))
        else:
            self.noteInfo=self.chn("本节无源码")
            self.noteInfoCanvas=graphics.Image.new((80,40))
            self.haveCode=False
    def viewBack(self):
        self.lessonReader=0
        appuifw.app.exit_key_handler=None
        self.canvas.bind(EKeyUpArrow,lambda:None)
        self.canvas.bind(EKeyDownArrow,lambda:None)
        self.canvas.bind(EKeyLeftArrow,lambda:None)
        self.canvas.bind(EKeyRightArrow,lambda:None)
        self.canvas.bind(EKeySelect,lambda:None)
        self.canvas.bind(EKeyLeftSoftkey,lambda:None)
        mc=MenuCanvas(self.currentLesson,False)
        mc.menuCanvas()
    def howManyLines(self):
        if self.currentPage<self.totalPage:
            self.lastPageLen=13
        else:
            self.lastPageLen=self.totalLine-(self.currentPage-1)*13
    def howManyPage(self,content):
        tmpc=content
        tmp=len(tmpc)
        i=0
        while i<tmp:
            lens=self.currentLesson.measure_text(tmpc[i],self.font,maxwidth=230)[2]
            if lens<len(tmpc[i]):
                self.totalLine+=1
                tmp+=1
                tmpc.insert(i,tmpc[i][:lens+1])
                tmpc[i+1]=tmpc[i+1][lens+1:]
            i+=1
        if self.totalLine%13!=0:
            self.totalPage=1+self.totalLine/13
        else:
            self.totalPage=self.totalLine/13
        self.howManyLines()
        return tmpc
    def createNoteInfoImage(self,noteBar,noteContr,noteSize=(64,32)):
        w=noteSize[0]
        h=noteSize[1]
        self.noteInfoCanvas.clear((200,200,200))
        self.noteInfoCanvas.rectangle((w/2-1+noteBar,h/2-1+noteBar/2,w/2-1-noteBar,h/2-1-noteBar/2),outline=0,width=2)
        self.noteInfoCanvas.text((8,22),self.noteInfo,font=self.font)
        self.currentLesson.blit(self.noteInfoCanvas,target=((240-w/2)/2+noteBar,(320-h/2)/2+noteBar/2),source=(w/2+noteBar,h/2+noteBar/2,w/2-noteBar,h/2-noteBar/2))
    def createImage(self,contentTxt):
        contentImage=graphics.Image.new(self.canvas.size)
        contentImage.clear((200*self.backGroundColor[0],200*self.backGroundColor[1],200*self.backGroundColor[2]))
        dcolor=0
        ddcolor=45
        for i in range(25):
            contentImage.line((0,i,240,i),(dcolor*self.backGroundColor[0],dcolor*self.backGroundColor[1],dcolor*self.backGroundColor[2]))
            dcolor+=4
            contentImage.line((5,ddcolor,240,ddcolor),(110*self.backGroundColor[0],110*self.backGroundColor[1],110*self.backGroundColor[2]))
            if ddcolor<280:
              ddcolor+=20
        contentImage.text((4,18),self.lessonTitle,(200*self.backGroundColor[0],200*self.backGroundColor[1],200*self.backGroundColor[2]),self.font)
        for i in range(self.lastPageLen):
            contentImage.text((4,44+20*i),self.chn(self.dchn(contentTxt[i+13*(self.currentPage-1)])),font=self.font)
        for i in range(len(self.pageInfo)):
            contentImage.text((5+i*190,310),self.pageInfo[i],(110*self.backGroundColor[0],110*self.backGroundColor[1],110*self.backGroundColor[2]),self.font)
        contentImage.text((95,310),self.chn(str(self.currentPage)+"/"+str(self.totalPage)),(110*self.backGroundColor[0],110*self.backGroundColor[1],110*self.backGroundColor[2]),self.font)
        return contentImage
    def lessonCanvas(self):
        self.currentLesson=self.createImage(self.currentTxt)
        newLesson=1
        noteBar=0
        noteContr=-1
        speed=0.0
        gravity=0.03
        currentposition=0
        menuBar=0
        while self.lessonReader:
            if self.isMenuCreate:
                self.currentLesson=self.createImage(self.currentTxt)
                dcolor=50
                menuBar+=2*self.menuControl
                #书签保存提示
                if self.menuControl==-1 and self.isBookMark:
                    noteBar+=4*noteContr
                    self.createNoteInfoImage(noteBar,noteContr)
                    if noteBar==-32:
                        e32.ao_sleep(1)
                        noteContr=1
                    if noteBar==0:
                        noteContr=-1
                        noteBar=0
                        self.isBookMark=False
                #源码运行提示
                if self.menuControl==-1 and self.isSeeCode:
                    noteBar+=4*noteContr
                    self.createNoteInfoImage(noteBar,noteContr,(80,40))
                    if noteBar==-40:
                        e32.ao_sleep(1)
                        noteContr=1
                    if noteBar==0:
                        noteContr=-1
                        noteBar=0
                        self.isSeeCode=False
                        if self.haveCode:
                            prevBody=appuifw.app.body
                            prevExit=appuifw.app.exit_key_handler
                            execfile(self.whichDirPath+self.chn(str(self.lessonIndex))+"_s.py", globals())
                            appuifw.app.body=prevBody
                            appuifw.app.exit_key_handler=prevExit
                #菜单显示动画
                if menuBar<0:
                    self.isMenuCreate=False
                    self.menuControl=1
                if menuBar>self.menuSize[0]:
                    menuBar=self.menuSize[0]
                self.menuImage.clear((200,200,200))
                self.menuImage.rectangle((-1,-1,self.menuSize[0]-1,self.menuSize[1]-1),outline=0,width=2)
                for i in range(20):
                    self.menuImage.line((0,self.cPosition*20+i,self.menuSize[0]-2,self.cPosition*20+i),(2*dcolor,2*dcolor,2*dcolor))
                    dcolor+=4
                for i in range(len(self.menuList)):
                    self.menuImage.text((2,i*20+16),self.chn(self.menuList[i]),font=self.font)
                self.currentLesson.blit(self.menuImage,target=(-self.menuSize[0]+menuBar,319-menuBar*self.menuSize[1]/self.menuSize[0]))
            else:
                if self.isNoPrev or self.isNoNext:
                    self.currentLesson=self.createImage(self.currentTxt)
                    noteBar+=4*noteContr
                    self.createNoteInfoImage(noteBar,noteContr)
                    if noteBar==-32:
                        e32.ao_sleep(1)
                        noteContr=1
                    if noteBar==0:
                        noteContr=-1
                        self.isNoPrev=False
                        self.isNoNext=False
                elif self.isPrevNext:
                    newLesson+=2
                    self.currentLesson.blit(self.prevNextLesson,target=(self.labelBackFront*(240-newLesson),0))
                    if newLesson>240:
                        self.isPrevNext=False
                        self.isFirstPage=True
                        self.isLastPage=False
                        self.currentTxt=self.prevNextTxt
                        self.currentLesson=self.prevNextLesson
                        newLesson=1
                elif self.firstRead:
                    speed*=0.99
                    speed+=gravity
                    currentposition+=speed
                    if currentposition>320:
                        currentposition=320-(currentposition-320)
                        speed=-0.80*speed
                    if abs(speed)<0.003:
                        self.firstRead=False
                        self.prevCanvas=None
            
            if self.prevCanvas:
                self.prevCanvas.blit(self.currentLesson,target=(0,0),source=(0,320-currentposition,240,320))
                self.canvas.blit(self.prevCanvas)
            else:
                self.canvas.blit(self.currentLesson,target=(0,0),source=(0,320-currentposition,240,320))
            e32.ao_yield()
class FileManager:
    def __init__(self,prevcanvas):
        self.dir_stack=[]
        self.__path__=self.chn(' C:\\')
        self.current_dir=['C',"D",'E',"Z"]
        self.fileManager=1
        self.index=0
        self.isOverBorder=False
        self.borderSize=17
        self.font=(u"Sans MT 936_S60",16)
        self.startIndex=0
        self.endIndex=4
        self.barLen=70
        self.markDir=4
        self.firstIn=True

        self.isMenuCreate=False
        self.cPosition=0
        self.menuControl=1
        self.menuSize=(70,80)
        self.menuList=['复制','删除','详情','添加阅读']
        self.isCopy=False
        self.isViewDetail=False
        self.selectPath=''
        self.ctime=''
        self.mtime=''
        self.size=''
        self.menuImage=graphics.Image.new(self.menuSize)
        
        self.prevCanvas=prevcanvas
        self.canvas=appuifw.Canvas(event_callback=self.updateDir)
        appuifw.app.body=self.canvas
        appuifw.app.screen="full"
        self.fileImage=graphics.Image.new(self.canvas.size)
        self.noteInfoCanvas=graphics.Image.new((160,80))
        self.canvas.blit(self.prevCanvas)
        appuifw.app.exit_key_handler=self.viewBack
    def chn(self,x):
        return x.decode('utf8')
    def rn(self,x):
        return x.encode('utf8')
    def viewBack(self):
        self.fileManager=0
        appuifw.app.exit_key_handler=None
        self.canvas.bind(EKeyUpArrow,lambda:None)
        self.canvas.bind(EKeyDownArrow,lambda:None)
        self.canvas.bind(EKeyLeftArrow,lambda:None)
        self.canvas.bind(EKeyRightArrow,lambda:None)
        self.canvas.bind(EKeySelect,lambda:None)
        self.canvas.bind(EKeyLeftSoftkey,lambda:None)
        mc=MenuCanvas(self.fileImage,False)
        mc.menuCanvas()
    def copy(self,path):
        self.isCopy=False
        shutil.copyfile(self.selectPath,path+os.path.split(self.selectPath)[1])
    def delete(self):
        os.remove(self.selectPath)
    def add(self):
        if not os.path.exists('C:\\iniReader\\'):
            os.mkdir('C:\\iniReader\\')
        shutil.copyfile(self.selectPath,'C:\\iniReader\\'+os.path.split(self.selectPath)[1])
    def view(self):
        self.isViewDetail=True
        self.ctime=time.strftime('%Y-%m-%d',time.localtime(os.path.getatime(self.selectPath)))
        self.mtime=time.strftime('%Y-%m-%d',time.localtime(os.path.getmtime(self.selectPath)))
        self.size=str(os.path.getsize(self.selectPath)/1024.0)[:4]
    def getBar(self):
        if self.index>13:
            self.startIndex=self.index-13
            self.endIndex=self.index+1
        else:
            if len(self.current_dir)>13:
                self.startIndex=0
                self.endIndex=14
            else:
                self.startIndex=0
                self.endIndex=len(self.current_dir)
        self.barLen=280.0/len(self.current_dir)
    def join_path(self,current_path):
        return current_path[0]+':\\'+'\\'.join(current_path[1:])
    def list_dir(self,path_stack):
        path=self.join_path(path_stack)
        markdir=0
        markfile=0
        for dir_list in os.listdir(path):
            if os.path.isdir(path+'\\'+dir_list):
                self.current_dir.insert(markdir,dir_list)
                markdir+=1
            elif dir_list.find('.txt')!=-1 or dir_list.find('.py')!=-1:
                self.current_dir.insert(markdir+markfile,dir_list)
                markfile+=1
        self.markDir=markdir
    def updateDir(self,keycode):
      if keycode["type"]==2:
        if keycode['scancode']==16:
            i="upfile"
        elif keycode['scancode']==17:
            i="downfile"
        elif keycode['scancode']==14:
            i="prevdir"
        elif keycode['scancode']==15:
            i="nextdir"
        elif keycode['scancode']==167:
            i="selectfile"
        elif  keycode['scancode']==164:
            i="managefile"
        tmpIndex=self.index
        if self.isMenuCreate:
            cp=self.cPosition
            if i=='upfile':
                self.cPosition-=1
            if i=='downfile':
                self.cPosition+=1
            if self.cPosition<0 or self.cPosition>len(self.menuList)-1:
                self.cPosition=0
            if i=='prevdir':
                self.menuControl=-1
            if i=='selectfile':
              if len(self.dir_stack)!=0:
                self.tmpDir_stack=[self.chn(s) for s in self.dir_stack]
                self.selectPath=os.path.join(self.join_path(self.tmpDir_stack),self.chn(self.current_dir[self.index]))
                if os.path.isfile(self.selectPath):
                    self.menuControl=-1
                    if self.cPosition==0:
                        self.isCopy=True
                    elif self.cPosition==1:
                        self.delete()
                    elif self.cPosition==2:
                        self.view()
                    elif self.cPosition==3:
                        self.add()                                      
        else:
            if i=='upfile':
                self.index-=1
            if i=='downfile':
                self.index+=1
            if self.index>len(self.current_dir)-1 or self.index<0:
                self.index=tmpIndex    
            if len(self.dir_stack)==0 and i=='nextdir':
                self.dir_stack.append(self.current_dir[self.index])
                self.current_dir=[]
                self.list_dir(self.dir_stack)
                self.index=0
            elif i=='prevdir':
                if len(self.dir_stack)>0:
                    tmp=self.dir_stack.pop()
                    if len(self.dir_stack)==0:
                        self.current_dir=['C',"D",'E',"Z"]
                    else:
                        self.current_dir=[]
                        self.list_dir(self.dir_stack)
                        
                self.index=self.current_dir.index(tmp)
            elif  i=='nextdir' and os.path.isdir(self.join_path(self.dir_stack)+'\\'+self.current_dir[self.index]) and self.current_dir[self.index]!='z:':
                self.dir_stack.append(self.rn(self.chn(self.current_dir[self.index])))
                self.current_dir=[]
                self.list_dir(self.dir_stack)
                if len(self.current_dir)==0:
                    self.current_dir=['空文件夹']
                self.index=0
            elif i=='selectfile':
                if len(self.dir_stack)!=0:
                    self.__path__=os.path.join(self.join_path(self.dir_stack),self.current_dir[self.index]+"\\")
                    if os.path.isdir(self.__path__):
                        if self.isCopy:
                            self.copy(self.__path__)
                        elif self.dir_stack[-1]==self.chn('iniwaplesson'):
                            LessonReader(self.__path__,self.fileImage,True).lessonCanvas()
                    else: #os.path.isfile(os.path.join(self.join_path(self.dir_stack),self.current_dir[self.index])):
                        LessonReader(os.path.join(self.join_path(self.dir_stack),self.current_dir[self.index]),self.fileImage,False).lessonCanvas()
                    #执行选择操作
            elif i=='managefile':
                self.isMenuCreate=True
            if len(self.dir_stack)!=0:
                self.tmpDir_stack=[self.chn(s) for s in self.dir_stack]
                self.__path__=os.path.join(self.join_path(self.tmpDir_stack),self.chn(self.current_dir[self.index]))
            else:
                self.__path__=self.chn(self.current_dir[self.index]+':\\')
            self.judgeBorder(self.__path__)
            self.getBar()
            self.createFileImage()
    def judgeBorder(self,text):
        self.borderSize=self.fileImage.measure_text(text,self.font,maxwidth=208)[2]
        if self.borderSize<len(text):
            self.isOverBorder=True
        else:
            self.isOverBorder=False
    def createNoteInfoImage(self,noteBar,noteContr,noteSize=(160,80)):
        w=noteSize[0]
        h=noteSize[1]
        self.noteInfoCanvas.clear((200,200,200))
        self.noteInfoCanvas.rectangle((w/2-1+noteBar,h/2-1+noteBar/2,w/2-1-noteBar,h/2-1-noteBar/2),outline=0,width=2)
        
        self.noteInfoCanvas.text((8,22),self.chn('最后访问:'+self.ctime),font=self.font)
        self.noteInfoCanvas.text((8,38),self.chn('最后修改:'+self.mtime),font=self.font)
        self.noteInfoCanvas.text((8,54),self.chn('文件大小:'+self.size+'K'),font=self.font)
        
        self.fileImage.blit(self.noteInfoCanvas,target=((240-w/4)/2+noteBar,(320-h/4)/2+noteBar/2),source=(w/2+noteBar,h/2+noteBar/2,w/2-noteBar,h/2-noteBar/2))
    def createFileImage(self):
        self.fileImage.clear((200,200,200))
        dcolor=0
        ddcolor=45
        for i in range(25):
            self.fileImage.line((0,i,240,i),(dcolor,dcolor,dcolor))
            self.fileImage.line((226+i/2,24+self.index*self.barLen,226+i/2,24+self.index*self.barLen+self.barLen),(dcolor*2,dcolor*2,dcolor*2))
            if i<21:
                if self.index<14:
                    self.fileImage.line((0,44-i+self.index*20,224,44-i+self.index*20),(dcolor+50,dcolor+50,dcolor+50))
                else:
                    self.fileImage.line((0,304-i,224,304-i),(dcolor+50,dcolor+50,dcolor+50))
            dcolor+=4
            self.fileImage.line((0,ddcolor,224,ddcolor),(110,110,110))
            if ddcolor<300:
                ddcolor+=20
        if self.isOverBorder:
            self.fileImage.text((0,18),self.__path__[:self.borderSize]+self.chn('…'),(110,110,110),font=self.font)
        else:
            self.fileImage.text((0,18),self.__path__,(110,110,110),font=self.font)
        for i in range(self.startIndex,self.endIndex):
            b=self.fileImage.measure_text(self.chn(self.current_dir[i]),self.font,maxwidth=208)[2]
            if i<self.markDir:
                if len(self.chn(self.current_dir[i]))>b:
                    self.fileImage.text((0,44+20*(i-self.startIndex)),self.chn(self.current_dir[i])[:b]+self.chn('...>>'),font=self.font)
                else:
                    self.fileImage.text((0,44+20*(i-self.startIndex)),self.chn(self.current_dir[i]+'>>'),font=self.font)
            else:
                if len(self.chn(self.current_dir[i]))>b:
                    self.fileImage.text((0,44+20*(i-self.startIndex)),self.chn(self.current_dir[i])[:b]+self.chn('...'),font=self.font)
                else:
                    self.fileImage.text((0,44+20*(i-self.startIndex)),self.chn(self.current_dir[i]),font=self.font)
        self.fileImage.rectangle((225,24,239,307),(110,110,110))
    def fileCanvas(self):
        speed=0.0
        gravity=0.03
        currentposition=0
        menuBar=0
        noteBar=0
        noteContr=-1
        self.createFileImage()
        while self.fileManager:
            if self.isMenuCreate:
                if self.menuControl==-1:
                    self.createFileImage()
                dcolor=50
                menuBar+=2*self.menuControl
                if self.menuControl<0 and self.isViewDetail:
                    noteBar+=4*noteContr
                    self.createNoteInfoImage(noteBar,noteContr,noteSize=(160,80))
                    if noteBar==-80:
                        e32.ao_sleep(4)
                        noteContr=1
                    if noteBar==0:
                        noteContr=-1
                        noteBar=0
                        self.isViewDetail=False
                        self.isMenuCreate=False
                        self.menuControl=1
                if menuBar<0 and not self.isViewDetail:
                    self.isMenuCreate=False
                    self.menuControl=1
                if menuBar>self.menuSize[0]:
                    menuBar=self.menuSize[0]
                self.menuImage.clear((200,200,200))
                self.menuImage.rectangle((-1,-1,self.menuSize[0]-1,self.menuSize[1]-1),outline=0,width=2)
                for i in range(20):
                    self.menuImage.line((0,self.cPosition*20+i,self.menuSize[0]-2,self.cPosition*20+i),(2*dcolor,2*dcolor,2*dcolor))
                    dcolor+=4
                for i in range(len(self.menuList)):
                    self.menuImage.text((2,i*20+16),self.chn(self.menuList[i]),font=self.font)
                self.fileImage.blit(self.menuImage,target=(-self.menuSize[0]+menuBar,319-menuBar*self.menuSize[1]/self.menuSize[0]))
            else:
                if self.firstIn:
                    speed*=0.99
                    speed+=gravity
                    currentposition+=speed
                    if currentposition>320:
                        currentposition=320-(currentposition-320)
                        speed=-0.80*speed
                        if abs(speed)<0.003:
                            self.firstIn=False
                            self.prevCanvas=None

            if self.prevCanvas:
                self.prevCanvas.blit(self.fileImage,target=(0,0),source=(0,320-currentposition,240,320))
                self.canvas.blit(self.prevCanvas)
            else:
                self.canvas.blit(self.fileImage,target=(0,0),source=(0,320-currentposition,240,320))
            e32.ao_yield()
MenuCanvas(None,True).menuCanvas()