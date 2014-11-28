#!/usr/bin/python
#-*-coding: tis-620 -*-

from socket import *
from thread import *
from time import time, sleep
from Tkinter import *
from uuid import getnode

VERSION = 0.1
DEBUG = 1

class App(object):
    def __init__(self):
        self.main = self.MainWindow()
        mainloop()

    class Network(object):
        class Sock(object):
            def __init__(self, sock):
                self.sock = sock
                self.data = "[:pack:]"

            def add(self, data):
                self.data += str(data) + "::::"

            def clear(self):
                self.data = "[:pack:]"

            def send(self):
                self.sock.send(self.data)

        def config(self, ip="infiteam.no-ip.org", port=12345, nickname="User"):
            self.ip = ip
            self.port = port
            self.nickname = nickname
            self.macaddr = getnode()

        def connect(self):
            self.uid = 0
            self.timeout = 0
            self.connected = 0
            self.sock = socket(AF_INET, SOCK_STREAM)
            print 'Connecting to %s:%d...' % (self.ip, self.port)
            self.sock.connect((self.ip, self.port))

            start_new(self.response, (s,))
            start_new(self.check_timeout, (s,))

        def check_timeout(self, conn):
            self.timeout = 0
            while True:
                sleep(1)
                self.timeout += 1
                if self.timeout > 3:
                    if self.connected == 0:
                        print "Couldn't connect to server. (Connection Timeout)"
                    else:
                        self.connected = 0
                        print "Connection lost."
                        self.connect()
                        print "Reconnecting..."
                    return

        def response(self, conn):
            sock = Sock()
            while True:
                data = conn.recv(2048)
                if not data: break
                
                data_sector = data.split("[:pack:]")[1::]
                for i in data_sector:
                    data = i.split("::::")

                    if data[0] == "sv_full":
                        print "Couldn't connect to server. (Server is full!)"
                        return

                    if data[0] == "new":
                        self.uid = int(data[1])
                        if self.uid >= 0:
                            self.connected = 1
                            sock.clear()
                            sock.add("new")
                            sock.add(self.uid)
                            sock.add(self.nickname)
                            sock.add(self.macaddr)
                            sock.send()
                            print "Connected."

                    if data[0] == "ping":
                        self.timeout = 0

                    if data[0] == "say":
                        print "[%s] %s" % (data[1], data[2])
                        #text.insert(END, "[%s] %s" % (data[1], data[2])+ "\n")
                        #text.yview(END)

                    if data[0] == "join":
                        pass

                    if data[0] == "left":
                        pass

    class ConnectWindow(object):
        def __init__(self):
            pass

        def tk_gui(self):
            '''
            root_connect = Tk()
            root_connect.title("Connect")

            frame1 = Frame(root_connect)
            frame1.pack(side=LEFT)
            frame2 = Frame(root_connect)
            frame2.pack(side=LEFT)
            
            label1 = Label(frame1, text="Server Address:")
            label1.pack()
            gethost = Entry(frame1)
            gethost.pack()
            gethost.delete(0, END)
            gethost.insert(0, "")
            
            label1 = Label(frame2, text="Nickname:")
            label1.pack(side=LEFT)
            getname = Entry(frame2)
            getname.pack(side=LEFT)
            getname.delete(0, END)
            getname.insert(0, "")
            
            button_getname = Button(root_connect, text="Enter", command=getname_callback)
            button_getname.pack(side=RIGHT)
            '''
            #root_connect.bind("<Return>", getname_callback)
            #root_connect.mainloop()
            pass

    class MainWindow(object):
        class Callback(object):
            def donothing(self):
                pass

            def send_message(self, event):
                print event
                pass

            def getname_callback(event=0):
                global nickname
                nickname = getname.get()
                print "Set name to", nickname
                client()
                root1.destroy()

            def send_callback(event=0):
                global connected
                if connected == 1:
                    global uid
                    #print getmsg.get()[0], ord(getmsg.get()[0])
                    s.send("say::::"+str(uid)+"::::"+utf8_encode(getmsg.get()))
                    getmsg.delete(0, END)
                    getmsg.insert(0, "")
                else:
                    text.insert(END, "Please reconnect.\n")
                    text.yview(END)
        
        def __init__(self):
            CAPTION = "PyChat v." + str(VERSION)
            WIDTH = 1136
            HEIGHT = 640

            self.callback = self.Callback()
            self.root = Tk()
            self.root.title(CAPTION)
            self.root.resizable(width=FALSE, height=FALSE)
            self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
            self.tk_menu()
            self.tk_gui()
            self.root.bind("<Return>", self.callback.send_message)

        def show(self):
            self.root.mainloop()
            pass

        def hide(self):
            pass

        def tk_menu(self):
            menubar = Menu(self.root)
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="Connect", command=self.callback.donothing)
            filemenu.add_command(label="Disconnect", command=self.callback.donothing)
            filemenu.add_separator()
            filemenu.add_command(label="Quit", command=self.callback.donothing)
            menubar.add_cascade(label="Connections", menu=filemenu)
            
            editmenu = Menu(menubar, tearoff=0)
            editmenu.add_command(label="Undo", command=self.callback.donothing)
            editmenu.add_separator()
            editmenu.add_command(label="Cut", command=self.callback.donothing)
            editmenu.add_command(label="Copy", command=self.callback.donothing)
            editmenu.add_command(label="Paste", command=self.callback.donothing)
            editmenu.add_command(label="Delete", command=self.callback.donothing)
            editmenu.add_command(label="Select All", command=self.callback.donothing)
            menubar.add_cascade(label="Settings", menu=editmenu)

            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="Check for Update", command=self.callback.donothing)
            helpmenu.add_command(label="About PyChat", command=self.callback.donothing)
            menubar.add_cascade(label="Help", menu=helpmenu)

            self.root.config(menu=menubar)

        def tk_gui(self):
            frame_pychat = Frame(self.root)
            frame_pychat.pack(side=TOP)
            frame_chat = Frame(frame_pychat)
            frame_chat.pack(side=RIGHT)
            frame_chatlog = Frame(frame_chat)
            frame_chatlog.pack(side=TOP)

            scrollbar = Scrollbar(frame_chatlog)
            scrollbar.pack(side=RIGHT, fill=Y)
            listbox_user = Listbox(frame_chatlog, width=24, height=38)
            listbox_user.pack(side=RIGHT)
            '''
            for i in range(100):
                listbox_user.insert(END, "User #"+str(i))
            '''

            listbox_user.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox_user.yview)
            
            scrollbar = Scrollbar(frame_chatlog)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.log = Text(frame_chatlog, width=90,height=38)
            self.log.pack(side=RIGHT)
            self.log.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.log.yview)

            frame_chatbox = Frame(frame_chat)
            frame_chatbox.pack(side=LEFT)
            label2 = Label(frame_chatbox, text="Chat:")
            label2.pack(side=LEFT)
            self.msg = Entry(frame_chatbox, width=111)
            self.msg.pack(side=LEFT)
            self.msg.delete(0, END)
            self.msg.insert(0, "")
            self.msg_send = Button(frame_chatbox, text="Send", command=self.callback.send_message)
            self.msg_send.pack(side=LEFT)

            #init roombox
            frame_room = Frame(frame_pychat)
            frame_room.pack(side=TOP)
            
            scrollbar = Scrollbar(frame_room)
            scrollbar.pack(side=RIGHT, fill=Y)

            listbox_room = Listbox(frame_room, width=40, height=38)
            listbox_room.pack()

            for i in range(100):
                listbox_room.insert(END, "Chatroom #"+str(i))

            listbox_room.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox_room.yview)
            pass

app = App()
