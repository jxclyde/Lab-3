from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import mycipher

key = 0
BUFSIZ = 1024
encryptionMode = "OFF"


def receive():
    """Handles receiving of messages."""

    global encryptionMode
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if ":" in msg:
                splt_msg = msg.split(':', 1)
                if encryptionMode == "ON":
                    msg = decrypt(splt_msg[1])
                else:
                    msg = splt_msg[1]
                msg_list.insert(tkinter.END, splt_msg[0] + ":" + msg)
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    """Handles sending of messages."""

    global encryptionMode
    msg = my_msg.get()
    if msg == "{quit}":
        client_socket.send(bytes(msg, "utf8"))
        client_socket.close()
        top.quit()
        return
    elif msg == "{encryption on}":
        encryptionMode = "ON"
        my_msg.set("")
        msg_list.insert(tkinter.END, "From now on all messages are now encrypted!")
        return
    elif msg == "{encryption off}":
        encryptionMode = "OFF"
        my_msg.set("")
        msg_list.insert(tkinter.END, "From now on all messages are not encrypted.")
        return
    elif encryptionMode == "ON":
        msg = encrypt(msg)

    client_socket.send(bytes(msg, "utf8"))
    my_msg.set("")

def decrypt(msg):
    print(msg)
    return mycipher.decrypt_message(key, msg)

def encrypt(msg):
    print(msg)
    return mycipher.encrypt_message(key, msg)

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)



HOST = input('Enter host: ')
PORT = input('Enter port: ')
key = mycipher.get_key()
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
if not HOST:
    HOST = "127.0.0.1"

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()