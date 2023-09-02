//install and use FastLED 3.3(Version)

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <FastLED.h>

#define LED_PIN D2
#define NUM_LEDS 16
#define brightness 100


int hue;
int saturation = 255;
int value = 255;

CRGB leds[NUM_LEDS];

char ssid[] = "Cevrei";   // your network SSID (name)
char pass[] = "vreaunet"; // your network password

WiFiUDP Udp;
const unsigned int localPort = 8888;

void setupLEDs() {
  FastLED.addLeds<WS2811, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear(); // Turn off all LEDs
  FastLED.show();  // Update LEDs
  FastLED.setBrightness(brightness); // brightness 0-255
  FastLED.setCorrection(UncorrectedColor);
}

void setupWifi() {
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting UDP");
  Udp.begin(localPort);
  Serial.print("Local port: ");
  Serial.println(Udp.localPort());
}

void leds_OFF() {
    for (int i = 0; i < NUM_LEDS; i ++)
    {leds[i] = CRGB::Black; // Turn off all LEDs
    FastLED.show();
    }
}

void leds_ON(int hue, int saturation, int value) {
  
    for (int i = 0; i < NUM_LEDS; i += 2) {
      leds[i] = CHSV(hue, saturation, value);    // Turn on current LED
      leds[i + 1] = CHSV(hue, saturation, value);  // Turn on next LED
    FastLED.show();  // Update the LED strip with the new colors
    FastLED.delay(2000);
  }
}

void setup() {
  Serial.begin(115200);
  setupWifi();
  setupLEDs();
  leds_OFF();
}

void processMessage(OSCMessage &msg) {
  if (msg.fullMatch("/leds/0")) {
    leds_OFF();
    Serial.println("Received LEDs OFF");
  } else if (msg.fullMatch("/leds/1")) {
    leds_ON(90, 255, 255);
    Serial.println("Shadow");
  } else if (msg.fullMatch("/leds/2")) {
    leds_ON(190, 255, 255);
    Serial.println("Anima");
  } else if (msg.fullMatch("/leds/3")) {
    leds_ON(116, 255, 255);
    Serial.println("Animus");
  } else if (msg.fullMatch("/leds/4")) {
    leds_ON(0, 0, 255);
    Serial.println("Self");
  } else if (msg.fullMatch("/leds/5")) {
    leds_ON(0, 0, 120);
    Serial.println("Persona");
  } else if (msg.fullMatch("/leds/6")) {
    leds_ON(173, 255, 255);
    Serial.println("Mother");
  } else if (msg.fullMatch("/leds/7")) {
    leds_ON(10, 150, 255);
    Serial.println("Father");
  } else if (msg.fullMatch("/leds/8")) {
    leds_ON(134, 255, 255);
    Serial.println("Child");
  } else if (msg.fullMatch("/leds/9")) {
    leds_ON(35, 255, 255);
    Serial.println("Trickster");
  }
}

void loop() {
  OSCMessage msg;
  int packetSize = Udp.parsePacket();

  if (packetSize > 0) {
    while (packetSize--) {
      msg.fill(Udp.read());
    }

    if (!msg.hasError()) {
      processMessage(msg);
    } else {
      Serial.print("Error while parsing OSC message: ");
      Serial.println(msg.getError());
    }
  }
  
}
