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
            self.roomlist = list()
            self.userlist = list()

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

                self.netsock = self.Sock(self.sock)
                self.response_h = start_new(self.response, (self.sock,))
                self.checktimeout_h = start_new(self.checktimeout, (self.sock,))
            except:
                print "Failed to connect."
            

        def close(self):
            self.mainself.user.delete(0, END)
            self.mainself.room.delete(0, END)
            self.mainself.log_readme()
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
                        self.mainself.log_readme()
                        print "Connection lost."

                    if self.connected == 2:
                        print "Reconnecting..."
                        start_new(self.connect, ())

        def response(self, conn):
            def user_text(idx, name, owner=0):
                tmp_text = "      [ID" + " " + str(idx) + "] " + str(name)
                if owner == 1:
                    tmp_text += " (Owner)"
                return tmp_text
            
            sock = self.Sock(conn)
            while True:
                data = conn.recv(4096)
                if not data: break

                data_sector = data.split("[:pack:]")[1:]
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
                            self.mainself.user.delete(0, END)
                            print "Connected."

                    if data[0] == "sv_msg":
                        self.mainself.room.config(state=NORMAL)
                        self.mainself.user.config(state=NORMAL)
                        self.mainself.log_clear()
                        self.mainself.server_message = list()
                        self.mainself.server_caption = data[1]
                        self.mainself.chatlabel.config(text=data[1])
                        for i in xrange(2, len(data)):
                            tmp = data[i].replace("\n","")
                            self.mainself.server_message.append(tmp)
                            self.mainself.log(str(tmp))
                        self.mainself.log("")

                    if data[0] == "sv_msg_add":
                        for i in xrange(1, len(data)):
                            tmp = data[i].replace("\n","")
                            self.mainself.server_message.append(tmp)
                            self.mainself.log(tmp)
                        self.mainself.log("")

                    if data[0] == "print":
                        self.mainself.log(data[1], 1)

                    if data[0] == "rm_list":
                        self.timeout = 0
                        self.roomlist = list()
                        self.mainself.room.delete(0, END)
                        for i in xrange(1, len(data), 2):
                            self.roomlist.append(data[i])
                            self.mainself.room.insert(END, "      "+str(data[i+1]))

                    if data[0] == "rm_request":
                        if data[1] == "0":
                            self.request_rid = data[2]
                            self.mainself.callback.window_enterpw(self.mainself)
                        if data[1] == "1":
                            self.mainself.log("Wrong Password!")

                    if data[0] == "rm_join":
                        self.rid = data[1]
                        self.rhost = data[2]
                        self.mainself.log_clear()
                        self.mainself.chatlabel.config(text=data[3])
                        if int(self.uid) != int(self.rhost):
                            self.userlist = list()
                            self.mainself.user.delete(0, END)
                            for i in xrange(5, len(data)-1, 2):
                                self.userlist.append(data[i])
                                tmp_text = user_text(data[i], data[i+1], 0)
                                if int(data[i]) == int(self.rhost):
                                    tmp_text = user_text(data[i], data[i+1], 1)
                                self.mainself.user.insert(END, tmp_text)
                        else:
                            self.userlist.append(self.uid)
                            self.mainself.user.insert(END, user_text(self.uid, self.nickname, 1))

                    if data[0] == "rm_adduser":
                        tmp_text = user_text(data[1], data[2], 0)
                        self.mainself.user.insert(END, tmp_text)
                        self.userlist.append(data[1])

                    if data[0] == "rm_deluser":
                        self.mainself.user.delete(self.userlist.index(data[1]))
                        self.userlist.remove(data[1])

                    if data[0] == "rm_chowner":
                        print data
                        print self.userlist
                        print "--------------------"
                        idx = self.userlist.index(data[1])
                        self.mainself.user.delete(idx)
                        tmp_text = user_text(data[1], data[2], 1)
                        if int(data[1]) == int(self.uid):
                            self.mainself.user.insert(idx, tmp_text)

                    if data[0] == "rm_kick":
                        self.network.rid = -1
                        self.network.select_uid = -1
                        self.network.userlist = list()
                        self.mainself.user.delete(0, END)
                        self.log_servermessage()
                        print "you were kicked from the room."

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
            name = self.name.get()
            if host_str != "" and name != "":
                host = host_str.split(":")
                ip = host[0]
                if len(host) == 2:
                    port = int(host[1])
                else:
                    port = 12345
                
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
                sock.add("rm_create")
                sock.add(self.network.uid)
                sock.add(roomname.get())
                sock.add(password.get())
                sock.send()
                root.destroy()

            root = Tk()
            root.title("Create Room")
            root.resizable(width=FALSE, height=FALSE)

            frame1 = Frame(root)
            frame1.grid(row=0, padx=10, pady=0)
            label1 = Label(frame1, text="Room Name:")
            label1.grid(row=0, column=0, sticky=W)
            roomname = Entry(frame1, width=64)
            roomname.grid(row=1, column=0)
            roomname.insert(0, self.network.nickname + "'s Room")
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

        def window_enterpw(self, mainself):
            def join_room():
                sock = self.network.Sock(self.network.sock)
                sock.add("rm_request")
                sock.add(self.network.uid)
                sock.add(self.network.request_rid)
                sock.add(password.get())
                sock.send()
                root.destroy()

            root = Tk()
            root.title("Enter Password")
            root.resizable(width=FALSE, height=FALSE)

            frame1 = Frame(root)
            frame1.grid(row=0, padx=5, pady=5)
            roomname = Entry(frame1, width=32, font=("Helvetica Neue", 13))
            roomname.grid(row=0, column=0)

            button1 = Button(frame1, text="Enter", command=join_room)
            button1.grid(row=0, column=1)

            root.bind("<Return>", join_room)
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

        def donothing(event):
            pass

        def send_message(self, event, mainself):
            text = mainself.chatbox.get()
            if len(text) == 0: return
            if text[0] == "/":
                cmd = text[1:].split(" ")
                if cmd[0] == "clear":
                    mainself.log_clear()
                elif cmd[0] == "debug":
                    pass
                else:
                    if mainself.network.connected == 1:
                        sock = mainself.network.Sock(mainself.network.sock)
                        sock.add("exc")
                        sock.add(mainself.network.uid)
                        sock.add(cmd[0])
                        if len(cmd) > 1:
                            for i in cmd[1:]:
                                sock.add(i)
                        sock.send()
                    else:
                        mainself.log("Unknown Command: " + text, 1)
            else:
                if mainself.network.connected == 1:
                    sock = mainself.network.Sock(mainself.network.sock)
                    sock.add("say")
                    sock.add(mainself.network.uid)
                    sock.add(text)
                    sock.send()
            mainself.history.append(text)
            mainself.history_max += 1
            mainself.history_idx = mainself.history_max
            mainself.chatbox.delete(0, END)
            mainself.chatbox.insert(0, "")

        def history_up(self, event, mainself):
            if mainself.history_idx > 0:
                mainself.history_idx -= 1
                mainself.chatbox.delete(0,END)
                mainself.chatbox.insert(0,mainself.history[mainself.history_idx])

        def history_down(self, event, mainself):
            mainself.chatbox.delete(0,END)
            if mainself.history_idx < mainself.history_max-1:
                mainself.history_idx += 1
                mainself.chatbox.insert(0,mainself.history[mainself.history_idx])

        def room_select(self, event, mainself):
            if mainself.network.connected == 1 and len(mainself.network.roomlist) > 0:
                widget = event.widget
                index = int(widget.curselection()[0])
                #value = widget.get(index)
                if index == int(mainself.network.rid):
                    mainself.log("You are already in this room.")
                else:
                    sock = mainself.network.Sock(mainself.network.sock)
                    if int(mainself.network.rid) != -1:
                        sock.add("rm_deluser")
                        sock.add(mainself.network.uid)
                        sock.send()
                        
                    mainself.select_uid = -1
                    sock.clear()
                    sock.add("rm_request")
                    sock.add(mainself.network.uid)
                    sock.add(mainself.network.roomlist[index])
                    sock.send()

        def pm(event, self):
            if self.network.connected == 1 and int(self.network.select_uid) != -1:
                self.chatbox.delete(0, END)
                self.chatbox.insert(0, "/pm "+ str(self.network.select_uid) + " ")

        def kick(event, self):
            if self.network.connected == 1 and int(self.network.select_uid) != -1:
                sock = self.network.netsock
                sock.add("kick")
                sock.add(self.network.uid)
                sock.add(self.network.macaddr)
                sock.add(self.network.select_uid)
                sock.send()

        def owner(event, self):
            if self.network.connected == 1 and int(self.network.select_uid) != -1:
                sock = self.network.netsock
                sock.add("rm_chowner")
                sock.add(self.network.uid)
                sock.add(self.network.macaddr)
                sock.add(self.network.select_uid)
                sock.send()

        def rm_chname(event, self):
            if self.network.connected == 1 and int(self.network.select_uid) != -1:
                self.chatbox.delete(0, END)
                self.chatbox.insert(0, "/set roomname "+ str(self.network.select_uid) + " ")

        def rm_chpass(event, self):
            if self.network.connected == 1 and int(self.network.select_uid) != -1:
                self.chatbox.delete(0, END)
                self.chatbox.insert(0, "/set roompass "+ str(self.network.select_uid) + " ")

        def rm_exit(event, self):
            if self.network.connected == 1 and int(self.network.rid) != -1:
                sock = self.network.netsock
                sock.add("rm_deluser")
                sock.add(self.network.uid)
                sock.send()
                self.network.rid = -1
                self.network.select_uid = -1
                self.network.userlist = list()
                self.user.delete(0, END)
                self.log_servermessage()

        def user_select(self, event, mainself):
            if mainself.network.connected == 1 and len(mainself.network.roomlist) > 0:
                widget = event.widget
                index = int(widget.curselection()[0])
                #value = widget.get(index)
                mainself.network.select_uid = mainself.network.userlist[index]

        def rootquit(event, self):
            self.root.destroy()
            pass
    
    def __init__(self):
        CAPTION = "PyChat v." + str(VERSION)

        self.caption = CAPTION
        self.chatcaption = self.caption+" Release Note"
        self.callback = self.Callback()
        self.network = self.Network()
        self.network.mainself = self
        self.history = list()
        self.history_idx = 0
        self.history_max = 0
        self.root = Tk()
        self.root.title(CAPTION)
        self.root.resizable(width=FALSE, height=FALSE)
        self.tk_menu()
        self.tk_gui()
        self.root.bind("<Return>", lambda event: self.callback.send_message(event, self))
        self.root.bind("<Up>", lambda event: self.callback.history_up(event, self))
        self.root.bind("<Down>", lambda event: self.callback.history_down(event, self))

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
        helpmenu.add_command(label="Check for Update", command=lambda: self.callback.window_enterpw(self))
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
        self.chatlabel = Label(frame3, text=" "+self.chatcaption, font=("Helvetica Neue", 14), width=64, fg='#333333', bg='white', anchor=W, justify=LEFT, padx=5, pady=5)
        label3 = Label(frame5, text=" User List", font=("Helvetica Neue", 14), width=24, fg='#333333', bg='white', anchor=W, justify=LEFT, padx=5, pady=5)

        label1.grid(row=0, column=0)
        self.chatlabel.grid(row=0, column=0)
        label3.grid(row=0, column=0)

        #ROOM LIST GUI
        frame_roomlist = Frame(frame1)
        frame_roomlist.grid(row=1, column=0)
        scrollbar1 = Scrollbar(frame_roomlist)
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.room = Listbox(frame_roomlist, width=44, height=35, bd=0, highlightthickness=0, activestyle=NONE, selectbackground="#3998D6", selectmode=SINGLE)
        self.room.pack(side=RIGHT)
        self.room.config(yscrollcommand=scrollbar1.set)
        self.room.bind('<<ListboxSelect>>', lambda event: self.callback.room_select(event, self))

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

        self.readme = list()
        if os.path.isfile("readme.txt"):
            f = open("readme.txt")
            for i in f:
                self.readme.append(i.replace("\n",""))
                self.log(i.replace("\n",""))
            self.log("")
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
        self.user.bind('<<ListboxSelect>>', lambda event: self.callback.user_select(event, self))

        #for i in range(100):
        #    listbox2.insert(END, "      User "+str(i))

        #listbox2.delete(0, END)
        self.button2 = Button(frame5, command=lambda : self.callback.pm(self), text="Private Message", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button2.grid(row=2, column=0)
        self.button3 = Button(frame5, command=lambda : self.callback.kick(self), text="Kick", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button3.grid(row=3, column=0)
        self.button4 = Button(frame5, command=lambda : self.callback.owner(self), text="Set Owner", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button4.grid(row=4, column=0)
        self.button5 = Button(frame5, command=lambda : self.callback.rm_chname(self), text="Change Room Name", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button5.grid(row=5, column=0)
        self.button6 = Button(frame5, command=lambda : self.callback.rm_chpass(self), text="Change Room Password", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button6.grid(row=6, column=0)
        self.button7 = Button(frame5, command=lambda : self.callback.rm_exit(self), text="Exit Room", bd=0, state=DISABLED, font=("Helvetica Neue", 14), width=24, fg='#4D89C1', bg='white', anchor=N, justify=CENTER, padx=5, pady=1)
        self.button7.grid(row=7, column=0)

    def log_servermessage(self):
        self.chatlabel.config(text=self.server_caption)
        self.log_clear()
        for i in self.server_message:
            self.log(i)

    def log_readme(self):
        self.chatlabel.config(text=self.chatcaption)
        self.log_clear()
        for i in self.readme:
            self.log(i)
    
    def log_clear(self):
        self.chatlog.config(state=NORMAL)
        self.chatlog.delete("1.0", END)
        self.chatlog.config(state=DISABLED)

    def log(self, text, newline=0):
        self.chatlog.config(state=NORMAL)
        self.chatlog.insert(END, text+"\n")
        self.chatlog.config(state=DISABLED)
        if newline: self.chatlog.yview(END)

    def check_gui_state(self):
        while True:
            sleep(0.5)
            try:
                if self.network.connected == 0 or self.network.connected == 2:
                    self.filemenu.entryconfig(1,state=DISABLED)
                    self.editmenu.entryconfig(0,state=DISABLED)
                    self.room.config(state=DISABLED)
                    self.user.config(state=DISABLED)
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
                    if int(self.network.rid) == -1:
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
                        if int(self.network.uid) == int(self.network.rhost):
                            self.button3.config(state=NORMAL)
                            self.button4.config(state=NORMAL)
                            self.button5.config(state=NORMAL)
                            self.button6.config(state=NORMAL)
            except:
                pass

if __name__ == "__main__":
    App()


