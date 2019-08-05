#==============================================================================
# #Here’s how we begin our server script
#==============================================================================

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#==============================================================================
# #After imports, we set up some constants for later use:
#==============================================================================
clients = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#==============================================================================
# we break our task of serving into accepting new connections, broadcasting messages and handling particular clients. Let’s begin with accepting connections:
#==============================================================================

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave!"+
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        
#==============================================================================
#  This is just a loop that waits forever for incoming connections and as soon as it gets one, it logs the connection (prints some of the connection details) and sends the connected client a welcome message. Then it stores the client’s address in the addresses dictionary and later starts the handling thread for that client. Of course, we haven’t yet defined the target function handle_client() for that, but here’s how we do it:       
#==============================================================================

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
     name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
     while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break
        
#==============================================================================
# Naturally, after we send the new client the welcoming message, it will reply with the name s/he wants to use for further communication. In the handle_client()        
#==============================================================================

#==============================================================================
# Now comes our broadcast() function:
#==============================================================================

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
     for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
        
#==============================================================================
# That was all the required functionalities for our server. Finally, we put in some code for starting our server and listening for incoming connections:        
#==============================================================================

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
    
#==============================================================================
# The Client    
#==============================================================================

#==============================================================================
# we’ll be writing a GUI! We use Tkinter, Python’s “batteries included” GUI building tool for our purpose. Let’s do some imports first:
#==============================================================================

#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

#==============================================================================
# Now we’ll write functions for handling sending and receiving of messages. We start with receive:
#==============================================================================

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break
        
#==============================================================================
# Next, we define the send() function:        
#==============================================================================

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

#==============================================================================
# We define one more function, which will be called when we choose to close the GUI window. It is a sort of cleanup-before-close function and shall close the socket connection before the GUI closes        
#==============================================================================

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()
    
#==============================================================================
#  Now we start building the GUI, in the main namespace (i.e., outside any function). We start by defining the top-level widget and set its title:    
#==============================================================================

top = tkinter.Tk()
top.title("Chatter")

#==============================================================================
# After that, we create a scrollbar for scrolling through this message frame.
#==============================================================================

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

#==============================================================================
# Now we define the message list which will be stored in messages_frame and then pack in (at the appropriate places) all the stuff we’ve created till now:
#==============================================================================

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

#==============================================================================
# After this, we create the input field for the user to input their message, and bind it to the string variable defined above.
#==============================================================================

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

#==============================================================================
# (Almost) done. We haven’t yet written code for connecting to the server. For that, we have to ask the user for the server’s address. I’ve done that by simply using input(), so the user is greeted with some command line prompt asking for host address before the GUI begins.
#==============================================================================

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000  # Default value.
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

#==============================================================================
# Once we get the address and create a socket to connect to it, we start the thread for receiving messages, and then the main loop for our GUI application:
#==============================================================================

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

