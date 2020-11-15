#-*-coding:utf8-*-
import os,shutil,appuifw,graphics,e32
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
from key_codes import *
running=1
cursor=0
cursorp=0
ch=None
inputc=""
def inputcode(keycode):
    global cursorp,ch,inputc
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
def quit():
    global running
    running=0
    graphics.screenshot().save("e:\\iniIME.png")
  #  print "Bye!"
    os.abort()
def chn(x):
    return x.decode("utf8")
canvas=appuifw.Canvas(event_callback=inputcode)
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
img=graphics.Image.new((w,h))
appuifw.app.exit_key_handler=quit
while running:
    img.clear(0)
    img.text((20,20),chn("输入法测试"),0xff0000,font=(u"Sans MT 936_S60",20))
    cursor^=0xffffff
    img.line((20+cursorp*20,50,20+cursorp*20,70),cursor,width=2)
    if ch:
        img.text((20,70),inputc,(255,255,0),font=(u"Sans MT 936_S60",20))
    canvas.blit(img)
    e32.ao_sleep(0.2)