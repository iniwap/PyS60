import appuifw,e32,contacts,messaging,flashy,TopWindow,codecs,inbox,logs
import time
from key_codes import *
from graphics import Image
def cn(x):
    return x.decode("utf8")
p=0
xy=[(69,1,110,42),(19,49,60,90),(69,49,110,90),(119,49,160,90),(69,97,110,138)]
def init():    
    canvas.bind(EKeyUpArrow,lambda: move(0,-1))
    canvas.bind(EKeyDownArrow,lambda: move(0,1))
    canvas.bind(EKeySelect,lambda: select())
    canvas.bind(EKeyLeftArrow,lambda: move(-1,0))
    canvas.bind(EKeyRightArrow,lambda: move(1,0))
    model=[cn("定时"),cn("签名"),cn("备份"),cn("自动"),cn("签名"),cn("闪信")]
    for  i in range(5):
        shadow(i,4)
    for i in range(3):
        img.rectangle((i*50+20,50,60+i*50,90),fill=0)
        img.text((i*50+28,72),model[i],fill=0x0000ff)
        img.rectangle((70,2+i*48,110,42+i*48),fill=0)
        img.text((78,24+i*48),model[i+3],fill=0x0000ff)
def move(x,y):
    global p
    if x==1:
        if p==1:
            p=2
        elif p==2:
            p=3
    if x==-1:
        if p==2:
            p=1
        elif p==3:
            p=2
    if y==1:
        if p==0:
            p=2
        elif p==2:
            p=4
    if y==-1:
        if p==4:
            p=2
        elif p==2:
            p=0
def  help():
    global w,img1
    explain=[cn("欢迎使用短信签名测试版"),u"================",cn("功能说明:"),cn("1.可设置自动回复"),cn("2.可设置定时回复"),cn("3.可发送闪信"),cn("4.签名功能可选"),cn("5.具有短信转E功能"),u"================",cn("@小布开发版权所有@")]
    w=TopWindow.TopWindow()
    img1=Image.new((176,208))
    img1.clear(0)
    for i  in range(10):
        img1.text((10,15+i*12),explain[i],fill=0x0000ff)
    w.add_image(img1,(0,0))
    w.size=(160,135)
    w.position=(5,45)
    w.shadow=5
    w.corner_type="corner5"
    w.show()
    e32.ao_sleep(10)
    w.hide()
def selectnum():
    global n
    db=contacts.open()
    names=[]
    numbers=[]
    for i in db:
        names.append(db[i].title)
        num=db[i].find("mobile_number")
        if  num:
            numbers.append(num[0].value)
        else :
            numbers.append(None)
    i=appuifw.selection_list(names)
    n=numbers[i]
def send(flag):
    if  flag==2:
        appuifw.note(cn("只支持英文"),"info")
        c=appuifw.query(cn("请输入英文或者拼音闪信"),"text")
        flashy.flashsms_send(n,c)
    if flag==1:
        f=open('e:\\sign.txt','r')
        sign=f.read()
        sign=sign.decode("utf16")
        f.close()
        messaging.sms_send(n,con+"\n\n\n\n"+cn("签名:")+sign,"UCS2")
    if flag==0:
        messaging.sms_send(n,con,"UCS2")
    if flag==3:
        f=open('e:\\sign.txt','r')
        sign=f.read()
        sign=sign.decode("utf16")
        f.close()
        messaging.sms_send(n,tcon+"\n\n\n\n"+cn("签名:")+sign,"UCS2")
def select():
    global  con,autoc,tcon,tim,dat
    if p==0:
        autoc=appuifw.query(cn("请输入自动回复短信内容："),"text")
        appuifw.note(cn("请开启自动回复"),"info")
    if p==4:
        con=appuifw.query(cn("请输入短信内容"),"text")
    if p==2:
        signcon=appuifw.query(cn("输入签名"),"text")
        signc=signcon.encode("utf16")
        f=open('e:\\sign.txt','w')
        f.write(signc)
        f.close()
    if p==3:
      appuifw.note(cn("备份操作可能会需要一点时间!"),"info")
      if appuifw.query(cn("确认将短信备份到E:/Others/备份.txt？"),"query"):
        box = inbox.Inbox()
        msg=box.sms_messages()
        f=codecs.open('E:/Others/备份.txt', 'w', 'utf8')
        for i in msg:
            f.write(box.address(i))
            f.write('\n')
            f.write(time.ctime(box.time(i)))
            f.write('\n')
            f.write(box.content(i))
            f.write('\n')
        f.close()
        appuifw.note(cn("短信已经转存至E:/Others/备份.txt"),"info")
    if p==1:
        appuifw.note(cn("输入内容和时间后选择发送即可"),"info")
        tcon=appuifw.query(cn("输入短信内容"),"text")
        dat=appuifw.query(cn("输入定时日期"),"date")
        tim=appuifw.query(cn("输入时间"),"time")
def shadow(index,n):
        if index==0:
            for i in range(1,n+1):
                img.rectangle((70+i,2+i,110+i,42+i),outline=(130,130,130))
        if index==1:
            for i in range(1,n+1):
                img.rectangle((20+i,50+i,60+i,90+i),outline=(130,130,130))
        if index==2:
            for i in range(1,n+1):
                img.rectangle((70+i,50+i,110+i,90+i),outline=(130,130,130))
        if index==3:
            for i in range(1,n+1):
                img.rectangle((120+i,50+i,160+i,90+i),outline=(130,130,130))
        if index==4:
            for i in range(1,n+1):
                img.rectangle((70+i,98+i,110+i,138+i),outline=(130,130,130))
auto=0
def autoreply():
    global auto
    auto=1
    autot=logs.sms(mode="in")
    i=inbox.Inbox()
    i_id=i.sms_messages()
    if i.unread(i_id[0]):
        messaging.sms_send(autot[0]["number"],autoc,"UCS2")
        auto=0
def isend():
    send(1)
def nsend():
    send(0)
def fsend():
    send(2)
secl=0.0
def  tsend():
    appuifw.note(cn("请选择联系人"),"info")
    secl=time.time()
    secl-=8*3600
    t=tim+dat-secl
    e32.ao_sleep(t)
    send(3)
def quit():
    global running
    running=0
def handle_redraw(rect):
    canvas.blit(img)
appuifw.app.screen='normal'
img=Image.new((176,208))
canvas=appuifw.Canvas(event_callback=None,redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.title=cn("短信签名秀")
appuifw.app.menu=[(cn("选择号码"),selectnum),(cn("发送"),((cn("发闪信"),fsend),(cn("发定时"),tsend),(cn("使用签名"),isend),(cn("不使用签名"),nsend))),(cn("开启自动回复"),autoreply),(cn("查看帮助"),help)]
appuifw.app.exit_key_handler=quit
running=1
while running:
    img.clear()
    shadow(p,7)
    init()
    img.rectangle(xy[p],outline=0xaaaaaa,width=1)
    if auto==1:
        autoreply()
    handle_redraw(())
    e32.ao_yield()