
# ! main loop query format
# Create a chatroom
# 'create';chatroomname;[list of people's UIDs]

# Remove a person from a chatroom
# 'add';chatroomname;toremoveUID

# Add a person to a chatroom
# 'add';chatroomname;newpersonUID

# Add a msg to a chatroom
# todo todo

# ! Server client query format
# Client tells server he is online
# UID;online

# Client tells server he is offline
# UID;ofline

# Client tells server to create a chatroom
# UID;create;targetUID;chatroomname;[; seperated UIDs of members]
# for each targetUID in list of UIDs

# Client tells server to remove themselves from a chatroom
# UID;remove;targetUID;chatroomname
# for each targetUID in list of UIDs

# Client tells server to add a person to a chatroom
# UID;addper;targetUID;chatroomname;newpersonUID
# for each targetUID in people in the chatroom

# Client send a message on a particular chatroom
# UID;send;targetUID;chatroomname;time;msg
# for each targetUID in people in the chatroom

import socket
import selectors

delim = ';'

BUFSIZ = 4096

selfIp = socket.gethostbyname(socket.gethostname())
selfPort = 25000

ip_table = { }
req_table = { }

listener = socket.socket( family = socket.AF_INET, type = socket.SOCK_DGRAM )
listener.bind(("", selfPort))

whitelisted_ips = ["106.201.123.139", "106.200.238.248", "49.207.201.183", "49.37.170.237", "49.207.201.250", "171.61.90.0", "49.207.223.177", "122.178.254.251", "49.37.166.91"]

listener.setblocking(False)

socketManager = selectors.DefaultSelector()
socketManager.register(listener, selectors.EVENT_READ, True)

print('I am', (selfIp, selfPort))

def tokenize( obj ):
    obj = obj.decode()
    tokens = [elem.strip() for elem in obj.split(delim)]
    print(tokens)
    return tokens

def deTokenize( tokens ):
    # for i in range(len(tokens)): tokens[i] = tokens[i].strip()
    msg = delim.join(tokens)
    print(msg)
    return msg.encode('utf-8')

def networking( ):
    # for ip in whitelisted_ips:  listener.sendto(b'', (ip, selfPort))
    for key in req_table:
        if(ip_table.get(key, None)):
            for query in req_table[key]:
                print(query)
                msg = deTokenize(query)
                listener.sendto(msg, ip_table[key])

            req_table[key] = []

    events = socketManager.select(timeout = 0.01)

    for (key, mask) in events:
        msg, addr = listener.recvfrom(BUFSIZ)
        print('msg:', msg)
        print('addr:', addr)
        if msg:
            tokens = tokenize(msg)

            sender = tokens[0]
            query = tokens[1]

            # Add UID to table
            if(query == 'online'):
                ip_table.setdefault(sender, addr)
                print(ip_table)

            # Remove UID from table
            elif(query == 'ofline'):
                try:
                    ip_table.pop(sender)
                except Exception as e:
                    print(e)
                print(ip_table)

            else:
                target = tokens[2]
                print(target)
                room_name = tokens[3]

                request = [query, room_name]

                if(req_table.get(target, None) is None): req_table[target] = []

                if(query == 'create'):
                    people = tokens[4:]
                    # request.append(people)
                    request += people
                elif(query == 'addper'):
                    newPerson = tokens[4]
                    request.append(newPerson)
                elif(query == 'remper'):
                    toRemove = tokens[4]
                    request.append(toRemove)
                elif(query == 'addmsg'):
                    timestamp = tokens[4]
                    message = tokens[5]
                    request += [timestamp, sender, message]

                req_table[target].append(request)

while True: networking( )