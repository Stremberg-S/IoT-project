import tkinter as tk


class ButtonFrame(tk.Frame):
    def __init__(
            self, master, play_callback, delete_callback,
            rename_callback, live_stream_callback, *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.play_button = tk.Button(
            self,
            text='Play',
            command=play_callback)
        self.play_button.grid(row=0, column=0, sticky='ew')

        self.delete_button = tk.Button(
            self,
            text='Delete',
            command=delete_callback
        )
        self.delete_button.grid(row=1, column=0, sticky='ew')

        self.rename_button = tk.Button(
            self,
            text='Rename',
            command=rename_callback
        )
        self.rename_button.grid(row=2, column=0, sticky='ew')

        self.live_stream_button = tk.Button(
            self,
            text='Live Stream',
            command=live_stream_callback
        )
        self.live_stream_button.grid(row=3, column=0, sticky='ew', pady=10)
        
        
    def rename_live_stream_button_text(self, new_text):
        self.live_stream_button.config(text=new_text)
