import tkinter as tk

from GUI.motion_camera import MotionCamera


def main():
    root = tk.Tk()
    MotionCamera(root)
    root.mainloop()


if __name__ == "__main__":
    main()
