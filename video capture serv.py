import socket
from VideoCapture3 import *
from PIL import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5000))
server_socket.listen(5)

print("Your IP address is: ", socket.gethostbyname(socket.gethostname()))

camera = Device()

image = camera.getImage()

print("Server Waiting for client on port 5000")

while 1:
    client_socket, address = server_socket.accept()

    image = camera.getImage().convert("RGB")

    image = image.resize((120, 90))

    # image.save("webcam.jpg")

    data = image.tostring()

    client_socket.sendall(data)
