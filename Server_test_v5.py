
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 5050

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind host and port together
server.bind((host, port))

#listen to client 
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    
    # for every client in the list of those connected
    for client in clients:
        # send them the passed in message
        client.send(message)

# takes the client and the nickname of the client
def register(client, nick):
    
    # opens the chat room login file to append
     with open('Chat_room_login.txt', 'a') as f:
             print("registering")
             
             # sends request for a password to the client
             client.send('PASS'.encode('ascii'))
             
             # saves the response as the variable password
             password = client.recv(1024).decode("ascii")
             print("recieved pass")
             
             # writes the nickname to the file
             f.write(nick)
             
             # space to identfy both parts
             f.write(" ")
             
             # appends after name the password
             f.write(password)
             
             # new line
             f.write("\n")

        
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # message comes in from client
            message = client.recv(1024)
            exit_command = message.split()
            print(exit_command[1])


            # if the message starts with '@'
            if message.split()[1][0] == 64:
            #if message.split()[1][0] == '@':
                
                # checks all the nicknames
                for nick in nicknames:

                    # create Direct message command by @<nickname>
                    # looks if it matches those on the nickname list
                    if (f"b'@{nick}'") == f'{message.split()[1]}':
                        # if it does, communicates only with that same client, by using the same index of the clients list
                        clients[nicknames.index(nick)].send(message)

               #create Exit command          
            elif f'{exit_command[1]}' == "b'EXIT'":
                client.send('EXIT'.encode('ascii'))
                raise Exception



            else:
                # or it sends to everyone in the chat room
                broadcast(message)
                
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()

            #send broadcast message to all clients that a person left the chatroom
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            print(f'{nickname} has left!')
            nicknames.remove(nickname)
            break
        
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        
        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        
        # the response from the client
        nickname = client.recv(1024).decode('ascii')
        
        # start the login process, new login or old and password request
        login(client,nickname)
        
        # informs the nickname of new attendee
        print("Nickname is {}".format(nickname))
        
        # once login over anouce chat room attendee
        broadcast("{} joined!".format(nickname).encode('ascii'))
        
        # sends message to client that they are now in the room
        client.send('Connected to server!'.encode('ascii'))
        
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# passes in the nickname and the socket infromation
def login(client,nickname):
    
    # checkes the chat room login file
    file = open("Chat_room_login.txt", "r")
    for credentials in file.readlines():
        
        # spliting up the lines in the file for nick name and password
        search_nick = credentials.split()
        print("searching creds")
        
        # if the first part of the file entry matches the nickname
        if nickname == search_nick[0]:
            
            # will ask for password
            client.send('PASS'.encode('ascii'))
            print("verify password")
            
            # waits to recieve the password
            password = client.recv(1024).decode('ascii')
            
            # loops until broken
            while (True):
                print("insided loop")
                
                # if the password does not match the second part of the file entry
                if f'{password}' != f'{search_nick[1]} {search_nick[2]}':
                    
                    # makes them try again
                    print("Wrong password, try again")
                   # print("----------------------------")
                    #print("sent password: " + password)
                    #print("search_nick[1]: " + search_nick[1])
                    #print("files saved: " + search_nick[2])
                    #print("if statement: " + search_nick[1] + " " + password +" != " + search_nick[2])
                    #print("----------------------------")
                    password = client.recv(1024).decode('ascii')
                    
                else:
                    # if it does match it breaks the loop after appending to the lists
                    nicknames.append(nickname)
                    clients.append(client)
                    print("Logged in")
                    return
        else:
            # if loop through file entries find no simular name, register them
            register(client, nickname)
            nicknames.append(nickname)
            clients.append(client)
            print("Registered")
            print("Logged in")
            return

    nicknames.append(nickname)
    clients.append(client)

print("server is listening....")
receive()
