#include <HX710B.h>

const int sensorDOUTPins[6] = {2, 3, 4, 5, 6, 7};  // DOUT pins for each sensor
const int sensorSCKPins[6] = {8, 9, 10, 11, 12, 13}; // SCK pins for each sensor

HX710B pressureSensors[6];  

void setup() {
    Serial.begin(115200);
    Serial.println("Initializing HX710B Pressure Sensors...");

    // Initialize each sensor
    for (int i = 0; i < 6; i++) {
        pressureSensors[i] = HX710B(sensorDOUTPins[i], sensorSCKPins[i]);  // Assign pins
    }

    Serial.println("Sensors initialized. Reading pressure values...");
}

void loop() {
    for (int i = 0; i < 6; i++) {
        uint32_t rawData = 0;
        uint8_t result = pressureSensors[i].read(&rawData);  // Read sensor data

        Serial.print("Sensor ");
        Serial.print(i + 1);
        Serial.print(": ");

        if (result == 0) {  // Check if reading was successful
            Serial.println(rawData);
        } else {
            Serial.println("Error reading sensor!");
        }
    }

    Serial.println("----------------------");
    delay(1000);  // Wait 1 second before next reading
}
