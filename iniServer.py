import socket,thread,time
def chn(x):return x.decode("utf8")
def dchn(x):return x.encode("utf8")
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',54321))
data=dchn("")
ips=[]
#def chatThread(no):
    #global data
while 1:
        buf, address = s.recvfrom(2048)
        if address not in ips:
            ips.append(address)
        for ip in ips:
            s.sendto(buf, ip)
  #  time.sleep(0.1)
#thread.start_new_thread(chatThread, (1,))
