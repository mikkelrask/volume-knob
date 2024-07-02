#include <HID-Project.h>
#include <HID-Settings.h>

#define REVERSED true

int currentVolume = 0;
int previousVolume = 0;
int volumeAdjustment = 0;

void setup()
{
  Serial.begin(115200);
  Consumer.begin();
  delay(1000);
  for (int i = 0; i < 52; i++)
  {
    Consumer.write(MEDIA_VOLUME_DOWN);
    delay(2);
  }
}

void loop()
{
  currentVolume = analogRead(A0);
  currentVolume = map(currentVolume, 0, 1023, 0, 101);
  if (REVERSED)
  {
    currentVolume = 101 - currentVolume;
  }
  if (abs(currentVolume - previousVolume) > 1)
  {
    int volumeDifference = (currentVolume / 2) - (previousVolume / 2);
    previousVolume = currentVolume;

    if (volumeDifference > 0)
    {
      for (int i = 0; i < volumeDifference; i++)
      {
        Consumer.write(MEDIA_VOLUME_UP);
        Serial.println(volumeAdjustment + i + 1);
        delay(2);
      }
    }
    else if (volumeDifference < 0)
    {
      for (int i = 0; i < abs(volumeDifference); i++)
      {
        Consumer.write(MEDIA_VOLUME_DOWN);
        Serial.println(volumeAdjustment - i - 1);
        delay(2);
      }
    }
    volumeAdjustment += volumeDifference;
  }
  delay(35);
}
