import cv2
import os
import easyocr
import openai
import time
from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer



# load and set the key for API
openai.api_key = open("text.txt", "r").read().strip("\n")

# Initialize the video capture device
cap = cv2.VideoCapture(0)

# Create a window to display the webcam feed
#cv2.namedWindow("Live Feed", cv2.WINDOW_NORMAL)

# Set the name of the folder
image_folder = "images"

# Set up UDP clients for sending OSC messages
client_leds = udp_client.SimpleUDPClient("192.168.1.247", 8888)
client_proj = udp_client.SimpleUDPClient("192.168.1.236", 8889)
client_tablet = udp_client.SimpleUDPClient("192.168.1.222", 12000)

# Ensure the folder exists or create it
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    

def analyze_handler(address, *args):
    print("Received OSC message:", address)
    
    # Capture a frame
    ret, frame = cap.read()
    
   # Get the list of existing image files
    existing_images = [f for f in os.listdir(image_folder) if f.endswith(".jpg")]
    existing_image_numbers = [int(f.split(".")[0]) for f in existing_images]

    # Find the next available image number
    if existing_image_numbers:
        next_image_number = max(existing_image_numbers) + 1
    else:
        next_image_number = 1

    # Create the full path for the next image
    next_image_path = os.path.join(image_folder, f"{next_image_number}.jpg")

    # Save the frame as an image
    cv2.imwrite(next_image_path, frame)
    print("Photo saved as {}".format(next_image_path))

    # Read the saved image file
    img = cv2.imread(next_image_path)

    # Convert to grayscale and binarize image using threshold
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_img, 210, 255, cv2.THRESH_BINARY)

    # Invert binary image
    inv_thresh = cv2.bitwise_not(thresh)
    #cv2.imshow("Binary image",inv_thresh)
    #cv2.imwrite("images/binar.jpg", inv_thresh)

    # Apply OCR and print the result
    reader = easyocr.Reader(['en'],gpu=True)
    result = reader.readtext(inv_thresh, detail=0, paragraph=True, text_threshold=0.8)

    print("\n")
    print("Sand text: ", result)
    
    
    # create the prompt request for API
    prompt = "Please classify " + ' '.join(result) + " in one of the Jungian archetypes(Self/Shadow/Anima/Animus/Persona/Parent/Child/Trickster) and provide only the category. Always reply with one of those categories, nothing else"
    
    print("API Prompt:")
    print(prompt)
    print("\n")

    # specify request details
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
    messages=[{"role": "user", "content": f"{prompt}"}],
    temperature=0.9
    )

    # estimate the tokens number | helpful for keeping track of the price
    print("Used tokens: ", completion.usage['total_tokens'])

    # the API answer that is going to be used for mandala
    reply_content = completion.choices[0].message.content
    print("Archetype: ", reply_content)

    if reply_content == "Shadow":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/1", reply_content)
        archetype_id = 0
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/0", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Anima":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/2", reply_content)
        archetype_id = 1
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/1", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Animus":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/3", reply_content)
        archetype_id = 2
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/2", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Self":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/4", reply_content)
        archetype_id = 3
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/3", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Persona":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/5", reply_content)
        archetype_id = 4
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/4", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Parent":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/6", reply_content)
        archetype_id = 5
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/5", archetype_id)
        #time.sleep(180)
        #client_tablet.send_message("/reset", archetype_id)

    if reply_content == "Child":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/7", reply_content)
        archetype_id = 6
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/6", archetype_id)
        #time.sleep(180)
       # client_tablet.send_message("/reset", archetype_id)

    #if reply_content == "Child":
        # Send reply_content via OSC as a string message 
    #   client_leds.send_message("/leds/8", reply_content)
    #  archetype_id = 7
    # client_proj.send_message("/mandala", archetype_id)

    if reply_content == "Trickster":
        # Send reply_content via OSC as a string message
        client_leds.send_message("/leds/9", reply_content)
        archetype_id = 7
        client_proj.send_message("/mandala", archetype_id)
        client_tablet.send_message("/mandala/7", archetype_id)
       # time.sleep(180)
       # client_tablet.send_message("/reset", archetype_id)

# OSC setup
dispatcher = Dispatcher()
dispatcher.map("/analyze", analyze_handler)

ip = "192.168.1.236"
port = 8887

server = BlockingOSCUDPServer((ip, port), dispatcher)
server.serve_forever() # Blocks forever






# Release the video capture device and destroy the window
cap.release()
cv2.destroyAllWindows()
