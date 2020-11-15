import appuifw,graphics,e32
def cn(x):
    return x.decode('utf-8')
running=1
xn=[0]
hn=[0]
nx=int(raw_input(cn('请输入x1(n)的长度:')))
nh=int(raw_input(cn('请输入x2(n)的长度:')))
print cn('请输入序列x1(n):')
for i in range(nx):
    xn.append(float(raw_input()))
print cn("请输入序列x2(n):")
for i in range(nh):
    hn.append(float(raw_input()))
del xn[0]
del hn[0]
N=int(raw_input(cn("请输入圆周卷积点数:")))
for i in range(len(xn),N):
    xn.append(0)
for i in range(len(hn),N):
    hn.append(0)
yn=[0]
for i in range(N):
    yn1=yn2=0
    for j in range(i+1):
        yn1+=xn[j]*hn[i-j]
    for t in range(i+1,N):
        yn2+=xn[t]*hn[N+i-t]
    yn.append(yn1+yn2)
def handle_redraw(rect):
    canvas.blit(img)
def quit():
    global running
    running=0
canvas=appuifw.Canvas(event_callback=None,redraw_callback=handle_redraw)
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
img=graphics.Image.new((w,h))
appuifw.app.exit_key_handler=quit
while running:
    img.clear(0xffffff)
    for i in range(18):
        img.line((i*10,0,i*10,208),0x0000ff)
    for i in range(21):
        img.line((0,i*10,176,i*10),0x0000ff)
    img.line((0,110,160,110),0x000000)
    img.line((155,105,160,110),0x000000,width=2)
    img.line((155,115,160,110),0x000000,width=2)
    img.line((10,20,10,160),0x000000)
    img.line((5,25,10,20),0x000000,width=2)
    img.line((15,25,10,20),0x000000,width=2)
    for i  in range(1,N+1):
        img.line((10*i,110,10*i,110-3*yn[i]),0xff0000,width=4)
        text=yn[i]
        img.text((10*i,110-3*yn[i]),u"%.0f"%text,0x000000)
        if yn[i]==0:
            img.point((10*i,110),0xff0000,width=4)
    img.text((40,30),u"%d"%N)
    img.text((50,30),cn("点圆周卷积图"),font=u'FONT_BOLD')
    handle_redraw(())
    e32.ao_yield()