import time
import pathlib
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
            gaussian_filter = True,
            add_count = False,
            auto_record = None
            ):
        self.cam = CameraMLX90640(port)
        self.filename = pathlib.Path(filename)
        self.gaussian_filter = gaussian_filter 
        self.temp_range = temp_range
        self.update_interval = self.UPDATE_INTERVAL 
        self.add_count = add_count
        self.auto_record = auto_record 
        self.recording = False
        self.recording_count = 0
        self.frame_count = 0
        self.frame_list = []


    def start_recording(self): 
        self.frame_list = []
        self.recording = True
        self.recording_count += 1
        print(f'recording {self.recording_count} start')


    def stop_recording(self): 
        self.recording = False
        num_frames = len(self.frame_list)
        frames = np.array(self.frame_list)
        if self.add_count:
            filename = f'{self.filename.stem}_{self.recording_count:03d}{self.filename.suffix}'
            filepath = self.filename.parent / filename
        else:
            filepath = self.filename
        np.save(filepath, frames)
        print(f'recording {self.recording_count} stop,', end=' ')
        print(f'#frames={num_frames}, file={filepath}')

    def on_key_press(self,event):
        if event.key == 'r':
            if self.recording == False:
                self.start_recording()
            else:
                self.stop_recording()

    def update(self, cnt):
        cmd = {'cmd': 'frame'}
        t0 = time.time()
        ok, frame = self.cam.grab_frame()
        t1 = time.time()
        if ok:
            self.frame_count += 1
            if self.gaussian_filter: 
                frame = scipy.ndimage.gaussian_filter(frame, sigma=1)
            self.pcm.set_array(frame)
            if self.recording:
                self.frame_list.append(frame)
                num_frames = len(self.frame_list)
                self.ax.set_title(f'frame # {self.frame_count}, recording: {num_frames}')
                if self.auto_record > 0:
                    if self.auto_record <= num_frames:
                        self.stop_recording()
                        self.auto_record = 0
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
        print('press r to toggle recording on/off')
        print()
        if self.auto_record > 0:
            self.start_recording()
        plt.show()

