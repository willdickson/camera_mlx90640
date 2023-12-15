import json
import serial
import numpy as np

class CameraMLX90640(serial.Serial):
    """
    Implements communications camera_mlx90640_firmware
    """

    FRAME_HEIGHT = 24
    FRAME_WIDTH = 32

    def __init__(self, port):
        self.port_param = {'port': port, 'baudrate': 115200, 'timeout': 2.0}
        super().__init__(**self.port_param)
        self.num_throw_away = 10
        self.throw_away_lines()

    def throw_away_lines(self):
        """ 
        Throw away first few lines. Deals with case where user has updated the
        firmware which writes a bunch text to the serial port. 
        """
        self.timeout = 0.1
        for i in range(self.num_throw_away):
            line = self.readline()
        self.timeout = self.port_param['timeout']

    def send_and_receive(self, msg_dict):
        """
        Send and receive message from the device.
        """
        msg_json = f'{json.dumps(msg_dict)}\n'
        self.write(msg_json.encode())
        rsp_json = self.read_until()
        rsp_json = rsp_json.strip()
        rsp_dict = {}
        try:
            rsp_dict = json.loads(rsp_json.decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print(f'Error decoding json message: {e}')
        return rsp_dict

    def grab_frame(self):
        """
        Grab from from camera and convert it to a numpy array
        """
        cmd = {'cmd': 'frame'}
        rsp = self.send_and_receive(cmd)
        try:
            frame = np.array(rsp['frame'])
        except KeyError:
            frame = np.zeros((self.FRAME_HEIGHT,self.FRAME_WIDTH))
            ok = False
        else:
            frame = np.array(frame)
            frame = np.reshape(frame, (self.FRAME_HEIGHT,self.FRAME_WIDTH))
            frame = np.flipud(frame)
            frame = np.fliplr(frame)
            ok = True
        return ok, frame

