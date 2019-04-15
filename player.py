import tkinter as tk
import tkinter.filedialog
import cv2

video_path = "video.mp4"

canvas_width = 800
canvas_height =700

master = tk.Tk()

def browse():
	global video_path 
	video_path = tk.filedialog.askopenfile().name


def play():
	print(video_path)
	cap = cv2.VideoCapture(video_path)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_heigth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	for _ in range(0, frame_count):
		_, frame = cap.read()
		frame = cv2.resize(frame, (int(canvas_width),int(canvas_height)))
		cv2.imshow(video_path, frame)
		cv2.waitKey(30)
	cv2.destroyAllWindows()

browse_button = tk.Button(master, text="Browse", command=browse)
browse_button.grid(row=0, column=0)

play_button = tk.Button(master, text="Play", command=play)
play_button.grid(row=1,column=0)

obj_label = tk.Label(master, text="Objects:")
obj_label.grid(row=0, column=1)

obj_0 = tk.IntVar()
obj_cb_0 = tk.Checkbutton(master, text="0", variable=obj_0)
obj_cb_0.grid(row=1, column=1)

obj_1 = tk.IntVar()
obj_cb_1 = tk.Checkbutton(master, text="1", variable=obj_1)
obj_cb_1.grid(row=2, column=1)


obj_2 = tk.IntVar()
obj_cb_2 = tk.Checkbutton(master, text="2", variable=obj_2)
obj_cb_2.grid(row=3, column=1)



tk.mainloop()
