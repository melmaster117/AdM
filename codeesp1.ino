#include <Wire.h>
#include "HX710B.h"


const int solenoidPins[] = {5, 18, 19, 21, 22, 23, 4}; 
const int pumpRelayPin = 25;

HX710B pressureSensors[] = {
    HX710B(32, 33),
    HX710B(26, 27),
    HX710B(14, 12),
    HX710B(13, 15),
    HX710B(2, 0),
    HX710B(16, 17)
};

const float inflatePressure = 8.0;
float segmentThresholds[6] = {8.0, 8.0, 8.0, 8.0, 8.0, 8.0};

void setup() {
    Serial.begin(115200);
    
    for (int i = 0; i < 7; i++) {
        pinMode(solenoidPins[i], OUTPUT);
        digitalWrite(solenoidPins[i], LOW); // All solenoids OFF initially
    }

    // Setup pump relay
    pinMode(pumpRelayPin, OUTPUT);
    digitalWrite(pumpRelayPin, LOW); // Pump OFF initially

    // Initialize pressure sensors
    for (int i = 0; i < 6; i++) {
        pressureSensors[i].begin();
    }

    Serial.println("System Initialized.");
    inflateAllSegments();
}

void loop() {
    adjustSegmentPressure(2, 5.0); 

    delay(10000);
}

void inflateAllSegments() {
    Serial.println("Inflating All Segments...");
    
    for (int i = 0; i < 6; i++) {
        digitalWrite(solenoidPins[i], HIGH);
    }
    digitalWrite(pumpRelayPin, HIGH);
    digitalWrite(solenoidPins[6], LOW); // Ensure outlet solenoid is closed

    bool inflated = false;
    while (!inflated) {
        inflated = true;
        for (int i = 0; i < 6; i++) {
            float pressure = getPressure(i);
            Serial.print("Segment "); Serial.print(i + 1);
            Serial.print(" Pressure: "); Serial.println(pressure);

            if (pressure < inflatePressure) {
                inflated = false; // Keep inflating if any segment is below threshold
            }
        }
        delay(500);
    }

    for (int i = 0; i < 6; i++) {
        digitalWrite(solenoidPins[i], LOW);
    }
    digitalWrite(pumpRelayPin, LOW);

    Serial.println("Inflation Complete.");
}

void adjustSegmentPressure(int segment, float newThreshold) {
    if (segment < 1 || segment > 6) return;

    Serial.print("Adjusting Segment "); Serial.print(segment);
    Serial.print(" to "); Serial.print(newThreshold); Serial.println(" PSI");

    segment--; // Convert to zero-based index
    segmentThresholds[segment] = newThreshold;

    while (getPressure(segment) > newThreshold) {
        digitalWrite(solenoidPins[segment], HIGH); // Open segment valve
        digitalWrite(solenoidPins[6], HIGH);       // Open outlet valve
        digitalWrite(pumpRelayPin, LOW);           // Ensure pump is off

        Serial.print("Releasing air from Segment "); Serial.println(segment + 1);
        delay(500);
    }

    digitalWrite(solenoidPins[segment], LOW);
    digitalWrite(solenoidPins[6], LOW);
    
    Serial.println("Pressure Adjusted.");
}

float getPressure(int index) {
    long raw = pressureSensors[index].read();
    return (raw / 1000.0); 

void presetCompensation(int inflateList[], int deflateList[], int inflateSize, int deflateSize) {
    Serial.println("Starting Preset Compensation...");

    for (int i = 0; i < inflateSize; i++) {
        int seg = inflateList[i] - 1;
        Serial.print("Inflating Segment "); Serial.println(seg + 1);
        
        digitalWrite(solenoidPins[seg], HIGH);
        digitalWrite(pumpRelayPin, HIGH);
        digitalWrite(solenoidPins[6], LOW); 

        while (getPressure(seg) < inflatePressure) {
            delay(500);
        }

        digitalWrite(solenoidPins[seg], LOW);
    }
    digitalWrite(pumpRelayPin, LOW);

    // Deflate Segments
    for (int i = 0; i < deflateSize; i++) {
        int seg = deflateList[i] - 1;
        Serial.print("Deflating Segment "); Serial.println(seg + 1);

        digitalWrite(solenoidPins[seg], HIGH);
        digitalWrite(solenoidPins[6], HIGH);
        digitalWrite(pumpRelayPin, LOW);

        while (getPressure(seg) > segmentThresholds[seg]) {
            delay(500);
        }

        digitalWrite(solenoidPins[seg], LOW);
        digitalWrite(solenoidPins[6], LOW);
    }

    Serial.println("Preset Compensation Complete.");
}
