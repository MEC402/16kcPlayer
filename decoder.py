import cv2
import numpy as np


head_codec_tag = "16KC"
head_tag_idx = (0, 4)
head_frame_count_idx = (4, 8)
head_frame_rate_idx = (8, 10)
head_width_idx = (10, 14)
head_height_idx = (14, 18)
head_object_number_idx = (18, 22)

bytes_in_head = 18 # Without the number of objects 18, with it 22 bytes
bytes_in_frame_data = 26

frame_count = None
frame_rate = None
frame_width = None
frame_height = None





def decode_head(bytes_array):
	global frame_count
	global frame_rate
	global frame_width
	global frame_height
	
	tag = bytes_array[head_tag_idx[0]:head_tag_idx[1]].decode("utf-8")
	if tag != head_codec_tag:
		raise Exception("The input file is not a 16k codec video (16KC)")

	frame_count = int.from_bytes(bytes_array[head_frame_count_idx[0] : head_frame_count_idx[1]], byteorder='big')
	frame_rate = int.from_bytes(bytes_array[head_frame_rate_idx[0] : head_frame_rate_idx[1]], byteorder='big')
	frame_width = int.from_bytes(bytes_array[head_width_idx[0] : head_width_idx[1]], byteorder='big')
	frame_height = int.from_bytes(bytes_array[head_height_idx[0] : head_height_idx[1]], byteorder='big')
	# total_object_number = int.from_bytes(bytes[head_object_number_idx[0] : head_object_number_idx[1]], byteorder='little')

	return (frame_count, frame_rate, frame_width, frame_height)




def decode_background(bytes_array):
	global frame_width
	global frame_height

	if frame_height is None or frame_width is None:
		raise Exception("Something went wrong at decode_background() ==> heigth or width is None")

	np_arr = np.fromstring(bytes_array, np.uint8)
	background = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
	return background


def decode_texture_atlas(bytes_array):
	np_arr = np.fromstring(bytes_array, np.uint8)#.reshape(frame_height, frame_width, 3)
	texture_atlas = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
	return texture_atlas



# MAIN METHOD

def decode_file(filename):
	global frame_count
	global frame_rate
	global frame_width
	global frame_height

	file = filename

	f = open(file, 'rb')

	# Read head
	byte_arr = f.read(bytes_in_head) 
	frame_count, frame_rate, frame_width, frame_height = decode_head(byte_arr)

	# Read the background
	background_size = int.from_bytes(f.read(4), byteorder='big')
	byte_arr = f.read(background_size)
	background = decode_background(byte_arr)


	# Read frames
	for i in range(0,frame_count-1):
		canvas = np.array(background)

		# Read frame data
		frame_data_element_count = int.from_bytes(f.read(4), byteorder='big')
		frame_data = []
		for e in range(0, frame_data_element_count):
			frame_data_row = f.read(bytes_in_frame_data)
			obj_id = int.from_bytes(frame_data_row[0:2], byteorder='big')
			obj_tex_x = int.from_bytes(frame_data_row[2:6], byteorder='big')
			obj_tex_y = int.from_bytes(frame_data_row[6:10], byteorder='big')
			obj_tex_w = int.from_bytes(frame_data_row[10:14], byteorder='big')
			obj_tex_h = int.from_bytes(frame_data_row[14:18], byteorder='big')
			obj_v_x = int.from_bytes(frame_data_row[18:22], byteorder='big')
			obj_v_y = int.from_bytes(frame_data_row[22:26], byteorder='big')
			frame_data.append([obj_id, obj_tex_x, obj_tex_y, obj_tex_w, obj_tex_h, obj_v_x, obj_v_y])

		# Read the texture atlas
		texture_atlas_size = int.from_bytes(f.read(4), byteorder='big')
		byte_arr = f.read(texture_atlas_size)
		texture_atlas = decode_texture_atlas(byte_arr)

		# Add objects to the canvas
		for e in frame_data:
			v_coords = (e[5], e[6])
			w = e[3]
			h = e[4]
			tex_coords = (e[1], e[2])
			canvas[v_coords[0]:v_coords[0]+h, v_coords[1]:v_coords[1]+w] = texture_atlas[tex_coords[0]:tex_coords[0]+h, tex_coords[1]:tex_coords[1]+w]
		cv2.imshow("img", canvas)
		cv2.waitKey(30)
	cv2.destroyAllWindows()

	f.close()

