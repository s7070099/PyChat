#!/usr/bin/python
#-*-coding: tis-620 -*-

'''
PyChat Server 1.0
'''
from socket import *
from thread import *
from time import *
import re, os, sys

#USER SETTINGS
HOST = '192.168.100.60'
PORT =  12345
MAX_USER = 200
MAX_ROOM = 16
SERVER_LOG = '' #emtpy if no Logging save.
SERVER_MSG = 'server_msg.txt'
SERVER_BAN = 'server_ban.txt'
SERVER_BADWORD = 'server_badword.txt'
SERVER_CMDHELP = 'server_commandhelp.txt'
SERVER_CAPTION = 'Welcome to Teruyo Server'
RECON_PASSWORD = "123456"

#DEVELOPER SETTINGS
VERSION = 1.0
DEBUG = 0

#INIT DATA STRUCTURE
class User(object):
    '''User Data Class'''
    used = 0
    ip = ""
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
            user_clear(i)
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
def user_clear(uid):
    rid = user[uid].room
    user[uid].used = 0
    if user[uid].room != -1:
        sock.clear()
        sock.add("rm_deluser")
        sock.add(uid)
        sock.sendroom_other(user[uid].room, uid)
        user[uid].room = -1
        if room[rid].owner == uid:
            auto_owner(uid, rid)

def u_send(i, data):
    try:
        user[i].sock.send("[:pack:]"+data)
    except:
        user[i].used = 0

def u_sendall(data):
    for i in xrange(MAX_USER):
        if user[i].used == 1:
            u_send(i, data)

def logging():
    while 1:
        server_log = sys.stdout
        log_file = open(SERVER_LOG,"a")
        sys.stdout = log_file
        sleep(1)
        sys.stdout = server_log
        log_file.close()

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

def sendmessageroom(text="", rid=-1):
    if rid != -1:
        for i in xrange(MAX_USER):
            if user[i].used == 1 and user[i].room == rid    :
                sendmessage(text, i)

def sendmessageall(text=""):
    for i in xrange(MAX_USER):
        if user[i].used == 1:
            sendmessage(text, i)

def idn(uid):
    return "("+str(uid)+")"

def auto_owner(uid, rid):
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
            return
    room[rid].used = 0

def is_banned(text):
    return str(text) in server_ban

def ban(uid):
    rid = int(user[uid].room)
    sock.clear()
    sock.add("ban")
    sock.send(uid)
    if rid != -1:
        sock.clear()
        sock.add("rm_deluser")
        sock.add(uid)
        sock.sendroom_other(rid, uid)
        if uid == room[rid].owner:
            auto_owner(uid, rid)

def replace_ex(text, old, new):
    text = re.compile(re.escape(old), re.IGNORECASE)
    text.sub(new, text)
    return text

def filter_badword(text):
    for i in server_badword:
        text = text.replace(i, len(i)*'*')
        #text = replace_ex(text, i, len(i)*'*')
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
                if is_banned(data[3]):
                    sock.clear()
                    sock.add("ban")
                    sock.send(uid)
                    print log(), "User", data[2]+"("+str(uid)+")", "was kick from server. (Server Ban)"
                else:
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
                sock.add("[" + user[uid].name + "] " + filter_badword(data[2]))
                sock.sendroom(user[uid].room)
                print log(), "[" + user[uid].name + "]"+"("+str(uid)+")", data[2]

            if data[0] == "dis" and len(data) == 2:
                uid = int(data[1])
                user[uid].used = 0
                print log(), "User", user[uid].name+"("+str(uid)+")", "is disconnected."

            if data[0] == "rm_create" and len(data) == 4:
                uid = int(data[1])
                if getroom() < MAX_ROOM:
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
                else:
                    sock.clear()
                    sock.add("print")
                    sock.add("Exceeds max room limit!")
                    sock.send(uid)

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
                sock.add("play_join")
                sock.sendroom_other(user[uid].room, uid)
                sock.clear()
                sock.add("rm_join")
                sock.add(rid)
                sock.add(room[rid].owner)
                sock.add(room[rid].name)
                sock.add("rm_list")
                for i in xrange(MAX_USER):
                    if user[i].room == rid:
                        #print user[i].name
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
                sock.clear()
                sock.add("play_exit")
                sock.sendroom_other(user[uid].room, uid)
                if int(uid) == int(room[rid].owner):
                    auto_owner(uid, rid)
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
                rid = user[uid].room

                if data[2] == "help":
                    for i in server_cmdhelp:
                        sendmessage(i, uid)

                elif data[2] == "pm":
                    oid = int(data[3])
                    if data[4] != "":
                        tmp = ' '.join(data[4:])
                        sendmessage("[FROM "+user[uid].name+"] "+tmp, oid)
                        sock.clear()
                        sock.add("play_pm")
                        sock.send(oid)

                elif data[2] == "room":
                    if data[3] == "name":
                        if room[rid].owner == uid:
                            tmp = ' '.join(data[4:])
                            room[rid].name = tmp
                            sock.clear()
                            sock.add("rm_rename")
                            sock.add(tmp)
                            sock.sendroom(rid)
                            sendmessageroom(user[uid].name + " change room name to " + tmp + ".", rid)
                        
                    elif data[3] == "password":
                        if room[rid].owner == uid:
                            tmp = ' '.join(data[4:])
                            room[rid].password = tmp
                            sendmessageroom(user[uid].name + " change room password to " + tmp + ".", rid)

                elif data[2] == "user":
                    if data[3] == "nickname":
                        tmp = ' '.join(data[4:])
                        user[uid].name = tmp
                        sock.clear()
                        sock.add("nickname")
                        sock.add(tmp)
                        sock.send(uid)
                        if rid != -1:
                            sock.clear()
                            sock.add("rm_deluser")
                            sock.add(uid)
                            sock.sendroom(rid)
                            sock.clear()
                            sock.add("rm_adduser")
                            sock.add(uid)
                            if room[rid].owner == uid:
                                tmp += " (owner)"
                            sock.add(tmp)
                            sock.sendroom(rid)
                            sendmessageroom(user[uid].name + " change nickname to " + user[uid].name + ".", rid)

                elif data[2] == "kick" and len(data) > 3:
                    oid = int(data[3])
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

                elif data[2] == "ban" and len(data) > 3:
                    if user[uid].admin > 0:   
                        if data[3] == "ip":
                            ip = data[4]
                            server_ban.append(ip)
                            f = open(SERVER_BAN, 'a')
                            f.write(ip)
                            f.close()
                            for i in xrange(MAX_USER):
                                if user[i].ip == ip:
                                    ban(i)
                                    print log(), user[uid].name+"("+str(uid)+")", "ban", user[i].name+"("+str(i)+"). (IP BAN)"
                        else:
                            oid = int(data[3])
                            if user[oid].used == 1:
                                server_ban.append(user[oid].macaddr)
                                f = open(SERVER_BAN, 'a')
                                f.write(user[oid].macaddr)
                                f.close()
                                for i in xrange(MAX_USER):
                                    if user[i].macaddr == user[oid].macaddr:
                                        ban(i)
                                        print log(), user[uid].name+"("+str(uid)+")", "ban", user[oid].name+"("+str(oid)+"). (MAC BAN)"
                    else:
                        sendmessage("Permission Denied!", uid)

                elif data[2] == "recon" and len(data) > 4:
                    if data[3] == "password":
                        if data[4] == RECON_PASSWORD:
                            user[uid].admin = 1
                            print log(), user[uid].name+"("+str(uid)+")", "Access Admin Permission."
                            sock.clear()
                            sock.add("print")
                            sock.add("Permission Granted.")
                            sock.send(uid)

                else:
                    sendmessage("Server Unknown Command: /"+data[2], uid)

            #sock.clear()
            #sock.add("err")
            #sock.sendsock(conn)

#INIT SOCKET, RECEIVER AND INIT VAR.
def server():
    '''Server Main Program'''

    if SERVER_LOG != "":
        print "***START IN LOGGING MODE***"
        start_new(logging, ())
        sleep(2)
    
    print 'PyChat Dedicated Server', VERSION, ""
    print 'Reading server message...'
    global server_message
    server_message = list()
    if os.path.isfile(SERVER_MSG):
        f = open(SERVER_MSG)
        for i in f:
            server_message.append(i)
        f.close()

    print 'Reading server command help...'
    global server_cmdhelp
    server_cmdhelp = list()
    if os.path.isfile(SERVER_CMDHELP):
        f = open(SERVER_CMDHELP)
        for i in f:
            server_cmdhelp.append(i.replace("\n", ""))
        f.close()

    print 'Reading server ban list...'
    global server_ban
    server_ban = list()
    if os.path.isfile(SERVER_BAN):
        f = open(SERVER_BAN)
        for i in f:
            server_ban.append(i)
        f.close()

    print 'Reading server badword list...'
    global server_badword
    server_badword = list()
    if os.path.isfile(SERVER_BADWORD):
        f = open(SERVER_BADWORD)
        for i in f:
            server_badword.append(i.replace("\n", ""))
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
        if is_banned(addr[0]):
            sock.clear()
            sock.add("print")
            sock.add("Server IP Banned !")
            sock.sendsock(conn)
            print log(), "Refuse Connection %s:%s (Server IP Ban)." % (addr[0], addr[1])
        else:
            serverfull = 1
            for i in xrange(MAX_USER):
                if user[i].used == 0:
                    start_new(response, (conn,))
                    user[i].used = 1
                    user[i].sock = conn
                    user[i].ip = addr[0]
                    user[i].room = 0
                    user[i].admin = 0
                    user[i].macaddr = ""
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
