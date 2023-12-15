import click
import platform
from camera_mlx90640.live_view import LiveView

DEFAULT_PORT_LINUX = '/dev/ttyACM0'
DEFAULT_PORT_WINDOWS = 'COM1'
DEFAULT_FILE = 'mlx90640_frames.npy'

if platform.system() == 'Linux':
    DEFAULT_PORT = DEFAULT_PORT_LINUX 
else:
    DEFAULT_PORT = DEFAULT_PORT_WINDOWS

@click.command()
@click.help_option('-h', '--help')
@click.option('-p', '--port', default=DEFAULT_PORT, help='device usb/serial port')
@click.option('-f', '--file', default=DEFAULT_FILE, help='recording file') 
def cli(port, file):
    print()
    print(f'running live view')
    print(f'  usb/serial port: {port}')
    print(f'  recording file:  {file}')
    print()
    live_view = LiveView(port=port, filename=file)
    live_view.run()



