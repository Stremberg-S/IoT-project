import os
import subprocess
from datetime import datetime as dt

from serial import Serial

SERIAL_PORT: str = '/dev/ttyUSB0'
BAUD_RATE: int = 9600
USB_DRIVE_PATH: str = '/media/pi/USB_DRIVE'


def setup_serial(port: str, baud_rate: int) -> Serial:
    """Set up serial communication with Arduino."""
    return Serial(port, baud_rate)


def record_video(output_path: str) -> None:
    """Record video using Raspberry Pi camera for 10 seconds."""
    timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    video_file = os.path.join(output_path, f'motion_{timestamp}.h264')
    subprocess.run(['raspivid', '-o', video_file, '-t', '10000'])


def main() -> None:
    arduino_serial = setup_serial(SERIAL_PORT, BAUD_RATE)

    while True:
        serial_data = arduino_serial.readline().strip().decode('utf-8')

        if serial_data == 'Motion detected!':
            print("Motion detected! Recording video...")
            record_video(USB_DRIVE_PATH)
            print("Video recorded.")

        elif serial_data == 'Motion ended!':
            print("Motion ended.")


if __name__ == '__main__':
    main()
