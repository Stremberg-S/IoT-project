import os
import tkinter as tk
import tkinter.messagebox as messagebox
from subprocess import Popen
from threading import Thread
from time import sleep

from config import RECORDED_VIDEOS_PATH, VLC_PATH


# from picamera import PiCamera


class MotionCamera:
    def __init__(self, master):
        self.vlc_process = None
        self.selected_video = None
        self.recorded_videos = None
        self.video_listbox = None
        self.video_frame = None
        self.master = master
        self.master.title('Raspberry-Motion-Cam')
        self.master.bind('<BackSpace>', self.handle_delete_key)
        self.live_stream_active = False
        self.recorded_videos_path = RECORDED_VIDEOS_PATH
        # self.camera = PiCamera()
        self.create_widgets()
        self.start_updater()

    def create_widgets(self) -> None:
        self.video_frame = tk.LabelFrame(self.master, text='Recorded Videos')
        self.video_frame.grid(row=0, column=1, padx=20, pady=10)

        self.video_listbox = tk.Listbox(self.video_frame, width=60, height=20)
        self.video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.video_listbox.bind('<<ListboxSelect>>', self.on_video_select)
        self.video_listbox.bind('<Double-Button-1>', lambda event: self.play_video())
        self.update_video_list()

        # Create a frame to contain the buttons
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Place the buttons inside the button frame
        play_button = tk.Button(
            button_frame,
            text='Play',
            command=self.play_video
        )
        play_button.grid(row=0, column=0, sticky='ew')

        delete_button = tk.Button(
            button_frame,
            text='Delete',
            command=self.delete_video
        )
        delete_button.grid(row=1, column=0, sticky='we')

        rename_button = tk.Button(
            button_frame,
            text='Rename',
            command=self.rename_video
        )
        rename_button.grid(row=2, column=0, sticky='ew')

        live_stream_button = tk.Button(
            button_frame,
            text='Live Stream',
            command=self.start_live_stream
        )
        live_stream_button.grid(row=3, column=0, sticky='ew', pady=10)

    def update_video_list(self) -> None:
        self.video_listbox.delete(0, tk.END)
        self.recorded_videos = sorted(os.listdir(self.recorded_videos_path))
        self.video_listbox.insert(tk.END, *self.recorded_videos)

    def on_video_select(self, event) -> None:
        self.selected_video = self.video_listbox.get(
            self.video_listbox.curselection()
        )

    def handle_delete_key(self, event):
        if self.selected_video:
            self.delete_video()
        else:
            pass

    def play_video(self) -> None:
        if self.selected_video:
            video_path = os.path.join(
                self.recorded_videos_path,
                self.selected_video
            )
            try:
                self.vlc_process = Popen([VLC_PATH, video_path])
                Thread(target=self.wait_for_vlc_exit).start()
            except Exception as e:
                print(f'Error playing video: {e}')
        else:
            print('Please select a video to play.')

    def wait_for_vlc_exit(self) -> None:
        self.vlc_process.wait()
        del self.vlc_process

    def delete_video(self) -> None:
        if self.selected_video:
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete '{self.selected_video}'?"
            )
            if confirm:
                video_path = os.path.join(
                    self.recorded_videos_path,
                    self.selected_video
                )
                os.remove(video_path)
                self.update_video_list()
        else:
            print('Please select a video to delete.')

    def rename_video(self) -> None:
        selected_index = self.video_listbox.curselection()
        if selected_index:
            selected_video = self.video_listbox.get(selected_index[0])
            old_path = os.path.join(self.recorded_videos_path, selected_video)

            entry = tk.Entry(self.video_listbox, width=60)
            entry.grid(row=selected_index[0], column=0, sticky='w')
            entry.insert(0, selected_video)
            entry.focus_set()

            def handle_rename(event) -> None:
                new_name = entry.get()
                new_path = os.path.join(self.recorded_videos_path, new_name)
                os.rename(old_path, new_path)
                self.update_video_list()
                entry.destroy()

            entry.bind('<Return>', handle_rename)
        else:
            print('Please select a video to rename.')

    def start_live_stream(self) -> None:
        if not self.live_stream_active:
            self.live_stream_active = True
            live_stream_window = tk.Toplevel(self.master)
            live_stream_window.title('Live Stream')
            live_stream_window.geometry('800x600')

            stream_label = tk.Label(live_stream_window)
            stream_label.pack()

            self.camera.start_preview(
                fullscreen=False,
                window=(live_stream_window.winfo_id())
            )
        else:
            print('Live stream is already active.')

    def start_updater(self) -> None:
        updater_thread = Thread(target=self.check_for_changes)
        updater_thread.daemon = True
        updater_thread.start()

    def check_for_changes(self) -> None:
        while True:
            current_files = set(os.listdir(self.recorded_videos_path))
            if current_files != set(self.recorded_videos):
                self.update_video_list()
            sleep(1)
