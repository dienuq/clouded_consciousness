import cv2
import os
import easyocr
import openai
from pythonosc import udp_client

# Load and set the key for API
openai.api_key = open("text.txt", "r").read().strip("\n")

# Set the path and filename of the image
image_file = "C:/Users/diana/Desktop/ITPMA Master/Anul2/text-recognition/pic3.jpg"

# Read the saved image file
img = cv2.imread(image_file)

# Convert to grayscale and binarize image using threshold
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_img, 210, 255, cv2.THRESH_BINARY)

# Invert binary image
inv_thresh = cv2.bitwise_not(thresh)
cv2.imshow("Binary image", inv_thresh)

# Apply OCR and print the result
reader = easyocr.Reader(['en'], gpu=True)
result = reader.readtext(inv_thresh, detail=0, paragraph=True, text_threshold=0.8)

print("\nScanned text:", result)

# Create the prompt request for API
prompt = "Please classify " + ' '.join(result) + " in one of the Jungian archetypes (Self/Shadow/Anima/Animus/Persona/Trickster) and provide only the name. Always reply with one of those categories, nothing else, no punctuation marks"

print("API Prompt:")
print(prompt)
print("\n")

# Specify request details
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"{prompt}"}],
    temperature=0.9
)

# Estimate the token count (helpful for keeping track of the price)
print("Used tokens:", completion.usage['total_tokens'])

# Get the API answer that is going to be used for mandala
reply_content = completion.choices[0].message.content
print("Archetype:", reply_content)

# OSC setup
client_leds = udp_client.SimpleUDPClient("192.168.1.247", 8888)  # ip and port for ESP8266 to control the LEDs
client_proj = udp_client.SimpleUDPClient("192.168.1.236", 8889)  # ip and port for mandala projection -> TouchDesigner

if reply_content == "Shadow":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/1", reply_content)
    archetype_id = 0
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Anima":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/2", reply_content)
    archetype_id = 1
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Animus":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/3", reply_content)
    archetype_id = 2
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Self":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/4", reply_content)
    archetype_id = 3
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Persona":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/5", reply_content)
    archetype_id = 4
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Mother":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/6", reply_content)
    archetype_id = 5
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Father":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/7", reply_content)
    archetype_id = 6
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Child":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/8", reply_content)
    archetype_id = 7
    client_proj.send_message("/mandala", archetype_id)

if reply_content == "Trickster":
    # Send reply_content via OSC as a string message
    client_leds.send_message("/leds/9", reply_content)
    archetype_id = 8
    client_proj.send_message("/mandala", archetype_id)


# Release the resources
cv2.destroyAllWindows()
