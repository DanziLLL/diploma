import platform
from linux_exporter import Linux
import getpass


if __name__ == '__main__':
    os = platform.system()
    if os == 'Linux':
        if getpass.getuser() != 'root':
            print('Script must be run as root!')
            exit(-1)
        else:
            Linux.get_data()

