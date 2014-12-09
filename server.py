#!/usr/bin/python
#-*-coding: tis-620 -*-

'''
PyChat Server
Version: 0.1
'''
from socket import *
from thread import *
from time import *

#SETTINGS
HOST = '127.0.0.1'
PORT =  12345
MAX_USER = 200
MAX_ROOM = 32
DEBUG = 1

#INIT DATA STRUCTURE
class User(object):
    used = 0
    name = ""
    room = 0
    macaddr = ""

user = list()
for i in xrange(MAX_USER):
    user.append(User())

class Room(object):
    used = 0
    name = ""
    max_user = 4

room = list()
for i in xrange(MAX_ROOM):
    room.append(Room())

#SIMPLE SOCK FUNC.
def u_send(i, data):
    try:
        user[i].sock.send("[:pack:]"+data)
    except:
        user[i].used = 0

def u_sendall(data):
    for i in xrange(MAX_USER):
        if user[i].used == 1:
            u_send(i, data)

def check_timeout(check):
    while 1:
        sleep(2)
        u_sendall("ping")

#NEW SOCK CLASS FOR EASY TO USE
class Sock(object):
    def __init__(self, sock):
        self.sock = sock
        self.data = "[:pack:]"

    def add(self, data):
        self.data += str(data) + "::::"

    def clear(self):
        self.data = "[:pack:]"

    def sendsock(self, s):
        try:
            s.send(self.data[:len(self.data)-4])
        except:
            for i in xrange(MAX_USER):
                if user[i].sock == s:
                    user[i].used = 0
                    return

    def send(self, i):
        try:
            user[i].sock.send(self.data[:len(self.data)-4])
        except:
            user[i].used = 0

    def sendall(self):
        for i in xrange(MAX_USER):
            if user[i].used == 1:
                self.send(i)


#MAIN SERVER LOGIC
def response(conn):
    state = 0
    while 1:
        if DEBUG:   print "Wait.."
        data = conn.recv(2048)
        if not data: break
        data_sector = data.split("[:pack:]")[1::]
        if DEBUG:   print data_sector
        for i in data_sector:

            data = i.split("::::")
            if DEBUG:   print data

            if data[0] == "new" and len(data) == 4:
                uid = int(data[1])
                user[uid].name = data[2]
                user[uid].macaddr = data[3]
                print "User
                ", data[2], "is connected."
                break

            if data[0] == "say" and len(data) == 3:
                sock.clear()
                sock.add("say")
                sock.add(user[int(data[1])].name)
                sock.add(data[2])
                sock.sendall()
                break

            if data[0] == "dis" and len(data) == 2:
                uid = int(data[1])
                user[uid].used = 0
                break

            sock.clear()
            sock.add("err")
            sock.sendsock(conn)

#INIT SOCKET, RECEIVER AND INIT VAR.
def server():
    print 'PyChat Server v.1.0.0'
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    global sock
    sock = Sock(s)
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
                user[i].sock = conn
                u_send(i, "new::::"+str(i))
                serverfull = 0
                break
        if serverfull == 1:
            conn.send("sv_full")

if __name__ == "__main__":
    server()
