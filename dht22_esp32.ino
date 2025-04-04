#include <DHT.h>

// Define DHT22 sensor pins
#define DHTPIN1 2     // GPIO 2
#define DHTPIN2 4     // GPIO 4
#define DHTPIN3 5     // GPIO 5
#define DHTTYPE DHT22

// Initialize DHT sensors
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);
DHT dht3(DHTPIN3, DHTTYPE);

void setup() {
  Serial.begin(115200);
  
  // Initialize all sensors
  dht1.begin();
  dht2.begin();
  dht3.begin();
  
  delay(2000); // Wait for sensors to stabilize
}

void loop() {
  // Read values from all three sensors
  float h1 = dht1.readHumidity();
  float t1 = dht1.readTemperature();
  float h2 = dht2.readHumidity();
  float t2 = dht2.readTemperature();
  float h3 = dht3.readHumidity();
  float t3 = dht3.readTemperature();

  // Check if any reads failed
  if (isnan(h1) || isnan(t1) || isnan(h2) || isnan(t2) || isnan(h3) || isnan(t3)) {
    Serial.println("0,0,0,0,0,0"); // Send zeros if reading failed
  } else {
    // Send data in format: humidity1,temperature1,humidity2,temperature2,humidity3,temperature3
    Serial.print(h1);
    Serial.print(",");
    Serial.print(t1);
    Serial.print(",");
    Serial.print(h2);
    Serial.print(",");
    Serial.print(t2);
    Serial.print(",");
    Serial.print(h3);
    Serial.print(",");
    Serial.println(t3);
  }

  delay(2000); // Wait 2 seconds between measurements
}
