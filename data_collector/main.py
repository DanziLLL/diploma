import platform
from linux import Linux
from windows import Windows
import getpass


if __name__ == '__main__':
    os = platform.system()
    if os == 'Linux':
        if getpass.getuser() != 'root':
            print('Script must be run as root!')
            exit(-1)
        Linux.get_data()
    elif os == 'Windows':
        Windows.get_data()
