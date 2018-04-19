import pygame, sys, socket
from PIL import Image

# Create a var for storing an IP address:
ip = str(input("Please enter the IP address: "))

# Start PyGame:
pygame.init()
# Create a PyGame screen, and set its size to 640x480L
screen = pygame.display.set_mode((640, 480))
# Set the window caption:
pygame.display.set_caption('Remote Webcam Viewer')
# Load a font:
font = pygame.font.SysFont("Arial", 14)
# Create a PyGame clock which will be used to limit the fps:
clock = pygame.time.Clock()

# Create some more var's:
timer = 0
previousImage = ""
image = ""

# Main program loop:
while 1:

    # Check if the exit button has been pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # We use a timer to limit how many images we request from the server each second:
    if timer < 1:

        # Create a socket connection for connecting to the server:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((str(ip), 5000))

        # Recieve data from the server:
        data = client_socket.recv(1024000)

        # Set the timer back to 30:
        timer = 30

    else:

        # Count down the timer:
        timer -= 1

    # We store the previous recieved image incase the client fails to recive all of the data for the new image:
    previousImage = image

    # We use a try clause to the program will not abort if there is an error:
    try:

        # We turn the data we revieved into a 120x90 PIL image:
        image = Image.fromstring("RGB", (120, 90), data)

        # We resize the image to 640x480:
        image = image.resize((640, 480))

        # We turn the PIL image into a surface that PyGame can display:
        image = pygame.image.frombuffer(image.tostring(), (640, 480), "RGB")

    except:

        # If we failed to recieve a new image we display the last image we revieved:
        image = previousImage

    # Set the var output to our image:
    output = image

    # We use PyGame to blit the output image to the screen:
    screen.blit(output, (0, 0))

    # We set our clock to tick 60 times a second, which limits the frame rate to that amount:
    clock.tick(60)
    # We update the screen:
    pygame.display.flip()
