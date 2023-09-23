import time
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from camera_mlx90640 import CameraMLX90640

class FrameGrabber:

    FRAME_HEIGHT = 24
    FRAME_WIDTH = 32

    def __init__(self, port):
        self.cam = CameraMLX90640(port)

    def update(self, cnt):
        print(f'cnt: {cnt}')
        cmd = {'cmd': 'frame'}
        t0 = time.time()
        rsp = self.cam.send_and_receive(cmd)
        t1 = time.time()
        print(f'dt: {t1 - t0}')
        try:
            frame = np.array(rsp['frame'])
        except KeyError:
            pass
        else:
            frame = np.array(frame)
            frame = np.reshape(frame, (self.FRAME_HEIGHT,self.FRAME_WIDTH))
            frame = np.flipud(frame)
            frame = np.fliplr(frame)
            frame = scipy.ndimage.gaussian_filter(frame, sigma=1)
            self.pcm.set_array(frame)
        return (self.pcm,)

    def run(self):
        dummy_frame = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH))
        self.fig, self.ax = plt.subplots(1,1)
        self.pcm = self.ax.pcolormesh(dummy_frame,vmin=20.0, vmax=40.0,cmap='inferno')
        self.cbar = self.fig.colorbar(self.pcm)
        self.cbar.set_label('deg (C) ')
        animation = anim.FuncAnimation(self.fig, self.update, interval=100) 
        plt.show()


if __name__ == '__main__':

   port = '/dev/ttyACM0'
   frame_grabber = FrameGrabber(port)
   frame_grabber.run()
