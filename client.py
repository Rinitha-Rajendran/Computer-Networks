import socket
import sys

print("Hello\n")
print("Welcome to our world")
print("Make it yours and take it with you")
print("STAY SAFE WHILE YOU BROWSE \nwith love from Application handlers")

url = input("Enter the URL that you want to know about: \n")
print("1. Basic information about the website")
print("2. Want a screenshot of a website")
print("3. Do you want to send the details to your mail ID?")
print("4. Want to know whether the website belongs to which category")
print("5. Want to know which country server the website belongs to")
print("6. Want to know how many external links are present in the website")
option = int(input("Select an option (1-6): "))

HOST = '127.0.0.1'
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except socket.error as e:
    print(f"Connection error: {str(e)}")
    sys.exit()

if option == 3:
    emailaddr = input("Enter your email address: ")
    message = f"{url}|{option}|{emailaddr}"
else:
    message = f"{url}|{option}"

try:
    client.sendall(message.encode('utf-8'))
    
    if option == 2:
        with open('screenshot.png', 'wb') as img_file:
            imgdata = client.recv(1024 * 1024)
            img_file.write(imgdata)
        print("Screenshot received and saved as 'screenshot.png'.")
    else:
        response = client.recv(1024)
        print("Response from server:", response.decode('utf-8'))

except socket.error as e:
    print(f"Error sending/receiving data: {str(e)}")

finally:
    client.close()
