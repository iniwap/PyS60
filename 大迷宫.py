#-*-coding:utf8-*-

import appuifw,graphics,e32,random,copy
from key_codes import *
running,pos_x,pos_y,step=1,0,0,0
Maze=[[[(i,j),[0,0,0,0],0]for i in range(29)]for j in range(29)]
def move(x,y):
    global pos_x,pos_y,Maze,step
    tmpx=pos_x
    tmpy=pos_y
    if x==1:
        if Maze[pos_y][pos_x][1][0]==1:
            step+=1
            pos_x+=1
    elif x==-1:
        if Maze[pos_y][pos_x][1][2]==1:
            step+=1
            pos_x+=-1
    elif y==1:
        if Maze[pos_y][pos_x][1][1]==1:
            step+=1
            pos_y+=1
    else:
        if Maze[pos_y][pos_x][1][3]==1:
            step+=1
            pos_y+=-1
    if tmpx!=pos_x or tmpy!=pos_y:
        img.point((tmpx*8+8,tmpy*8+8),0xaaaaaa,width=6)
    if pos_x==28 and pos_y==28:
        img.text((100,100),chn("通关了！"),0xff0000)
def get_neighbors(cell):
    neighbors=[]
    if cell[0][0]+1<len(Maze):
        if Maze[cell[0][1]][cell[0][0]+1][2]==0:
            neighbors.append(Maze[cell[0][1]][cell[0][0]+1])
    if cell[0][1]+1<len(Maze):
        if Maze[cell[0][1]+1][cell[0][0]][2]==0:
            neighbors.append(Maze[cell[0][1]+1][cell[0][0]])
    if cell[0][0]-1>=0:
        if Maze[cell[0][1]][cell[0][0]-1][2]==0:
            neighbors.append(Maze[cell[0][1]][cell[0][0]-1])
    if cell[0][1]-1>=0:
        if Maze[cell[0][1]-1][cell[0][0]][2]==0:
            neighbors.append(Maze[cell[0][1]-1][cell[0][0]])
    return neighbors
def generate_Maze():
    depth=0
    MazeStack=[]
    current_cell=Maze[0][0]
    mark_visited(current_cell)
    MazeStack.append(current_cell)
    while len(MazeStack)!=0:
        depth+=1
        neighbor=get_neighbors(current_cell)
        if len(neighbor)!=0 and depth%16!=0:
            temp=random.randint(0,len(neighbor)-1)
            knock_wall(current_cell,neighbor[temp])
            current_cell=neighbor[temp]
            mark_visited(current_cell)
            MazeStack.append(current_cell)
        elif len(neighbor)!=0 and depth%16==0:
            temp=random.randint(0,len(MazeStack)-1)
            current_cell=MazeStack[temp]
            del(MazeStack[temp])
        else:
            current_cell=MazeStack.pop()
def knock_wall(cell,next_cell):
    x=cell[0][0]
    y=cell[0][1]
    next_x=next_cell[0][0]
    next_y=next_cell[0][1]
    if x+1==next_x:
        Maze[y][x][1][0]=1
        Maze[next_y][next_x][1][2]=1
    if y+1==next_y:
        Maze[y][x][1][1]=1
        Maze[next_y][next_x][1][3]=1
    if x-1==next_x:
        Maze[y][x][1][2]=1
        Maze[next_y][next_x][1][0]=1
    if y-1==next_y:
        Maze[y][x][1][3]=1
        Maze[next_y][next_x][1][1]=1
def mark_visited(cell):
    x=cell[0][0]
    y=cell[0][1]
    Maze[y][x][2]=1
def quit():
    global running
    graphics.screenshot().save("c:\\maze.png")
    running=0
def chn(x):
    return x.decode("utf8")
canvas=appuifw.Canvas()
appuifw.app.body=canvas
appuifw.app.screen="full"
w,h=canvas.size
canvas.bind(EKeyLeftArrow,lambda:move(-1,0))
canvas.bind(EKeyRightArrow,lambda:move(1,0))
canvas.bind(EKeyDownArrow,lambda:move(0,1))
canvas.bind(EKeyUpArrow,lambda:move(0,-1))
img=graphics.Image.new((w,h))
imgtext=graphics.Image.new((60,20))
appuifw.app.exit_key_handler=quit
def paintMaze():
    img.clear(0xaaaaaa)
    for x in range(29):
        for y in range(29):
            img.rectangle((x*8+5,5+y*8,x*8+13,13+y*8),0x0000ff)
            if Maze[y][x][1][0]==1:
                img.line((x*8+12,6+y*8,x*8+12,y*8+10),0xaaaaaa,width=2)
            if Maze[y][x][1][1]==1:
                img.line((x*8+6,12+y*8,x*8+10,y*8+12),0xaaaaaa,width=2)
            if Maze[y][x][1][2]==1:
                img.line((x*8+4,6+y*8,x*8+4,y*8+10),0xaaaaaa,width=2)
            if Maze[y][x][1][3]==1:
                img.line((x*8+6,4+y*8,x*8+10,y*8+4),0xaaaaaa,width=2)
    img.rectangle((4,4,238,238),0x0000ff)
    img.line((4,4,4,11),0xaaaaaa,width=2)
    img.line((230,236,238,236),0xaaaaaa,width=2)
    img.text((40,260),chn('Steps:'),0x0000ff)
def play():
  global pos_x,pos_y,step
  generate_Maze()
  paintMaze()
  while running:
    imgtext.clear(0xaaaaaa)
    img.point((pos_x*8+8,pos_y*8+8),0x00ff00,width=6)
    imgtext.text((5,10),chn(str(step)),0xff0000)
    img.blit(imgtext,target=(80,250))
    canvas.blit(img)
    e32.ao_yield()
play()