import socket
import selectors

BUFSIZ = 4096

selfIp = socket.gethostbyname(socket.gethostname())
selfPort = 16384

ip_table = { }
req_table = { }

#socketManager = selectors.DefaultSelector(  )
listener = socket.socket( family = socket.AF_INET, type = socket.SOCK_DGRAM )
listener.bind(("", selfPort))

client = ("106.201.123.139", selfPort) # Replace with your router public IP
# print("punching")
listener.sendto(b'', client)
data, addr = listener.recvfrom(BUFSIZ)
print(addr)
listener.sendto(b'', client)
# print("punched")

listener.setblocking(False)

socketManager = selectors.DefaultSelector()
socketManager.register(listener, selectors.EVENT_READ, True)

print('I am', (selfIp, selfPort))

def networking( ):
    while True:

        for key in req_table:
            if(not (ip_table.get(key, None) is None)):
                for query in req_table[key]:
                    print(query)
                    msg = query[0] + ';' + query[1]
                    if(query[0] == 'create'):
                        for UID in query[2]:
                            msg += ';' + UID

                    elif(query[0] == 'remove'):
                        msg += ';' + query[2]

                    if(query[0] == 'recv'):
                        msg += ';' + 'arandomthing'

                    listener.sendto(msg.encode('utf8'), ip_table[key])

                del query

        events = socketManager.select(timeout = None)
        for(key, mask) in events:
            msg, addr = listener.recvfrom(BUFSIZ)
            if not msg : continue
            msg = (msg.decode()).split(';')

            sender = msg[0] # This is the UID of the sender
            query = msg[1] # This is the actual query of the user

            # Add phone number to table
            if(query == 'online'):
                ip_table.setdefault(sender, addr)
                print(ip_table)

            # Remove phone number to table
            elif(query == 'ofline'):
                ip_table.pop(sender)
                print(ip_table)

            # Create a chatroom with a certain name for a certain user
            elif(query == 'create'):

                target = msg[2]
                name = msg[3]

                UIDs = [sender]
                for UID in msg[4:]: UIDs.append(UID)

                if(req_table.get(target, None) is None):
                    req_table[target] = []
                req_table[target].append(['create', name, UIDs])

            # Remove a person from the chatroom of other people
            elif(query == 'remove'):

                target = msg[2]
                name = msg[3]

                if(req_table.get(target, None) is None):
                    req_table[target] = []
                req_table[target].append(['remove', name, sender])

            # Send a message to a person on a particular chatroom
            elif(query == 'send'):

                target = msg[2]
                name = msg[3]
                data = msg[4]

                if(req_table.get(target, None) is None):
                    req_table[target] = []
                req_table[target].append(['recv', name, sender, data])

networking( )