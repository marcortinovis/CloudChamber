import os
import shutil
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class VideoFrameSorterApp:
    def __init__(self, root, video_path, trace_folder, doubt_folder, nothing_folder):
        self.root = root
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
        self.root.geometry("1900x1000")

        # Create canvas to display images
        self.canvas = tk.Canvas(root, width=1600, height=900)
        self.canvas.pack()

        # Instructions for the user
        self.instructions = tk.Label(root, text="Press T for 'Trace', D for 'Doubt', N for 'Nothing'")
        self.instructions.pack(pady=10)

        # Bind keyboard keys to corresponding functions
        self.root.bind("<KeyPress-t>", self.move_to_trace)
        self.root.bind("<KeyPress-d>", self.move_to_doubt)
        self.root.bind("<KeyPress-n>", self.move_to_nothing)

        # Display the first frame
        self.display_frame()

    def display_frame(self):

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, np.random.uniform(low=0.0, high=self.total_frames+1, size=None))
        ret, frame1 = self.cap.read()


        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            self.frame_index += 1

            # Convert frame to PIL Image for Tkinter display
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_pil = img_pil.resize((1600, 900), Image.ANTIALIAS)
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