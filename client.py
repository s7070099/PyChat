#!/usr/bin/python
#-*-coding: tis-620 -*-
from socket import *
from thread import *
from time import time, sleep
from Tkinter import *
from uuid import getnode
import tkMessageBox

VERSION = 0.2
DEBUG = 1

class App(object):
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
                self.sock.send(self.data[:len(self.data)-4])


        def config(self, ip="infiteam.no-ip.org", port=12345, nickname="User"):
            self.ip = ip
            self.port = port
            self.nickname = nickname
            self.macaddr = getnode()

        def connect(self):
            self.uid = 0
            self.timeout = 0
            self.connected = 0
            self.threadend = 0
            self.sock = socket(AF_INET, SOCK_STREAM)
            print 'Connecting to %s:%d...' % (self.ip, self.port)
            self.sock.connect((self.ip, self.port))

            self.response_td = start_new(self.response, (self.sock,))
            self.checktimeout_td = start_new(self.checktimeout, (self.sock,))

        def close(self):
            self.sock.shutdown(SHUT_RDWR)
            self.sock.close()
            self.connected = 0
            print "Disconnected."

        def checktimeout(self, conn):
            self.timeout = 0
            stop = 0
            while True:
                print stop
                if stop == 1: return
                sleep(1)
                print id
                self.timeout += 1
                if self.timeout > 3:
                    stop = 1
                    if self.connected == 0:
                        print "Couldn't connect to server. (Connection Timeout)"
                    else:
                        self.connect()
                        print "Connection lost."
                        print "Reconnecting..."
                    return

        def response(self, conn):
            sock = self.Sock(conn)
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
        def __init__(self, mainself):
            self.mainself = mainself
            self.root = Tk()
            self.root.title("Connect")
            self.root.resizable(width=FALSE, height=FALSE)
            self.tk_gui()
            self.root.mainloop()

        def tk_gui(self):
            frame1 = Frame(self.root)
            frame1.grid(row=0, padx=10, pady=0)
            label1 = Label(frame1, text="Server Address:")
            label1.grid(row=0, column=0, sticky=W)
            self.host = Entry(frame1, width=64)
            self.host.grid(row=1, column=0)
            label2 = Label(frame1, text="Nickname:")
            label2.grid(row=2, column=0, sticky=W)
            self.name = Entry(frame1, width=64)
            self.name.grid(row=3, column=0)

            frame2 = Frame(frame1)
            frame2.grid(row=4, pady=10, sticky=E)
            button1 = Button(frame2, text="Connect", command=self.connect)
            button1.grid(row=0, column=0, padx=10, sticky=E)
            button2 = Button(frame2, text="Cancel", command=self.root.destroy)
            button2.grid(row=0, column=1, sticky=E)

            if self.mainself.tk_handle == 1: self.root.bind("<Return>", self.connect)

        def connect(self):
            host = self.host.get().split(":")
            ip = host[0]
            if len(host) == 2:
                port = int(host[1])
            else:
                port = 12345
            name = self.name.get()
            try:
                self.mainself.network.config(ip, port, name)
                self.mainself.network.connect()
                self.root.destroy()
            except:
                print "Could not connect to server."

                
    class Callback(object):
        def window_connect(event, self):
            self.window_connect = self.ConnectWindow(self)
            self.tk_handle = 1

        def window_about(event):
            root = Tk()
            root.title("About PyChat")
            root.resizable(width=FALSE, height=FALSE)

            frame1 = Frame(root)
            frame1.pack(padx=32, pady=10)
            
            label1 = Label(frame1, text="This is a Socket Chat Program")
            label1.pack()
            label2 = Label(frame1, text="Version "+str(VERSION))
            label2.pack()

            def close_window():
                root.destroy()

            button1 = Button(frame1, text="Close Window", command=close_window)
            button1.pack()
            
            root.mainloop()

        def disconnect(event, self):
            self.network.close()
            pass

        def donothing(event):
            pass

        def send_message(event):
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

        def rootquit(event, self):
            self.root.destroy()
            pass
        
    
    def __init__(self):
        CAPTION = "PyChat v." + str(VERSION)
        WIDTH = 1136
        HEIGHT = 640

        self.callback = self.Callback()
        self.network = self.Network()
        self.root = Tk()
        self.root.title(CAPTION)
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.tk_menu()
        self.tk_gui()
        self.tk_handle = 0
        if self.tk_handle == 0: self.root.bind("<Return>", self.callback.send_message)
        self.root.mainloop()

    def tk_menu(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Connect", command=lambda: self.callback.window_connect(self))
        filemenu.add_command(label="Disconnect", command=lambda: self.callback.disconnect(self))
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=lambda: self.callback.rootquit(self))
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
        helpmenu.add_command(label="About PyChat", command=self.callback.window_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def tk_gui(self):
        '''
        frame_pychat = Frame(self.root)
        frame_pychat.pack(side=TOP)
        frame_chat = Frame(frame_pychat)
        frame_chat.pack(side=RIGHT)
        frame_chatlog = Frame(frame_chat)
        frame_chatlog.pack(side=TOP)
        
        scrollbar = Scrollbar(frame_chatlog)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox_user = Listbox(frame_chatlog, width=64, height=38)
        listbox_user.pack(side=RIGHT)
        '''
        '''
        for i in range(100):
            listbox_user.insert(END, "User #"+str(i))
        '''

        '''
        listbox_user.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox_user.yview)
        '''

        '''
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
        '''

        '''
        #init roombox
        frame_room = Frame(frame_pychat)
        frame_room.pack(side=TOP)
        
        scrollbar = Scrollbar(frame_room)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox_room = Listbox(frame_room, width=64, height=38)
        listbox_room.pack()

        for i in range(100):
            listbox_room.insert(END, "Chatroom #"+str(i))

        listbox_room.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox_room.yview)
        '''
        pass

if __name__ == "__main__":
    App()
