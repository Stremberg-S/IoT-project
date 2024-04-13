import sys

import tkinter as tk

from GUI.motion_camera import MotionCamera

sys.path.append('/home/r4GUI/Ryhma2/stremberg/IoT-project')


def main():
    root = tk.Tk()
    MotionCamera(root)
    root.mainloop()


if __name__ == "__main__":
    main()
