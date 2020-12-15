import socket
import selectors

BUFSIZ = 4096

selfIp = socket.gethostbyname(socket.gethostname())
selfPort = 16384

ip_table = { }
req_table = { }

#socketManager = selectors.DefaultSelector(  )
listener = socket.socket( family = socket.AF_INET, type = socket.SOCK_DGRAM )
listener.bind((selfIp, selfPort))

print('I am', (selfIp, selfPort))

while True:
    msg, addr = listener.recvfrom(BUFSIZ)
    msg = msg.split(';')

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

    elif(query == 'remove'):
        target = msg[2]
        name = msg[3]

    elif(query == 'send'):
        target = msg[2]
        name = msg[3]
        data = msg[4]
