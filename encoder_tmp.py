import cv2
import numpy as np

texture_atlas_w = 1000
texture_atlas_h = 1000

file = open("video.16kc", 'wb')
file.write(bytes("16KC", 'utf-8'))


background = cv2.imread("testImage.png", cv2.IMREAD_COLOR)

cap = cv2.VideoCapture("Test_Bird_1object.mp4")
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_heigth = background.shape[0]
frame_width = background.shape[1]
frame_fps = int(cap.get(cv2.CAP_PROP_FPS))


file.write(frame_count.to_bytes(4, byteorder='big'))
file.write(frame_fps.to_bytes(2, byteorder='big'))
file.write(frame_width.to_bytes(4, byteorder='big'))
file.write(frame_heigth.to_bytes(4, byteorder='big'))

_, background = cv2.imencode('.png', background)
background = background.tobytes()

file.write(len(background).to_bytes(4, byteorder='big'))
file.write(background)


_, f = cap.read()
i = 0
while f is not None:
	texture_atlas = np.zeros((texture_atlas_w,texture_atlas_h,3), dtype=np.uint8)
	frame_obj_count = 1
	file.write(frame_obj_count.to_bytes(4, byteorder='big'))

	texture_atlas[0:f.shape[0], 0:f.shape[1]] = f

	obj_id = 0
	obj_tex_x = 0
	obj_tex_y = 0
	obj_tex_w = f.shape[1]
	obj_tex_h = f.shape[0]
	obj_v_x = 20
	obj_v_y = i
	i=i+1

	file.write(obj_id.to_bytes(2, byteorder='big'))
	file.write(obj_tex_x.to_bytes(4, byteorder='big'))
	file.write(obj_tex_y.to_bytes(4, byteorder='big'))
	file.write(obj_tex_w.to_bytes(4, byteorder='big'))
	file.write(obj_tex_h.to_bytes(4, byteorder='big'))
	file.write(obj_v_x.to_bytes(4, byteorder='big'))
	file.write(obj_v_y.to_bytes(4, byteorder='big'))

	_, texture_atlas = cv2.imencode('.png', texture_atlas)
	texture_atlas = texture_atlas.tobytes()

	file.write(len(texture_atlas).to_bytes(4, byteorder='big'))
	file.write(texture_atlas)


	_, f = cap.read()

file.close()

