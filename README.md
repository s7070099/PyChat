PyChat
======
> *"send chat and remote command."*

An internet connection is required while running this application.

Open and use immediately, No installation required.

##Setting Up a Server
In the Server Folder to include the necessary files.
- ####server.py
> PyChat server python file.<br><br>
**HOST** server ip.<br>
**PORT** server port.<br>
**MAX_USER** server max user.<br>
**MAX_ROOM** server max room.<br>
**SERVER_MSG** server welcome message file.<br>
**SERVER_BAN** server ban list file.<br>
**SERVER_BADWORD** server badword list file.<br>
**SERVER_CMDHELP** server command help file.<br>
**SERVER_CAPTION** server caption.

- ####server_badword.txt
> Badword list, you can config here.

- ####server_ban.txt
> Ban list, by MAC Address.

- ####server_commandhelp.txt
> Command help when user use command /help.

- ####server_msg.txt
> Server welcome message when user connected.

##Client Side
Client need to complie before use because security problem.

####How to
1. Go to "Connection > Connect" to open connect window.
2. Input server ip, port (EXAMPLE 127.0.0.1:12345) and nickname press connect button.
3. Create room by press create button.
4. Enjoy!
