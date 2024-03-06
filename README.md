# Motion Detection and Recording System using Arduino Uno and Raspberry Pi

This project utilizes an Arduino Uno and a Raspberry Pi 3 to detect motion using an HC-SR04 Ultrasonic Range Sensor and
record video when motion is detected. The recorded video is saved to an external USB storage device connected to the
Raspberry Pi.

## Hardware Requirements:

* Arduino Uno
* Raspberry Pi 3
* HC-SR04 Ultrasonic Range Sensor
* Raspberry Pi Camera Module V2
* External USB storage device (not necessary)

## Installation and Setup:

#### Arduino Setup:

* Connect the HC-SR04 Ultrasonic Range Sensor to the Arduino Uno.
  Upload the provided Arduino code to the Arduino Uno using the Arduino IDE.

#### Raspberry Pi Setup:

* Connect the Raspberry Pi Camera Module V2 to the Raspberry Pi.
  Ensure the Python libraries are installed by running ```pip install picamera``` .
  Copy the provided Python script to the Raspberry Pi.

#### Hardware Connection:

* Connect the Arduino Uno and Raspberry Pi 3 via USB.
  Attach the external USB storage device to the Raspberry Pi.

## Usage:

* Power on both the Arduino Uno and Raspberry Pi 3.
  The Arduino Uno will continuously monitor for motion using the HC-SR04 sensor.

* When motion is detected, the Arduino Uno will send a signal to the Raspberry Pi via serial communication.

* The Raspberry Pi script will receive the signal and start recording video using the Raspberry Pi Camera Module.

* The recorded video will be saved to the external USB storage device connected to the Raspberry Pi.

* Once motion ends, the recording will stop automatically.
