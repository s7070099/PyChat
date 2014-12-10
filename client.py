#!/usr/bin/python
#-*-coding: tis-620 -*-

'''
PyChat Client
'''
from socket import *
from thread import *
from time import time, sleep
from Tkinter import *
from uuid import getnode
import tkMessageBox, sys, os

VERSION = 0.2
DEBUG = 1
#os.system('c:\python27\python server.py')

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

        def __init__(self):
            self.connected = 0
            self.stop = 0

        def config(self, ip="infiteam.no-ip.org", port=12345, nickname="User"):
            self.ip = ip
            self.port = port
            self.nickname = nickname
            self.macaddr = getnode()

        def connect(self):
            if self.connected == 1:
                self.close()
                sleep(1)
            self.uid = 0
            self.timeout = 0
            self.connected = 0
            self.threadend = 0
            self.stop = 0
            self.sock = socket(AF_INET, SOCK_STREAM)
            print 'Connecting to %s:%d...' % (self.ip, self.port)
            self.sock.connect((self.ip, self.port))

            self.response_td = start_new(self.response, (self.sock,))
            self.checktimeout_td = start_new(self.checktimeout, (self.sock,))

        def close(self):
            sock = self.Sock(self.sock)
            sock.clear()
            sock.add("dis")
            sock.add(self.uid)
            sock.send()
            self.sock.close()
            self.connected = 2
            self.stop = 1
            print "Disconnected."

        def checktimeout(self, conn):
            stop = 0
            while True:
                if stop == 1: return
                stop = self.stop
                if stop == 1: return
                sleep(0.5)
                self.timeout += 0.5
                if self.timeout > 3:
                    stop = 1
                    if self.connected == 0:
                        print "Couldn't connect to server. (Connection Timeout)"
                    elif self.connected == 1:
                        self.connect()
                        print "Connection lost."
                        print "Reconnecting..."

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

                    if data[0] == "err":
                        print "Kicked from server. (Socket Error)"
                        self.close()
                    

    class ConnectWindow(object):
        def __init__(self, mainself):
            CAPTION = "Connect"
            
            self.mainself = mainself
            self.root = Tk()
            self.root.title(CAPTION)
            self.root.resizable(width=FALSE, height=FALSE)
            self.tk_gui()
            
            if os.path.isfile("user.cfg"):
                f = open("user.cfg")
                host, name = f.readline().split(" ")
                self.host.insert(0, host)
                self.name.insert(0, name)
                f.close()
                
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

            self.root.bind("<Return>", self.connect)

        def connect(self, event=0):
            host_str = self.host.get()
            host = host_str.split(":")
            ip = host[0]
            if len(host) == 2:
                port = int(host[1])
            else:
                port = 12345
            name = self.name.get()
            f = open("user.cfg", "w")
            f.write(host_str+" "+name)
            f.close()
            try:
                self.mainself.network.config(ip, port, name)
                self.mainself.network.connect()
                self.root.destroy()
            except:
                print "Could not connect to server."

                
    class Callback(object):
        def window_connect(event, self):
            self.window_connect = self.ConnectWindow(self)

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
            label3 = Label(frame1, text="")
            label3.pack()
            label4 = Label(frame1, text="by Rungsimun and Pattamaporn")
            label4.pack()
            label5 = Label(frame1, text="")
            label5.pack()

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

        def send_message(self, event):
            print self, event

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

        self.caption = CAPTION
        self.callback = self.Callback()
        self.network = self.Network()
        self.root = Tk()
        self.root.title(CAPTION)
        self.root.resizable(width=FALSE, height=FALSE)
        self.tk_menu()
        self.tk_gui()
        self.root.bind("<Return>", self.callback.send_message)
        self.root.mainloop()

    def tk_menu(self):
        menubar = Menu(self.root)
        #menubar.config(bg='white', bd=0)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Connect", command=lambda: self.callback.window_connect(self))
        filemenu.add_command(label="Disconnect", command=lambda: self.callback.disconnect(self))
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=lambda: self.callback.rootquit(self))
        menubar.add_cascade(label="Connections", menu=filemenu)
        
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Change Name", command=self.callback.donothing)
        menubar.add_cascade(label="Settings", menu=editmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Check for Update", command=self.callback.donothing)
        helpmenu.add_command(label="About PyChat", command=self.callback.window_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def tk_gui(self):
        #INIT
        self.root.configure(background='white')
        
        frame1 = Frame(self.root)
        frame2 = Frame(self.root, width=1, height=631, bg='#E6E6E6')
        frame3 = Frame(self.root)
        frame4 = Frame(self.root, width=1, height=631, bg='#E6E6E6')
        frame5 = Frame(self.root)

        frame1.grid(row=0, column=0)
        frame2.grid(row=0, column=1)
        frame3.grid(row=0, column=2)
        frame4.grid(row=0, column=3)
        frame5.grid(row=0, column=4)

        label1 = Label(frame1, text=" Room List", font=("Helvetica Neue", 14), width=24, fg='#333333', bg='white', anchor=W, justify=LEFT, padx=5, pady=5)
        label2 = Label(frame3, text=" "+self.caption+" Release Note", font=("Helvetica Neue", 14), width=64, fg='#333333', bg='white', anchor=W, justify=LEFT, padx=5, pady=5)
        label3 = Label(frame5, text=" User List", font=("Helvetica Neue", 14), width=24, fg='#333333', bg='white', anchor=W, justify=LEFT, padx=5, pady=5)

        label1.grid(row=0, column=0)
        label2.grid(row=0, column=0)
        label3.grid(row=0, column=0)

        #ROOM LIST GUI
        frame_roomlist = Frame(frame1)
        frame_roomlist.grid(row=1, column=0)
        scrollbar1 = Scrollbar(frame_roomlist)
        scrollbar1.pack(side=RIGHT, fill=Y)
        listbox1 = Listbox(frame_roomlist, width=44, height=35, bd=0, highlightthickness=0, activestyle=NONE, selectbackground="#3998D6", selectmode=SINGLE)
        listbox1.pack(side=RIGHT)
        listbox1.config(yscrollcommand=scrollbar1.set)

        for i in range(100):
            listbox1.insert(END, "      Room "+str(i))

        button1 = Button(frame1, text="Create Room", bd=0, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        button1.grid(row=2, column=0)

        #CHAT GUI
        frame_chat = Frame(frame3)
        frame_chat.grid(row=1, column=0)
        scrollbar2 = Scrollbar(frame_chat)
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.chatlog = Text(frame_chat, width=82,height=33, bd=0, padx=20, pady=5, font=("Helvetica Neue", 11))
        self.chatlog.pack(side=RIGHT)
        self.chatlog.config(yscrollcommand=scrollbar2.set)

        if os.path.isfile("readme.txt"):
            f = open("readme.txt")
            for i in f:
                self.chatlog.insert(END, i)
            f.close()

        entry1 = Entry(frame3, width=61, bd=0, font=("Helvetica Neue", 14))
        entry1.grid(row=2, column=0)


        #USER LIST GUI
        frame_roomlist = Frame(frame5)
        frame_roomlist.grid(row=1, column=0)
        scrollbar1 = Scrollbar(frame_roomlist)
        scrollbar1.pack(side=RIGHT, fill=Y)
        listbox1 = Listbox(frame_roomlist, width=44, height=35, bd=0, highlightthickness=0, activestyle=NONE, selectbackground="#3998D6", selectmode=SINGLE)
        listbox1.pack(side=RIGHT)
        listbox1.config(yscrollcommand=scrollbar1.set)

        for i in range(100):
            listbox1.insert(END, "      User "+str(i))

        button1 = Button(frame5, text="Exit Room", bd=0, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        button1.grid(row=2, column=0)
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
