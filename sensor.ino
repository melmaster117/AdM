const int FSR_PIN = A0;
int forceValue = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  forceValue = analogRead(FSR_PIN);  // Corrected function name
  Serial.print("Force Sensor Value: ");
  Serial.println(forceValue);

  delay(500);
}
