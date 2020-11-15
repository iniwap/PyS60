#-*-coding:utf8-*-

#ubaner.com
import inbox,messaging,telephone,e32
def chn(x):
    return x.decode('utf8')
i=inbox.Inbox()
while 1:
    e32.ao_sleep(1)
    i_id=i.sms_messages()
    if i.unread(i_id[0]):
        messaging.sms_send("10086",i.content(i_id[0])+'\n\n'+chn('来自：')+i.address(i_id[0]),"UCS2")
        i.set_unread(i_id[0],0)
        break
