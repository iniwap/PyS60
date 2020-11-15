#-*-coding:utf8-*-


#引入模块
import appuifw, key_codes, glcanvas, graphics,e32
from gles import *
#变量定义
running=1
#重绘函数，这里定义了投影变换
def reshape():
    pass
    #
#初始化函数，用于创建运行参数环境
def myinit():
    #相应的初始化操作
    pass
#建模,用于构建三维模型
def modeling():
    #建模
    pass
#显示函数，包含一系列变换操作
def display():
    #外观属性等处理
    pass
#运行逻辑
def logic():
    #定义程序运行逻辑，对所描述问题的操作
    pass
#退出
def exit():
    pass
#按键处理
def keysEvent(event):
    #定义按键事件处理操作
    pass
#主函数
def main():
    appuifw.app.exit_key_handler=exit
    appuifw.app.screen = 'full'
    canvas=glcanvas.GLCanvas(redraw_callback=display,event_callback=keysEvent, resize_callback=reshape)
    appuifw.app.body=canvas
    myinit()
    while running:
        #主循环
        pass
if  __name__=="__main__":
    main()