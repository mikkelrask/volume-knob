#include <hid-project.h>

void setup() {
  Serial.begin(115200);
  delay(200); // Allow time for keyboard to initialize
}

void loop() {
  // Read potentiometer value and map it to volume levels (0-100%)
  int sensorValue = analogRead(A0);
  int volume = map(sensorValue, 0, 1023, 0, 100);
  Serial.println(sensorValue);
  // Adjust volume only if there's a significant change
  static int lastVolume = -1;
  if (volume != lastVolume) {
    Serial.println(volume);
    lastVolume = volume; 
  }
  delay(20); // Adjust delay for smooth operation
}
