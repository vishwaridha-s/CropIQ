#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define SOIL_MOISTURE_PIN 34  
#define DHT_PIN 21           
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);


const char* ssid = "Crop";
const char* password = "123456789";


// === Django API endpoint ===
const char* serverUrl = "http://192.168.30.237/fetch/"; // Replace with your actual IP

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Connected to WiFi!");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal Strength (RSSI): ");
  Serial.println(WiFi.RSSI());
}

void sendSensorData(float temperature, float humidity, int moisture) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"temperature\": " + String(temperature, 1) +
                     ", \"humidity\": " + String(humidityx) +
                     ", \"moisture\": " + String(moisture) + "}";

    Serial.println("Sending payload: " + payload);

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.print("✅ HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("📦 Server response: " + response);
    } else {
      Serial.print("❌ Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("❌ WiFi disconnected. Unable to send data.");
  }
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int moisture = analogRead(SOIL_MOISTURE_PIN);  // Reads raw value from 0–4095

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("⚠️ Failed to read from DHT sensor!");
  } else {
    Serial.print("🌡️ Temp: "); Serial.print(temperature);
    Serial.print(" °C | 💧 Humidity: "); Serial.print(humidity);
    Serial.print(" % | 🌱 Moisture: "); Serial.println(moisture);

    sendSensorData(temperature, humidity, moisture);
  }

  delay(10000); // Send every 10 seconds
}
