from camera_mlx90640 import CameraMLX90640

port = '/dev/ttyACM0'
num_frame = 20 
cam = CameraMLX90640(port)

frame_list = []
for i in range(num_frame):
    ok, frame = cam.grab_frame()
    print(f'frame: {i}, ok={ok}')
    if ok:
        frame_list.append(frame)
print()
print(f'{len(frame_list)} frames acquired')



