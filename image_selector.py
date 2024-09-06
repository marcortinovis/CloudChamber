'''
A python script that takes a video and interactively separates the frames in the three categories.

Before starting the program you should substitute VIDEO_PATH with the path of your video,
then execute the program and it will prompt you a window showing the frames. You can tell the program
what you're seeing with the keyboard (the keys to use are printed on screen). The saved images are stored
in three folders that (if they don't yet exists) are created when starting the program. You should
export the images before running the program another time, or else there is the risk to lose them.

This is not necessarily the most updated version of the program. See https://github.com/marcortinovis/CloudChamber/blob/main/image_selector.py
'''

import os
import shutil
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class VideoFrameSorterApp:
    def __init__(self, root, video_path, trace_folder, doubt_folder, nothing_folder):
        self.root = root
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.scale_canvas = 0.9
        self.scale_image = 0.89
        self.root.state('zoomed')
        self.video_path = video_path
        self.trace_folder = trace_folder
        self.doubt_folder = doubt_folder
        self.nothing_folder = nothing_folder
        self.current_frame = None
        self.frame_index = 0

        # Open the video using OpenCV
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: Cannot open video file.")
            exit()

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Configure the main window
        self.root.title("Video Frame Sorter")
        self.root.geometry(f"{int(round(self.scale_canvas*self.screen_width))}x{int(round(self.scale_canvas*self.screen_height))}+{0}+{0}")

        # Create canvas to display images
        self.canvas = tk.Canvas(root, width=self.scale_canvas*self.screen_width, height=self.scale_canvas*self.screen_height)
        self.canvas.pack()

        # Instructions for the user
        self.instructions = tk.Label(root, text="Press T for 'Trace', D for 'Doubt', N for 'Nothing'")
        self.instructions.pack(pady=0)

        # Bind keyboard keys to corresponding functions
        self.root.bind("<KeyPress-t>", self.move_to_trace)
        self.root.bind("<KeyPress-d>", self.move_to_doubt)
        self.root.bind("<KeyPress-n>", self.move_to_nothing)

        # Display the first frame
        self.display_frame()

    def display_frame(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, np.random.uniform(low=0.0, high=self.total_frames+1, size=None))
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            self.frame_index += 1

            # Convert frame to PIL Image for Tkinter display
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_pil = img_pil.resize((int(round(self.scale_image*self.screen_width)), int(round(self.scale_image*self.screen_height))), Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img_pil)

            # Clear the canvas and display the frame
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        else:
            # If no more frames are left, show a message
            self.instructions.config(text="All frames have been sorted!")
            self.canvas.delete("all")
            self.cap.release()

    def save_frame(self, target_folder):
        # Save the current frame to the corresponding folder
        if self.current_frame is not None:
            frame_filename = f"frame_{self.frame_index}.png"
            frame_path = os.path.join(target_folder, frame_filename)
            cv2.imwrite(frame_path, self.current_frame)
            print(f"Saved frame {self.frame_index} to {target_folder}")

    def move_to_trace(self, event=None):
        self.save_frame(self.trace_folder)
        self.display_frame()

    def move_to_doubt(self, event=None):
        self.save_frame(self.doubt_folder)
        self.display_frame()

    def move_to_nothing(self, event=None):
        self.save_frame(self.nothing_folder)
        self.display_frame()

# Set your directories here
video_path = 'VIDEO_PATH'         # Path to your video file
trace_folder = 'trace_frames'     # Folder where "Trace" frames will go
doubt_folder = 'doubt_frames'     # Folder where "Doubt" frames will go
nothing_folder = 'nothing_frames' # Folder where "Nothing" frames will go

# Create destination folders if they don't exist
os.makedirs(trace_folder, exist_ok=True)
os.makedirs(doubt_folder, exist_ok=True)
os.makedirs(nothing_folder, exist_ok=True)

# Run the app
root = tk.Tk()
app = VideoFrameSorterApp(root, video_path, trace_folder, doubt_folder, nothing_folder)
root.mainloop()