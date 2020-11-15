import socket,thread,time,sys,e32
def chn(x):return x.decode("utf8")
def dchn(x):return x.encode("utf8")
host = '127.0.0.1'
port = 54321
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))
inputc=chn("我")
timer=e32.Ao_timer()
def chatThread():
    s.sendall(dchn(chn('nickname:')+inputc))
    buf = s.recv(2048)
    print chn(buf)
    timer.after(0.01,chatThread)
timer.after(0.01,chatThread)