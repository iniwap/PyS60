#-*-coding:utf8-*-
import os,shutil,appuifw,graphics,e32,socket,thread,time
from key_codes import *
try:
    if not os.path.exists("c:\\Resource\\iniIME.py"):
        shutil.copyfile("e:\\ChineseCharacter\\iniIME.py","c:\\Resource\\iniIME.py")
        os.remove("e:\\ChineseCharacter\\iniIME.py")
except:
    os.abort()
try:
    import iniIME
except:
    os.abort()
running=1
cursor=0
cursorp=0
ch=None
msg=0
inputc=""
def inputcode(keycode):
    global cursorp,ch,inputc,msg
    if keycode["type"]==2:
        if keycode["scancode"]==50:
            #启用输入法，第一个参数显示位置，第二个当前img,第三个当前输入
            ime=iniIME.iniIME(100,img,"2")
            #获得选择的文字
            ch=ime.getSelect()
            if ch:
                cursorp+=1
                inputc+=ch
        if keycode["scancode"]==51:
            ime=iniIME.iniIME(100,img,"3")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==52:
            ime=iniIME.iniIME(100,img,"4")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==53:
            ime=iniIME.iniIME(100,img,"5")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==54:
            ime=iniIME.iniIME(100,img,"6")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==55:
            ime=iniIME.iniIME(100,img,"7")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==56:
            ime=iniIME.iniIME(100,img,"8")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==57:
            ime=iniIME.iniIME(100,img,"9")
            ch=ime.getSelect()
            if ch:
                inputc+=ch
                cursorp+=1
        if keycode["scancode"]==167:
            sock.sendall("nickName:"+"ca")
            #thread.start_new_thread(chatThread, (1,))
            chatThread(1)
            msg=1
def quit():
    global running
    running=0
    graphics.screenshot().save("e:\\iniIME.png")
def chn(x):
    return x.decode("utf8")
def dchn(x):
    return x.encode("utf8")
canvas=appuifw.Canvas(event_callback=inputcode)
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
img=graphics.Image.new((w,h))
appuifw.app.exit_key_handler=quit
data=""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 54321))
def chatThread(no):
    global data
    while 1:
#        time.sleep(0.3)
        buf=sock.recv(2048)
        if not len(buf):
            break
        data+=buf
while running:
    img.clear(0)
    img.text((20,20),chn("输入法测试"),0xff0000,font=(u"Sans MT 936_S60",20))
    cursor^=0xffffff
    img.line((0,190,240,190),0x00ff00,width=2)
    img.line((5+cursorp*16,200,5+cursorp*16,220),cursor,width=2)
    if msg:
        img.text((5,20),chn(data),(255,255,0),font=(u"Sans MT 936_S60",16))
    if ch:
        img.text((5,220),inputc,(255,255,0),font=(u"Sans MT 936_S60",16))
    canvas.blit(img)
    e32.ao_sleep(0.2)