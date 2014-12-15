#!/usr/bin/python
#-*-coding: tis-620 -*-

'''
PyChat Server
'''
from socket import *
from thread import *
from time import *
import os

#SETTINGS
VERSION = 0.3
HOST = '127.0.0.1'
PORT =  12345
MAX_USER = 200
MAX_ROOM = 16
SERVER_MSG = 'server_msg.txt'
SERVER_BAN = 'server_ban.txt'
SERVER_CAPTION = "Welcome to Teruyo Server"
DEBUG = 0

#INIT DATA STRUCTURE
class User(object):
    used = 0
    name = ""
    room = -1
    macaddr = ""
    admin = 0

user = list()
for i in xrange(MAX_USER):
    user.append(User())

class Room(object):
    used = 0
    name = ""
    password = ""
    owner = -1
    #max_user = 4

room = list()
for i in xrange(MAX_ROOM):
    room.append(Room())


#NEW SOCK CLASS FOR EASY TO USE
class Sock(object):
    def __init__(self, sock):
        self.sock = sock
        self.data = "[:pack:]"

    def add(self, data):
        self.data += str(data) + "::::"

    def pack(self):
        self.data = self.data[:len(self.data)-4]
        self.data += "[:pack:]"

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
            #check room empty

    def sendall(self):
        for i in xrange(MAX_USER):
            if user[i].used == 1:
                self.send(i)

    def sendroom(self, rid):
        for i in xrange(MAX_USER):
            if user[i].used == 1 and int(user[i].room) == int(rid):
                self.send(i)

    def sendroom_other(self, rid, uid):
        for i in xrange(MAX_USER):
            if user[i].used == 1 and int(user[i].room) == int(rid) and i != int(uid):
                self.send(i)


#MISC FUNC.
def u_send(i, data):
    try:
        user[i].sock.send("[:pack:]"+data)
    except:
        user[i].used = 0

def u_sendall(data):
    for i in xrange(MAX_USER):
        if user[i].used == 1:
            u_send(i, data)

def check_timeout():
    while 1:
        sleep(2)
        sock.clear()
        sock.add("rm_list")
        for i in xrange(MAX_ROOM):
            if room[i].used == 1:
                sock.add(i)
                sock.add(room[i].name)
        sock.sendall()

def log():
    import time
    localtime = time.localtime(time.time())
    timestring = time.strftime ('[%Y-%m-%d %H:%M:%S]')
    return timestring

def getid(name):
    for i in xrange(MAX_USER):
        if user[i].name == name:
            return i
    return -1

def getroom():
    count = 0
    for i in xrange(MAX_ROOM):
        if room[i].used == 1:
            count += 1
    return count

def room_usercount(rid):
    count = 0
    for i in xrange(MAX_USER):
        if user[i].room == rid:
            count += 1
    return count

def sendmessage(text="", uid=-1):
    sock.clear()
    sock.add("print")
    sock.add(text)
    if uid != -1:
        sock.send(uid)

def idn(uid):
    return "("+str(uid)+")"

def filter_restrict(text):
    restrict = ["fuck", "wtf", "shit", "bitch", "wth", "lmao", "lmfao",
                "stfw","damn", "slut", "utsl", "retarded", "fucking",
                "bastard", "prick", "dick", "jerk", "twat", "pussy", "crap",
                "bull", "gfy", "asshole", "giyf", "gtfo", "jfgi", "fgi",
                "stfu", "rtfa", "rtfm", "dfc", "roflao", "douchebag"]
    for i in restrict:
        text = text.replace(i, len(i)*"*")
    return text

#MAIN SERVER LOGIC
def response(conn):
    state = 0
    while 1:
        if DEBUG: print "Wait.."
        data = conn.recv(1024)
        if not data: break
        data_sector = data.split("[:pack:]")[1::]
        if DEBUG: print data_sector
        for i in data_sector:

            data = i.split("::::")
            if DEBUG: print data

            if data[0] == "new" and len(data) == 4:
                uid = int(data[1])
                user[uid].name = data[2]
                user[uid].macaddr = data[3]
                print log(), "User", data[2]+"("+str(uid)+")", "is connected."

                #Send server message to client.
                sock.clear()
                sock.add("sv_msg")
                sock.add(SERVER_CAPTION)
                count = 0
                for i in server_message:
                    if count < 2048:
                        count += len(i)
                        sock.add(i)
                    else:
                        count = 0
                        sock.send(uid)
                        sock.clear()
                        sock.add("sv_msg_add")
                sock.send(uid)
                
                sock.clear()
                sock.add("rm_list")
                for i in xrange(MAX_ROOM):
                    if room[i].used == 1:
                        sock.add(i)
                        sock.add(room[i].name)
                sock.send(uid)

            if data[0] == "chn" and len(data) == 4:
                uid = int(data[1])
                print log(), "User", user[uid].name+"("+str(uid)+")", "Change name to", data[2]
                user[uid].name = data[2]

            if data[0] == "say" and len(data) == 3:
                uid = int(data[1])
                sock.clear()
                sock.add("play_msg")
                sock.sendroom_other(user[uid].room, uid)
                sock.clear()
                sock.add("print")
                sock.add("[" + user[uid].name + "] " + filter_restrict(data[2]))
                sock.sendroom(user[uid].room)
                print log(), "[" + user[uid].name + "]"+"("+str(uid)+")", data[2]

            if data[0] == "dis" and len(data) == 2:
                uid = int(data[1])
                user[uid].used = 0
                print log(), "User", user[uid].name+"("+str(uid)+")", "is disconnected."

            if data[0] == "rm_kick":
                uid = int(data[1])
                oid = int(data[2])
                rid = int(user[uid].room)
                if uid == room[rid].owner and uid != oid and user[oid].used == 1 and user[oid].room == user[uid].room:
                    user[oid].room = -1
                    sock.clear()
                    sock.add("rm_kick")
                    sock.send(oid)
                    sock.clear()
                    sock.add("rm_deluser")
                    sock.add(oid)
                    sock.sendroom(rid)
                    print log(), "User", user[uid].name+"("+str(uid)+") Kick ", user[oid].name+"("+str(oid)+") from room."

            if data[0] == "rm_create" and len(data) == 4:
                uid = int(data[1])
                for i in xrange(MAX_ROOM):
                    if room[i].used == 0:
                        room[i].used = 1
                        room[i].name = data[2]
                        room[i].password = data[3]
                        room[i].owner = uid
                        user[uid].room = i
                        sock.clear()
                        sock.add("rm_join")
                        sock.add(i)
                        sock.add(uid)
                        sock.add(data[2])
                        sock.send(uid)
                        sendmessage("Type /help for command list.", uid)
                        print log(), "User", user[uid].name+"("+str(uid)+")", "Create Room", "[",room[i].name,"]" , "[", i,"]"
                        break

            if data[0] == "rm_request":
                uid = int(data[1])
                rid = int(data[2])
                if room[rid].used == 0: break
                if room[rid].password != "":
                    if len(data) == 4:
                        if data[3] != room[rid].password:
                            sock.clear()
                            sock.add("rm_request")
                            sock.add("1")
                            sock.send(uid)
                            break
                    else:
                        sock.clear()
                        sock.add("rm_request")
                        sock.add("0")
                        sock.add(rid)
                        sock.send(uid)
                        break

                user[uid].room = rid
                sock.clear()
                sock.add("rm_join")
                sock.add(rid)
                sock.add(room[rid].owner)
                sock.add(room[rid].name)
                sock.add("rm_list")
                for i in xrange(MAX_USER):
                    if user[i].room == rid:
                        print user[i].name
                        sock.add(i)
                        sock.add(user[i].name)
                sock.send(uid)

                sock.clear()
                sock.add("rm_adduser")
                sock.add(uid)
                sock.add(user[uid].name)
                sock.sendroom_other(rid, uid)
                
                sendmessage("Type /help for command list.", uid)

            if data[0] == "rm_deluser":
                uid = int(data[1])
                rid = user[uid].room
                sock.clear()
                sock.add("rm_deluser")
                sock.add(uid)
                sock.sendroom_other(rid, uid)
                if int(uid) == int(room[rid].owner):
                    new_owner = 0
                    for i in xrange(MAX_USER):
                        if user[i].room == rid and i != uid:
                            room[rid].owner = i
                            sock.clear()
                            sock.add("rm_chowner")
                            sock.add("")
                            sock.add("")
                            sock.add(i)
                            sock.add(user[i].name)
                            sock.sendroom_other(user[uid].room, uid)
                            new_owner = 1
                            break
                    if new_owner == 0:
                        room[rid].used = 0
                user[uid].room = -1

            if data[0] == "rm_chowner":
                uid = int(data[1])
                oid = int(data[2])
                rid = int(user[uid].room)
                if uid == int(room[rid].owner) and uid != oid and user[oid].used == 1 and user[oid].room == user[uid].room:
                    room[rid].owner = oid
                    sock.clear()
                    sock.add("rm_chowner")
                    sock.add(uid)
                    sock.add(user[uid].name)
                    sock.add(oid)
                    sock.add(user[oid].name)
                    sock.sendroom(rid)
                    print log(), "User", user[uid].name+idn(uid), "Change owner to", user[oid].name+idn(oid)+"."

            if data[0] == "exc":
                uid = int(data[1])
                
                if data[2] == "help":
                    sendmessage("/example1", uid)
                    sendmessage("/example2", uid)
                    sendmessage("/example3", uid)

                elif data[2] == "ban":
                    oid = int(data[3])
                    if user[uid].admin > 0:
                        with open(SERVER_BAN, "a") as f:
                            f.writeline(user[oid].macaddr)
                    else:
                        sendmessage("Permission Denied!", uid)

                elif data[2] == "pm":
                    oid = int(data[3])
                    if data[4] != "":
                        sendmessage("[FROM "+user[uid].name+"] "+data[4], oid)

                else:
                    sendmessage("Server Unknown Command: /"+data[2], uid)

            #sock.clear()
            #sock.add("err")
            #sock.sendsock(conn)

#INIT SOCKET, RECEIVER AND INIT VAR.
def server():
    print 'PyChat Dedicated Server', VERSION, ""
    
    print 'Reading server message...'
    global server_message
    server_message = list()
    if os.path.isfile(SERVER_MSG):
        f = open(SERVER_MSG)
        for i in f:
            server_message.append(i)
        f.close()

    print 'Reading server ban list...'
    global server_ban
    server_ban = list()
    if os.path.isfile(SERVER_BAN):
        f = open(SERVER_BAN)
        for i in f:
            server_ban.append(i)
        f.close()

    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print 'Server is starting on %s:%s\n' % (HOST, PORT), '\n'
    global sock
    sock = Sock(s)
    
    start_new(check_timeout, ())
    while 1:
        conn, addr = s.accept()
        print log(), 'Incomming Connection %s:%s...' % (addr[0], addr[1])
        serverfull = 1
        for i in xrange(MAX_USER):
            if user[i].used == 0:
                start_new(response, (conn,))
                user[i].used = 1
                user[i].sock = conn
                sock.clear()
                sock.add("new")
                sock.add(i)
                sock.send(i)
                serverfull = 0
                break
        if serverfull == 1:
            conn.send("sv_full")

if __name__ == "__main__":
    server()
