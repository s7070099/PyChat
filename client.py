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

VERSION = 0.3
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
                try:
                    self.sock.send(self.data[:len(self.data)-4])
                except:
                    print "Failed to send socket. (Connection lost)"

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
            if self.connected == 2:
                self.old_sock = self.sock
            self.uid = -1
            self.rid = -1
            self.rhost = ""
            self.timeout = 0
            self.threadend = 0
            self.stop = 0

            try:
                self.sock = socket(AF_INET, SOCK_STREAM)
                print 'Connecting to %s:%d...' % (self.ip, self.port)
                self.sock.connect((self.ip, self.port))
                if self.connected == 2:
                    self.old_sock.close()
                    self.stop = 1
                    sleep(1)
                    self.stop = 0
                    self.connected = 1

                self.response_h = start_new(self.response, (self.sock,))
                self.checktimeout_h = start_new(self.checktimeout, (self.sock,))
            except:
                print "Failed to connect."
            

        def close(self):
            sock = self.Sock(self.sock)
            sock.clear()
            sock.add("dis")
            sock.add(self.uid)
            sock.send()
            self.sock.close()
            self.connected = 0
            self.stop = 1
            print "Disconnected."

        def checktimeout(self, conn):
            stop = 0
            while True:
                if stop == 1: return
                #print stop, self.timeout
                stop = self.stop
                if stop == 1: return
                sleep(0.5)
                self.timeout += 0.5
                if self.timeout > 3:
                    if self.connected == 0:
                        self.close()
                        print "Couldn't connect to server. (Connection Timeout)"
                    elif self.connected == 1:
                        self.connected = 2
                        print "Connection lost."

                    if self.connected == 2:
                        print "Reconnecting..."
                        start_new(self.connect, ())

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
                        break

                    if data[0] == "ping":
                        self.timeout = 0
                        break

                    if data[0] == "say":
                        print "[%s] %s" % (data[1], data[2])
                        #text.insert(END, "[%s] %s" % (data[1], data[2])+ "\n")
                        #text.yview(END)
                        break

                    if data[0] == "join":
                        break

                    if data[0] == "left":
                        break

                    if data[0] == "err":
                        print "Kicked from server. (Socket Error)"
                        self.close()
                        break
                    

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
                if self.mainself.network.connected == 2: self.mainself.network.connected = 1
                self.mainself.network.config(ip, port, name)
                self.mainself.network.connect()
                self.root.destroy()
            except:
                print "Could not connect to server."

                
    class Callback(object):
        def window_connect(event, self):
            self.window_connect = self.ConnectWindow(self)

        def window_createroom(event, self):
            def create_room():
                sock = self.network.Sock(self.network.sock)
                sock.add("cr")
                sock.add(self.network.uid)
                sock.add(roomname.get())
                sock.add(password.get())
                sock.send()

            root = Tk()
            root.title("Create Room")
            root.resizable(width=FALSE, height=FALSE)

            frame1 = Frame(root)
            frame1.grid(row=0, padx=10, pady=0)
            label1 = Label(frame1, text="Room Name:")
            label1.grid(row=0, column=0, sticky=W)
            roomname = Entry(frame1, width=64)
            roomname.grid(row=1, column=0)
            label2 = Label(frame1, text="Room Password:")
            label2.grid(row=2, column=0, sticky=W)
            password = Entry(frame1, width=64)
            password.grid(row=3, column=0)

            frame2 = Frame(frame1)
            frame2.grid(row=4, pady=10, sticky=E)
            button1 = Button(frame2, text="Create Room", command=create_room)
            button1.grid(row=0, column=0, padx=10, sticky=E)
            button2 = Button(frame2, text="Cancel", command=root.destroy)
            button2.grid(row=0, column=1, sticky=E)

            root.bind("<Return>", create_room)
            root.mainloop()

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
        self.network.mainself = self
        self.root = Tk()
        self.root.title(CAPTION)
        self.root.resizable(width=FALSE, height=FALSE)
        self.tk_menu()
        self.tk_gui()
        self.root.bind("<Return>", self.callback.send_message)

        start_new(self.check_gui_state, ())
        self.root.mainloop()

    def tk_menu(self):
        menubar = Menu(self.root)
        #menubar.config(bg='white', bd=0)
        
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Connect", command=lambda: self.callback.window_connect(self))
        self.filemenu.add_command(label="Disconnect", command=lambda: self.callback.disconnect(self))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=lambda: self.callback.rootquit(self))
        menubar.add_cascade(label="Connections", menu=self.filemenu)
        
        self.editmenu = Menu(menubar, tearoff=0)
        self.editmenu.add_command(label="Change Name", command=self.callback.donothing)
        menubar.add_cascade(label="Settings", menu=self.editmenu)

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
        self.room = Listbox(frame_roomlist, width=44, height=35, bd=0, highlightthickness=0, activestyle=NONE, selectbackground="#3998D6", selectmode=SINGLE)
        self.room.pack(side=RIGHT)
        self.room.config(yscrollcommand=scrollbar1.set)

        #for i in range(100):
        #    listbox1.insert(END, "      Room "+str(i))

        self.button1 = Button(frame1, text="Create Room", state=DISABLED, bd=0, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1, command=lambda: self.callback.window_createroom(self))
        self.button1.grid(row=2, column=0)

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
                self.log(i)
            f.close()

        self.chatbox = Entry(frame3, width=61, bd=0, font=("Helvetica Neue", 14))
        self.chatbox.grid(row=2, column=0)

        #USER LIST GUI
        frame_userlist = Frame(frame5)
        frame_userlist.grid(row=1, column=0)
        scrollbar3 = Scrollbar(frame_userlist)
        scrollbar3.pack(side=RIGHT, fill=Y)
        self.user = Listbox(frame_userlist, width=44, height=24, bd=0, highlightthickness=0, activestyle=NONE, selectbackground="#3998D6", selectmode=SINGLE)
        self.user.pack(side=RIGHT)
        self.user.config(yscrollcommand=scrollbar3.set)

        #for i in range(100):
        #    listbox2.insert(END, "      User "+str(i))

        #listbox2.delete(0, END)
        self.button2 = Button(frame5, text="Private Message", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button2.grid(row=2, column=0)
        self.button3 = Button(frame5, text="Kick", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button3.grid(row=3, column=0)
        self.button4 = Button(frame5, text="Set Owner", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button4.grid(row=4, column=0)
        self.button5 = Button(frame5, text="Change Room Name", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button5.grid(row=5, column=0)
        self.button6 = Button(frame5, text="Change Room Password", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button6.grid(row=6, column=0)
        self.button7 = Button(frame5, text="Exit Room", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button7.grid(row=7, column=0)

    def log(self, text):
        self.chatlog.config(state=NORMAL)
        self.chatlog.insert(END, text)
        self.chatlog.config(state=DISABLED)

    def check_gui_state(self):
        while True:
            sleep(0.5)
            if self.network.connected == 0 or self.network.connected == 2:
                self.filemenu.entryconfig(1,state=DISABLED)
                self.editmenu.entryconfig(0,state=DISABLED)
                self.button1.config(state=DISABLED)
                self.button2.config(state=DISABLED)
                self.button3.config(state=DISABLED)
                self.button4.config(state=DISABLED)
                self.button5.config(state=DISABLED)
                self.button6.config(state=DISABLED)
                self.button7.config(state=DISABLED)
            else:
                self.filemenu.entryconfig(1,state=NORMAL)
                self.editmenu.entryconfig(0,state=NORMAL)
                if self.network.rid == -1:
                    self.button1.config(state=NORMAL)
                    self.button2.config(state=DISABLED)
                    self.button3.config(state=DISABLED)
                    self.button4.config(state=DISABLED)
                    self.button5.config(state=DISABLED)
                    self.button6.config(state=DISABLED)
                    self.button7.config(state=DISABLED)
                else:
                    self.button1.config(state=DISABLED)
                    self.button2.config(state=NORMAL)
                    self.button3.config(state=DISABLED)
                    self.button4.config(state=DISABLED)
                    self.button5.config(state=DISABLED)
                    self.button6.config(state=DISABLED)
                    self.button7.config(state=NORMAL)
                    if self.network.uid == self.network.rhost:
                        self.button3.config(state=NORMAL)
                        self.button4.config(state=NORMAL)
                        self.button5.config(state=NORMAL)
                        self.button6.config(state=NORMAL)

if __name__ == "__main__":
    App()
