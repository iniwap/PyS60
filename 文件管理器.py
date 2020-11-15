#-*-coding:utf8-*-

import os,appuifw,e32,graphics
from key_codes import EKeyLeftArrow
class FileManager:
    def __init__(self):
        self.lock=e32.Ao_lock()
        self.dir_stack=[]
        self.__path__=''
        self.current_dir=['C','E']
    def chn(self,x):
        return x.decode('utf8')
    def rn(self,x):
        return x.encode('utf8')
    def file_select(self):
        self.lb=appuifw.Listbox([self.chn(item) for item in self.current_dir],self.update)
        self.lb.bind(EKeyLeftArrow,lambda:self.update(-1))
        appuifw.app.title=self.chn('open file')
        appuifw.app.body=self.lb
        appuifw.app.exit_key_handler=self.lock.signal
        self.lock.wait()
    def join_path(self,current_path):
        return current_path[0]+':\\'+'\\'.join(current_path[1:])
    def list_dir(self,path_stack):
        path=self.join_path(path_stack)
        for dir_list in os.listdir(path):
            if os.path.isdir(path+'\\'+dir_list):
                self.current_dir.insert(0,dir_list)
            elif dir_list.find('.png')!=-1 or dir_list.find('.jpg')!=-1:
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
            self.dir_stack.append(self.rn(self.chn(self.current_dir[index])))
            self.current_dir=[]
            self.list_dir(self.dir_stack)
        else:
            dir_stack=[self.chn(i) for i in self.dir_stack]
            self.__path__=os.path.join(self.join_path(dir_stack),self.chn(self.current_dir[index]))
        items=[self.chn(s) for s in self.current_dir]
        if len(items)==0:
            items=[self.chn('(empty)')]
        self.lb.set_list(items,0)
fm=FileManager()
fm.file_select()
path=fm.__path__
graphics.Image.open(path)
