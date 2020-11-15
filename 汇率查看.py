#-*-coding:utf-8-*-
import appuifw,e32,urllib,re,graphics
ziti=u'CombinedChinesePlain12'
global url
url=""
reg=0.001
running=1
def cn(x):return x.decode("utf-8")
def en(x):return x.encode('utf8')
country=cn('美元')
def USD():
    global country
    country=cn('美元')
    graphics.screenshot().save('c:\\ada.jpg')
    join('USD')
    convert()
def JPY():
    global country
    country=cn('日元')
    join('JPY')
    convert()
def EUR():
    global country
    country=cn('欧元')
    join('EUR')
    convert()
def GBP():
    global country
    country=cn('英镑')
    join('GBP')
    convert()
def HKD():
    global country
    country=cn('港币')
    join('HKD')
    convert()
def TWD():
    global country
    country=cn('台币')
    join('TWD')
    convert()
def CAD():
    global country
    country=cn('加元')
    join('CAD')
    convert()
def KRW():
    global country
    country=cn('韩元')
    join('KRW')
    convert()
def join(x):
    global url
    url="http://www.google.com/finance/converter?a=1&from=CNY&to="+x
def convert():
    global reg
    appuifw.note(cn('请稍后'),'info')
    post=urllib.urlopen(url)
    htmlsrc=post.readlines()
    htmlstr=str(htmlsrc[185])
    reg=re.findall(r'(?<=class\=bld\>).+?(?=\&nbsp\;)',htmlstr)
    reg=reg[0]
def quit():
    global running
    running=0
appuifw.app.body=m=appuifw.Canvas()
appuifw.app.exit_key_handler=quit
appuifw.app.title=cn("汇率查看")
appuifw.app.screen='normal'
appuifw.app.menu=[(cn('美元'),USD),
                  (cn('日元'),JPY),
                  (cn('欧元'),EUR),
                  (cn('英镑'),GBP),
                  (cn('港币'),HKD),
                  (cn('台币'),TWD),
                  (cn('加元'),CAD),
                  (cn('韩元'),KRW)]
img=graphics.Image.new((m.size))
while running:
    img.clear(0xaaaaaa)
    img.text((60,40),cn('汇率查看'),0xffffff,font=ziti)
    img.line((10,43,160,43),0xffffff)
    img.line((100,43,100,110),0xffffff)
    img.line((10,80,160,80),0xffffff)
    img.line((10,110,160,110),0xffffff)
    img.text((20,70),cn('人民币兑')+country,0xffffff,font=ziti)
    img.text((20,100),country+cn('兑人民币'),0xffffff,font=ziti)
    img.text((105,70),cn(str(reg)[:5]),0xffffff,font=ziti)
    img.text((105,100),cn(str(1/float(reg))[:5]),0xffffff,font=ziti)
    m.blit(img)
    graphics.screenshot().save('c:\\ad.jpg')
    e32.ao_yield()