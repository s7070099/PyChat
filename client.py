from socket import *
from thread import *
from time import *
from Tkinter import *

HOST = "192.168.100.60"#HOST = '180.183.97.132'
PORT = 50037

nickname = ""
connected = 0
uid = 0

def check_timeout():
    while 1:
        sleep(2)
        

def response(conn):
    global connected
    timeout = 0
    while 1:
        #print timeout
        '''
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
        '''

        data = conn.recv(1024)
        print data
        if not data: break

        data_sector = data.split("[:pack:]")[1::]
        #print data

        for i in data_sector:
            data = i.split("::::")
            #print data

            if data[0] == "sv_full":
                print "Couldn't connect to server. (Server is full!)"
                #client()
                return

            if data[0] == "new":
                global uid
                uid = int(data[1])
                if uid >= 0:
                    connected = 1
                    print nickname
                    conn.send("new::::"+str(uid)+"::::"+nickname)
                    print "Connected."

            if data[0] == "ping":
                timeout = 0

            if data[0] == "say":
                print "[%s] %s" % (data[1], data[2])
                text.insert(END, "[%s] %s" % (data[1], data[2])+ "\n")
                text.yview(END)
                #print "[%s] %s" % (data[1], data[2]), "\n"

'''
def say(conn):
    while 1:
        #print connected
        if connected == 1:
            #print "Says: "
            conn.send("say::::"+str(uid)+"::::"+raw_input())
'''

def client():
    global s
    s = socket(AF_INET, SOCK_STREAM)
    print 'Connecting to %s:%d...' % (HOST, PORT)
    s.connect((HOST, PORT))
    start_new(response, (s,))
    #start_new(say, (s,))

def pychat():
    global nickname
    #print "Nickname: "
    #nickname = raw_input()
    #client()

    def getname_callback():
        global nickname
        nickname = getname.get()
        print "Set name to", nickname
        client()
        root1.destroy()

    root1 = Tk()
    label1 = Label(root1, text="Enter Your Name:")
    label1.pack(side=LEFT)
    getname = Entry(root1)
    getname.pack(side=LEFT)
    getname.delete(0, END)
    getname.insert(0, "")
    button_getname = Button(root1, text="Enter", command=getname_callback)
    button_getname.pack(side=RIGHT)
    root1.bind("<Return>", getname_callback)
    root1.mainloop()

    def send_callback():
        #print connected
        if connected == 1:
            global uid
            s.send("say::::"+str(uid)+"::::"+getmsg.get())
            getmsg.delete(0, END)
            getmsg.insert(0, "")
        else:
            text.insert(END, "Please reconnect.\n")
            text.yview(END)

    root2 = Tk()
    global text
    text = Text(root2)
    #text.insert(INSERT, "Hello.....\n")
    #text.insert(END, "Bye Bye.....\n")
    text.pack()
    #text.tag_add("here", "1.0", "1.4")
    #text.tag_add("start", "1.8", "1.13")
    #text.tag_config("here", background="yellow", foreground="blue")
    #text.tag_config("start", background="black", foreground="green")
    label2 = Label(root2, text="Chat:")
    label2.pack(side=LEFT)
    getmsg = Entry(root2, width=92)
    getmsg.pack(side=LEFT)
    getmsg.delete(0, END)
    getmsg.insert(0, "")
    button_getname = Button(root2, text="Send", command=send_callback)
    button_getname.pack(side=RIGHT)
    root2.bind("<Return>", send_callback)
    root2.mainloop()    

pychat()
