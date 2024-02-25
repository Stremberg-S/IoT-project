#include <Wire.h>
#include <Arduino.h>
#include <SoftwareSerial.h>

const int LED_PIN = 13;
const int PIR_PIN = 8;

bool motionDetected = false;

void setup()
{
  pinMode(LED_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  Serial.begin(9600);
}

void loop()
{
  // check current motion status
  bool currentMotion = digitalRead(PIR_PIN) == HIGH;

  if (currentMotion && !motionDetected)
  {                                     // if motion detected and not previously detected
    Serial.println("Motion detected!"); // print message
    motionDetected = true;              // update motion detection flag
    digitalWrite(LED_PIN, HIGH);        // turn LED on
  }
  else if (!currentMotion && motionDetected)
  {                                  // if no motion and previously detected
    Serial.println("Motion ended!"); // print message
    motionDetected = false;          // update motion detection flag
    digitalWrite(LED_PIN, LOW);      // turn LED off
  }
}
