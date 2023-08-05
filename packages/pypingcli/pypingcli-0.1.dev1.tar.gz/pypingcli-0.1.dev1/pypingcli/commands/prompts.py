import globals
import sys
import pypingcli.sockets
import pypingcli.util
from pypingcli.messaging.socketAction import sendMsg
def invokePrompt():
    """State based prompt calls."""
    commands = []
    if globals.state['connected'] == True:
        commands = ['send','disconnect']
        run = printPrompt(commands)
        if run == -1:
            return -1
        elif run == "send":
            sendMsg()
        
    else:
        commands = ['Connect','Accept','Go online','Edit username',]
        run = printPrompt(commands)
        threadVar = None
        if run == -1:
            return -1
        elif run == "Connect":
            pypingcli.sockets.chat_client()
            # pypingcli.sockets.server.test()
            # print("threadVar.isAlive()",threadVar.isAlive() if threadVar else "None")
            # sockets.Client()
        # elif run == "ter":
        #     globals.state['connected'] = 't'
        elif run == "Accept":
            # threadVar = pypingcli.sockets.util.startDaemonServer()
            pypingcli.sockets.chat_server()
            # sockets.Server()
            # pass
        elif run == 'Edit username':
            globals.user = pypingcli.util.safeInput(message="\rNew Username.>")
        elif run == 'Go online':
            pypingcli.sockets.chat_client(globals.internetServerIP)


def printPrompt(options):
    """Prints, validates and returns options."""
    print "Commands : 0) Quit ",
    for index,command in enumerate(options,1):
        print "{}){} ".format(index,command) ,
    invFlag = True
    while invFlag:
        tmpInput = None
        try:
            tmpInput = int(input("\n: "))
        except:
            pass
        if tmpInput >= 0 and tmpInput<=len(options):
            break
        print("Invalid Option.")
        
    if tmpInput == 0:
        return -1
    return options[tmpInput-1]