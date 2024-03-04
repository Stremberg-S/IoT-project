import os
from datetime import datetime as dt
from subprocess import Popen
from time import sleep

from serial import Serial, SerialException

from picamera import PiCamera

SERIAL_PORT: str = '/dev/ttyUSB0'
BAUD_RATE: int = 9600
USB_DRIVE_PATH: str = '/media/r4GUI/BB35-4AB9/raspberry'
MOTION_DETECTED_MSG: str = 'Motion detected'
MOTION_ENDED_MSG: str = 'No motion'


def setup_serial(port: str, baud_rate: int) -> Serial or None:
    try:
        return Serial(port, baud_rate)
    except SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None


# def record_video(output_path: str) -> None:
#     try:
#         timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
#         video_file = os.path.join(output_path, f'motion_{timestamp}.h264')
#         recording_process = Popen(['raspivid', '-o', video_file])
#         sleep(10)
#         recording_process.terminate()
#     except Exception as e:
#         print(f'Error recording video: {e}')


def record_video(output_path: str) -> None:
    """Record video using Raspberry Pi camera for 10 seconds."""
    try:
        timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        video_file = os.path.join(output_path, f'motion_{timestamp}.h264')
#
        camera = PiCamera().start_preview()
        camera.start_recording(video_file)
        sleep(10)  # Record for 10 seconds
        camera.stop_recording().stop_preview().close()
    except Exception as e:
        print(f"Error recording video: {e}")


def main() -> None:
    ino_serial = setup_serial(SERIAL_PORT, BAUD_RATE)
    print(ino_serial)
    print('Connected')

    if ino_serial is None:
        print('no connection!!')
        return

    try:
        while True:
            serial_data = ino_serial.readline().strip().decode('utf-8')
            print(serial_data)

            if serial_data == MOTION_DETECTED_MSG:
                print('Motion detected! Recording video...')
                record_video(USB_DRIVE_PATH)
                print('Video recorded.')
            elif serial_data == MOTION_ENDED_MSG:
                print('Motion ended.')
    except KeyboardInterrupt:
        print('Program terminated by user.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        ino_serial.close()


if __name__ == '__main__':
    main()
#

# import os
# 
# def get_usb_drive_name():
#     devices = os.listdir('/media/r4GUI')
#     
#     for device in devices:
#         print(device)
#         
#         
# if __name__ == '__main__':
#     get_usb_drive_name()