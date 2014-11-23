from socket import *
from thread import *
from time import *

HOST = '192.168.100.70'
PORT = 50035
MAX_USER = 200

class User(object):
    used = 0
    name = ""
    room = 0

class Room(object):
    used = 0
    name = ""
    max_user = 4

user = list()
for i in xrange(MAX_USER):
    user.append(User())

def check_timeout(check):
    while 1:
        sleep(2)
        u_sendall("ping")

def u_send(i, data):
    try:
        user[i].conn.send("[:pack:]"+data)
    except:
        user[i].used = 0

def u_sendall(data):
    for i in xrange(MAX_USER):
        if user[i].used == 1:
            u_send(i, data)

def response(conn):
    state = 0
    while 1:
        print "Wait.."
        data = conn.recv(2048)
        if not data: break

        data = data.split("::::")
        print data

        if data[0] == "new":
            uid = int(data[1])
            user[uid].name = data[2]
            print data[2], "is connected."

        if data[0] == "say":
            u_sendall("say::::"+user[int(data[1])].name+"::::"+data[2])

def server():
    print 'PyChat Server v.1.0.0'
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print 'Server is starting on %s:%s\n' % (HOST, PORT)
    start_new(check_timeout, (0,))
    while 1:
        conn, addr = s.accept()
        print 'Incomming Connection %s:%s...' % (addr[0], addr[1])
        serverfull = 1
        for i in xrange(MAX_USER):
            if user[i].used == 0:
                start_new(response, (conn,))
                user[i].used = 1
                user[i].conn = conn
                u_send(i, "new::::"+str(i))
                serverfull = 0
                break
        if serverfull == 1:
            conn.send("sv_full")

server()
