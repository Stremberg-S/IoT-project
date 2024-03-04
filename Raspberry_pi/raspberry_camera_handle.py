import os
from datetime import datetime as dt
from time import sleep
from serial import Serial, SerialException
from picamera import PiCamera


SERIAL_PORT: str = '/dev/ttyUSB0'
BAUD_RATE: int = 9600
USB_DRIVE_PATH: str = '/media/r4GUI/BB35-4AB9/raspberry'
MOTION_DETECTED_MSG: str = '1'
MOTION_ENDED_MSG: str = '0'


def setup_serial(port: str, baud_rate: int) -> Serial or None:
    try:
        return Serial(port, baud_rate)
    except SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None


def record_video(output_path: str, recording_duration: int) -> None:
    try:
        timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        video_file = os.path.join(output_path, f'motion_{timestamp}.h264')

        with PiCamera() as camera:
            camera.start_recording(video_file)
            camera.wait_recording(recording_duration)  # Record for specified duration
            camera.stop_recording()
    except Exception as e:
        print(f"Error recording video: {e}")


def main() -> None:
    ino_serial = setup_serial(SERIAL_PORT, BAUD_RATE)
    print('Connection with Arduino - OK')

    if ino_serial is None:
        print('no connection!!')
        return

    motion_start_time = None
    try:
        while True:
            serial_data = ino_serial.readline().strip().decode('utf-8')
            print(serial_data)

            if serial_data == MOTION_DETECTED_MSG:
                if motion_start_time is None:
                    motion_start_time = dt.now()
                    print('Motion detected! Recording video...')
            elif serial_data == MOTION_ENDED_MSG:
                if motion_start_time is not None:
                    motion_end_time = dt.now()
                    motion_duration = (
                        motion_end_time - motion_start_time
                        ).total_seconds()
                    
                    if motion_duration >= 2:
                        print('Recording video...')
                        record_video(USB_DRIVE_PATH, int(motion_duration))
                        print('Video recorded.')
                    
                    motion_start_time = None
    except KeyboardInterrupt:
        print('Program terminated by user.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        ino_serial.close()


if __name__ == '__main__':
    main()
