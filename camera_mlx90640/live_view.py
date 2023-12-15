import time
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from camera_mlx90640 import CameraMLX90640

class LiveView:

    DEFAULT_PORT = '/dev/ttyACM0'
    DEFAULT_FILENAME = 'mlx90640_frames.npy'
    DEFAULT_TEMP_RANGE = (20.0, 40.0)
    UPDATE_INTERVAL = 100

    def __init__(
            self, 
            port = DEFAULT_PORT, 
            filename = DEFAULT_FILENAME, 
            temp_range = DEFAULT_TEMP_RANGE,
            gaussian_filter = True
            ):
        self.cam = CameraMLX90640(port)
        self.filename = filename
        self.gaussian_filter = gaussian_filter 
        self.temp_range = temp_range
        self.update_interval = self.UPDATE_INTERVAL 
        self.recording = False
        self.frame_list = []
        
    def on_key_press(self,event):
        if event.key == 'r':
            if self.recording == False:
                self.frame_list = []
                self.recording = True
                print(f'recording start')
            else:
                self.recording = False
                num_frames = len(self.frame_list)
                frames = np.array(self.frame_list)
                np.save(self.filename, frames)
                print(f'recording stop, #frames={num_frames}, file={self.filename}')

    def update(self, cnt):
        cmd = {'cmd': 'frame'}
        t0 = time.time()
        ok, frame = self.cam.grab_frame()
        t1 = time.time()
        if ok:
            if self.gaussian_filter: 
                frame = scipy.ndimage.gaussian_filter(frame, sigma=1)
            self.pcm.set_array(frame)
        if self.recording:
            self.frame_list.append(frame)
            num_frames = len(self.frame_list)
            self.ax.set_title(f'frame # {cnt}, recording: {num_frames}')
        else:
            self.ax.set_title(f'frame # {cnt}')
        return (self.pcm,)

    def run(self):
        dummy_frame = np.zeros((self.cam.FRAME_HEIGHT, self.cam.FRAME_WIDTH))
        self.fig, self.ax = plt.subplots(1,1)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        temp_min, temp_max = self.temp_range
        self.pcm = self.ax.pcolormesh(dummy_frame,vmin=temp_min, vmax=temp_max, cmap='inferno')
        self.cbar = self.fig.colorbar(self.pcm)
        self.cbar.set_label('deg (C) ')
        animation = anim.FuncAnimation(
                self.fig, 
                self.update, 
                interval=self.update_interval, 
                cache_frame_data=False
                ) 
        plt.show()

# ---------------------------------------------------------------------------------------
#if __name__ == '__main__':
#   live_view = LiveView()
#   live_view.run()
