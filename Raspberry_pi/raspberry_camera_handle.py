import os
import sys

sys.path.append('/home/r4GUI/Ryhma2/stremberg/IoT-project')

from datetime import datetime as dt

from picamera import PiCamera
from serial import Serial, SerialException

from config import (BAUD_RATE, MIN_RECORDING_DURATION, MOTION_DETECTED_MSG,
                    MOTION_ENDED_MSG, SERIAL_PORT, USB_DRIVE_PATH)

motion_start_time = None


def setup_serial(port: str, baud_rate: int) -> Serial or None:
    try:
        return Serial(port, baud_rate)
    except SerialException as e:
        print(f'Error opening serial port {port}: {e}')
        return None


def record_video(output_path: str, rec_duration: int) -> None:
    try:
        timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        video_file = os.path.join(output_path, f'{timestamp}.h264')

        with PiCamera() as cam:
            cam.start_recording(video_file)
            cam.wait_recording(rec_duration)
            cam.stop_recording()
    except Exception as e:
        print(f'Error recording video: {e}')


def handle_motion_detection(serial_data: str) -> None:
    global motion_start_time

    if serial_data == MOTION_DETECTED_MSG:
        if motion_start_time is None:
            motion_start_time = dt.now()

    elif serial_data == MOTION_ENDED_MSG:
        if motion_start_time is not None:
            motion_end_time = dt.now()
            motion_duration = (
                    motion_end_time - motion_start_time
            ).total_seconds()

            if motion_duration >= MIN_RECORDING_DURATION:
                print('Recording video...')
                record_video(USB_DRIVE_PATH, int(motion_duration))
                print('Video recorded.')

            motion_start_time = None


def main() -> None:
    ino_serial = setup_serial(SERIAL_PORT, BAUD_RATE)
    print('Connection with Arduino - OK')

    if ino_serial is None:
        print('No connection!!')
        return

    try:
        while True:
            serial_data = ino_serial.readline().strip().decode('utf-8')
            print(serial_data)

            handle_motion_detection(serial_data)
    except KeyboardInterrupt:
        print('Program terminated by user.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        ino_serial.close()


if __name__ == '__main__':
    main()
