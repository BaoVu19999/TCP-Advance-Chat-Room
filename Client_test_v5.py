
import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5050))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            # If 'NICK' Send Nickname
            if message == 'NICK':
                # it sends back the nickname
                client.send(nickname.encode('ascii'))
                # the next message that comes to the client
                next_message = client.recv(1024).decode('ascii')
                # if it reads PASS
                if next_message == 'PASS':
                    # it should print this
                    print("PASS request recieved") # WHY DOES THIS WORK?
                    # prompt should read this and wait for input of password
                    #client.send(input("Registering, choose password: ").encode('ascii'))
            elif message == 'EXIT':
                raise Exception
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
        
# Sending Messages To Server
def write():
     while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

    # Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
