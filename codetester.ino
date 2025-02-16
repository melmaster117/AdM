const int solenoidPins[7] = {2, 3, 4, 5, 6, 7, 8};  
const int pumpPin = 9; 

void setup() {
    Serial.begin(115200);

    for (int i = 0; i < 7; i++) {
        pinMode(solenoidPins[i], OUTPUT);
        digitalWrite(solenoidPins[i], LOW); // Ensure solenoids are off initially
    }
    pinMode(pumpPin, OUTPUT);
    digitalWrite(pumpPin, LOW); // Ensure pump is off initially

    Serial.println("Starting inflation...");
    inflateAllSegments();
    
    Serial.println("Starting deflation...");
    deflateSegmentsOneByOne();

    Serial.println("Releasing all air...");
    releaseAllAir();
    
    Serial.println("Process complete.");
}

void loop() {
}

void inflateAllSegments() {
    for (int i = 0; i < 6; i++) {
        digitalWrite(solenoidPins[i], HIGH); // Open segment solenoids
    }
    digitalWrite(pumpPin, HIGH); // Turn on air pump
    delay(120000); // Wait for 120 seconds

    digitalWrite(pumpPin, LOW); // Turn off pump
    for (int i = 0; i < 6; i++) {
        digitalWrite(solenoidPins[i], LOW); // Close all segment solenoids
    }

    Serial.println("Inflation complete.");
}
void deflateSegmentsOneByOne() {
    for (int i = 0; i < 6; i++) {
        digitalWrite(solenoidPins[i], HIGH); // Open the segment solenoid
        digitalWrite(solenoidPins[6], HIGH); // Open outlet solenoid
        delay(5000); // Let air out for 5 seconds
        digitalWrite(solenoidPins[i], LOW); // Close segment solenoid
        digitalWrite(solenoidPins[6], LOW); // Close outlet solenoid
        Serial.print("Segment ");
        Serial.print(i + 1);
        Serial.println(" deflated.");
    }
}

void releaseAllAir() {
    digitalWrite(solenoidPins[6], HIGH); // Open outlet solenoid
    delay(10000); // Let all air escape for 10 seconds
    digitalWrite(solenoidPins[6], LOW); // Close outlet solenoid
    Serial.println("All air released.");
}
