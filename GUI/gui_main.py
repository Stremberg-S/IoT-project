import tkinter as tk

from GUI.motion_camera_gui import MotionCamera


def main():
    root = tk.Tk()
    motion_gui = MotionCamera(root)
    # root.after(1000, motion_gui.update_video_list)
    root.mainloop()


if __name__ == "__main__":
    main()
