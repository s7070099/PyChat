#!/usr/bin/python
#-*-coding: tis-620 -*-

from socket import *
from thread import *
from time import *
from Tkinter import *

HOST = "192.168.100.70"#HOST = 'infiteam.no-ip.org'
PORT = 50035

nickname = ""
connected = 0
uid = 0

def check_timeout(conn):
    global connected
    global timeout
    timeout = 0
    while 1:
        sleep(1)
        timeout += 1
        if timeout > 5:
            if connected == 0:
                print "Couldn't connect to server. (Connection Timeout)"
            else:
                connected = 0
                print "Connection lost."
                client()
                print "Reconnecting..."
            return

def utf8_encode(text):
    '''
    tmp = ""
    for i in text:
        if ord(i) >= 128:
            print i, ord(i)
            tmp += "chr((%d)" % ord(i-3424)
        else:
            tmp += i
    return tmp
    '''
    return text

def utf8_decode(text):
    '''
    tmp = ""
    ins = ""
    decode = ""
    for i in text:
        if ins != "":
            ins += i
        if i == "c":
            ins = "c"
            decode = ""
        if ins == "":
            tmp += i
        if len(ins) > 5:
            if ins[:5] == "chr((":
                if i == ")":
                    print decode
                    tmp += chr(int(decode))
                    print chr(int(decode))
                    ins = ""
                if i.isdigit() and len(decode) <= 3:
                    decode += i
                else:
                    tmp += ins
                    ins = ""
    return tmp
    '''
    return text

def response(conn):
    global connected
    global timeout
    while 1:
        data = conn.recv(2048)
        if not data: break
        
        data_sector = data.split("[:pack:]")[1::]
        for i in data_sector:
            data = i.split("::::")

            if data[0] == "sv_full":
                print "Couldn't connect to server. (Server is full!)"
                return

            if data[0] == "new":
                global uid
                uid = int(data[1])
                if uid >= 0:
                    connected = 1
                    conn.send("new::::"+str(uid)+"::::"+utf8_encode(nickname))
                    print "Connected."

            if data[0] == "ping":
                timeout = 0

            if data[0] == "say":
                print "[%s] %s" % (utf8_decode(data[1]), utf8_decode(data[2]))
                text.insert(END, "[%s] %s" % (utf8_decode(data[1]), utf8_decode(data[2]))+ "\n")
                text.yview(END)

            if data[0] == "join":
                pass

            if data[0] == "left":
                pass

def client():
    global s
    s = socket(AF_INET, SOCK_STREAM)
    print 'Connecting to %s:%d...' % (HOST, PORT)
    s.connect((HOST, PORT))
    start_new(response, (s,))
    start_new(check_timeout, (s,))

def pychat():
    global nickname

    def getname_callback(event=0):
        global nickname
        nickname = getname.get()
        print "Set name to", nickname
        client()
        root1.destroy()
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
    #root_connect.bind("<Return>", getname_callback)
    #root_connect.mainloop()
    '''

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

    def donothing():
        pass

    #init window
    width, height = 1136,640
    root = Tk()
    root.title("PyChat 0.1")
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('{}x{}'.format(width, height))

    #init menu   
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Connect", command=donothing)
    filemenu.add_command(label="Disconnect", command=donothing)
    filemenu.add_command(label="Server List", command=donothing)
    filemenu.add_command(label="Save as...", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=donothing)
    menubar.add_cascade(label="Connections", menu=filemenu)
    
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)
    menubar.add_cascade(label="Settings", menu=editmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Check for Update", command=donothing)
    helpmenu.add_command(label="About PyChat", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    #frame
    frame_pychat = Frame(root)
    frame_pychat.pack(side=TOP)
    frame_chat = Frame(frame_pychat)
    frame_chat.pack(side=RIGHT)
    frame_chatlog = Frame(frame_chat)
    frame_chatlog.pack(side=TOP)

    scrollbar = Scrollbar(frame_chatlog)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox_user = Listbox(frame_chatlog, width=24, height=38)
    listbox_user.pack(side=RIGHT)
    for i in range(100):
        listbox_user.insert(END, "User #"+str(i))

    listbox_user.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_user.yview)
    
    global text
    scrollbar = Scrollbar(frame_chatlog)
    scrollbar.pack(side=RIGHT, fill=Y)
    text = Text(frame_chatlog, width=90,height=38)
    text.pack(side=RIGHT)
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)

    frame_chatbox = Frame(frame_chat)
    frame_chatbox.pack(side=LEFT)
    label2 = Label(frame_chatbox, text="Chat:")
    label2.pack(side=LEFT)
    getmsg = Entry(frame_chatbox, width=111)
    getmsg.pack(side=LEFT)
    getmsg.delete(0, END)
    getmsg.insert(0, "")
    button_getname = Button(frame_chatbox, text="Send", command=send_callback)
    button_getname.pack(side=LEFT)

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

    #root control
    root.bind("<Return>", send_callback)
    root.mainloop()

pychat()
