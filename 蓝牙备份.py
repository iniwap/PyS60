#-*-coding:utf-8-*-
#ubaner.com
import contacts,appuifw
from e32socket import *
def chn(x):
    return x.decode('utf8')
def backUpContact():
    db=contacts.open()
    names=[]
    numbers=[]
    appuifw.note(chn('名片提取中，请稍后...'),'info')
    for i in db:
        names.append(db[i].title)
        num=db[i].find("mobile_number")
        if  num:
            numbers.append(num[0].value)
        else :
            numbers.append(None)
    f=open("c:\\contact.txt","w")
    for i in range(len(names)):
        f.write(names[i].encode("utf8"))
        f.write(':')
        f.write(numbers[i])
        f.write("\n")
def bt_tran():
    try:
        phone = bt_obex_discover('00:11:67:55:8f:69')
        addr=phone[0]
        port=phone[1].values()[0]
        file=u"c:\\contact.txt"
        bt_obex_send_file(addr,port,file)
    except:
        appuifw.note(chn('发送失败'),'error')
backUpContact()
bt_tran()
