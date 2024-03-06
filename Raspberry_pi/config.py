import os

from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

SERIAL_PORT: str = os.getenv('SERIAL_PORT')
BAUD_RATE: int = int(os.getenv('BAUD_RATE'))
USB_DRIVE_PATH: str = os.getenv('USB_DRIVE_PATH')

MOTION_DETECTED_MSG: str = '1'
MOTION_ENDED_MSG: str = '0'
MIN_RECORDING_DURATION: int = 2  # seconds
