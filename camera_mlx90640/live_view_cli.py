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
@click.option(
        '-p', '--port', 
        default=DEFAULT_PORT, 
        help='device usb/serial port'
        )
@click.option(
        '-f', '--file', 
        default = DEFAULT_FILE, 
        help = 'recording file name') 
@click.option(
        '-c', '--count', 
        is_flag = True, 
        show_default = True, 
        default = False, 
        help = 'add count to filename'
        ) 
@click.option(
        '-a', '--auto', 
        show_default = False, 
        default = 0, 
        help = 'auto record this many frames'
        ) 
def cli(port, file, count, auto):
    print()
    print(f'running live view')
    print(f'  usb/serial port:  {port}')
    print(f'  recording file:   {file}')
    print(f'  recording count:  {count}')
    print(f'  auto record:      {auto}')
    print()
    live_view = LiveView(port=port, filename=file, add_count=count, auto_record=auto)
    live_view.run()



