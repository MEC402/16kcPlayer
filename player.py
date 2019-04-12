from tkinter import *
import cv2
from PIL import Image, ImageTk

video_path = "video.mp4"

canvas_width = 800
canvas_height =700

master = Tk()

canvas = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
canvas.pack()

#img = PhotoImage(file='testImage.png')
array = cv2.imread("testImage.png")
frame = ImageTk.PhotoImage(image=Image.fromarray(array))
canvas_img = canvas.create_image(20,20, anchor=NW, image=frame)

cap = cv2.VideoCapture(video_path)
def play():
	_, frame = cap.read()
	frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
	canvas.itemconfig(canvas_img, image = frame)
	"""
	cap = cv2.VideoCapture(video_path)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_heigth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	for _ in range(0, frame_count):
		_, frame = cap.read()
		img = ImageTk.PhotoImage(image=Image.fromarray(frame))
		canvas.itemconfig(canvas_img, image = img)
	"""


play_button = Button(master, text="Play", command=play)
play_button.pack()

mainloop()
