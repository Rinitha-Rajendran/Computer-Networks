import socket
import sys
from _thread import *
from basicinformation import extracttext
from screenshotfunc import screenshot
from emailcode import sendemail
from country import countryweb
from ml import mlmodel
from external import externllinks

HOST = '192.168.169.243'
PORT = 1234

server = socket.socket()
try:
    server.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
    sys.exit()

print("Waiting for connection")
server.listen(5)

def clienthandler(connection):
    while True:
        data = connection.recv(4096)
        if not data:
            break

        messageparts = data.decode("utf-8").split('|')
        if len(messageparts) >= 2:
            url = messageparts[0]
            option = messageparts[1]

            if option == '1':
                reply = extracttext(url)
            elif option == '2':
                filename = 'screenshot.png'
                screenshot(url, filename)
                with open(filename, 'rb') as img_file:
                    while chunk := img_file.read(2048):
                        connection.sendall(chunk)
                continue

            elif option == '3' and len(messageparts) == 3:
                emailaddress = messageparts[2]
                details = extracttext(url)
                subject = "Website Details"
                filename='screenshot.png'
                screenshot(url,filename)
                sendemail(emailaddress, subject,details,filename)
                reply = f"Details sent to {emailaddress}."
            elif option=='4':
                reply=mlmodel(url)

            elif option=='5':
                reply=countryweb(url)
            elif option=='6':
                reply=externllinks(url)
               
            else:
                reply = 'Invalid option.\n'
        else:
            reply = "Invalid data received.\n"
        
        connection.sendall(reply.encode('utf-8'))

    connection.close()

while True:
    client, addr = server.accept()
    print("Connected to: " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clienthandler, (client,))