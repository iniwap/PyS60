import socket,thread,appuifw
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("127.0.0.1",54321))
s.listen(5)
while 1:
    clientsock,clientaddr=s.accept()
    #print 'connect from',clientsock.getpeername()
    s.sendall("y")
#    buf=sock.recv(2048)
  #  if not len(buf):
    #    break
    clientsock.close()