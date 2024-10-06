#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char *ssid = "Free Public Wi-Fi";
const char *password = "2A0R0M4AAN";

ESP8266WebServer server(80);

const int pin1 = 5;  // GPIO5, D1 on NodeMCU
const int pin2 = 4;  // GPIO4, D2 on NodeMCU
const int pin3 = 0;  // GPI00, D3 on NodeMCU
const int pin4 = 2;  // GPI00, D4 on NodeMCU

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Set GPIO pins as outputs
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);

  // Define webpage
  server.on("/", HTTP_GET, handleRoot);
  server.on("/activatePin1", HTTP_GET, activatePin1);
  server.on("/deactivatePin1", HTTP_GET, deactivatePin1);
  server.on("/reversePin1", HTTP_GET, reversePin1);  // New reverse function for Motor 1
  server.on("/activatePin2", HTTP_GET, activatePin2);
  server.on("/deactivatePin2", HTTP_GET, deactivatePin2);
  server.on("/reversePin2", HTTP_GET, reversePin2);  // New reverse function for Motor 2

  // Start server
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP8266 Web Server</h1>";
  html += "<p>Click the buttons to control GPIO pins:</p>";
  html += "<button onclick=\"activatePin(1)\">Activate Forward</button>";
  html += "<button onclick=\"deactivatePin(1)\">Deactivate Forward</button>";
  html += "<button onclick=\"reversePin(1)\">Activate Reverse</button>";  // New reverse button for Motor 1
  html += "<br>";
  html += "<button onclick=\"activatePin(2)\">Activate Left</button>";
  html += "<button onclick=\"deactivatePin(2)\">Deactivate Direction</button>";
  html += "<button onclick=\"reversePin(2)\">Activate Right</button>";  // New reverse button for Motor 2
  html += "<script>function activatePin(pin) {fetch('/activatePin' + pin);}</script>";
  html += "<script>function deactivatePin(pin) {fetch('/deactivatePin' + pin);}</script>";
  html += "<script>function reversePin(pin) {fetch('/reversePin' + pin);}</script>";  // New reverse function call
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void activatePin1() {
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
  digitalWrite(pin3, HIGH);
  digitalWrite(pin4, LOW);
  server.send(200, "text/plain", "Pin 1 activated");
}

void deactivatePin1() {
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, LOW);
  server.send(200, "text/plain", "Pin 1 deactivated");
}

void reversePin1() {
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, HIGH);
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, HIGH);
  server.send(200, "text/plain", "Motor 1 reversed");
}

void activatePin2() {
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
  digitalWrite(pin3, LOW);
  digitalWrite(pin4, LOW);
  server.send(200, "text/plain", "Pin 2 activated");
}

void deactivatePin2() {
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
  digitalWrite(pin3, HIGH);
  digitalWrite(pin4, LOW);
  server.send(200, "text/plain", "Pin 2 deactivated");
}

void reversePin2() {
  digitalWrite(pin3, HIGH);
  digitalWrite(pin4, LOW);
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  server.send(200, "text/plain", "Motor 2 reversed");
}
