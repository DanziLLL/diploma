from dmidecode import DMIDecode
import netifaces
import subprocess
from os import listdir
from os.path import exists
import platform
import json
import requests

dmi_list = [0, 2, 4, 17]  # man dmidecode for dmi types
response_template = {
    'cpu': {},
    'ram': {},
    'video': {},
    'storage': {},
    'platform': {},
    'network': {},
    'misc': {}
}


class Linux:
    @staticmethod
    def get_data():
        rsp = response_template
        dmi = DMIDecode()
        for i in dmi.data.values():
            if i['DMIType'] in dmi_list:
                Linux.__dmi2inv(i, rsp)
        Linux.__get_network(rsp)
        Linux.__get_drives_info(rsp)
        Linux.__get_gpu(rsp)
        Linux.__get_misc(rsp)
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        answer = requests.post('http://inventoryapp.example.com:9000/api/computer', data=json.dumps({'data': rsp}), headers=headers)
        return answer

    @staticmethod
    def __get_misc(rsp):
        rsp['misc']['os'] = {}
        rsp['misc']['os']['distro'] = platform.linux_distribution()[0]
        rsp['misc']['os']['version'] = platform.linux_distribution()[1]
        rsp['misc']['hostname'] = platform.node()


    @staticmethod
    def __get_drives_info(rsp):
        drives = [f for f in listdir('/sys/block/')]
        for i in drives:
            if exists('/sys/block/{}/device/model'.format(i)):
                with open('/sys/block/{}/device/model'.format(i)) as f:
                    rsp['storage'][i] = {}
                    rsp['storage'][i]['model'] = f.readline().rstrip()
                    f.close()
                with open('/sys/class/block/{}/size'.format(i)) as f:
                    size = (int(f.readline()) * 512) // pow(2, 30)
                    rsp['storage'][i]['size'] = size
                    f.close()
        return

    @staticmethod
    def __get_gpu(rsp):
        lspci = subprocess.check_output(["lspci"]).decode("utf-8").replace('\\n', '\n')
        for line in lspci.splitlines():
            if 'VGA' in line:
                rsp['video']['model'] = line.split(': ')[1]

    @staticmethod
    def __get_network(rsp):
        ifaces = netifaces.interfaces()
        for interface in ifaces:
            if interface == 'lo':  # we don't need loop interface
                continue
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
                # only interfaces with ip addresses are interesting for us
                rsp['network'][interface] = {}
                rsp['network'][interface]['ip'] = addrs[netifaces.AF_INET][0]['addr']
                rsp['network'][interface]['mac'] = addrs[netifaces.AF_LINK][0]['addr']

    @staticmethod
    def __dmi2inv(entry, rsp):
        if entry['DMIType'] == 0:  # BIOS
            rsp['platform']['bios_version'] = entry['Version']
            return
        elif entry['DMIType'] == 2:  # Baseboard
            rsp['platform']['manufacturer'] = entry['Manufacturer']
            rsp['platform']['model'] = entry['Product Name']
            rsp['platform']['version'] = entry['Version']
            return
        elif entry['DMIType'] == 4:  # CPU
            rsp['cpu']['model'] = entry['Version'].split(' @ ')[0]
            rsp['cpu']['frequency'] = int(entry['Current Speed'].split()[0])
            rsp['cpu']['physical_cores'] = int(entry['Core Count'])
            rsp['cpu']['logical_cores'] = int(entry['Thread Count'])
            return
        elif entry['DMIType'] == 17:  # RAM
            rsp['ram'][entry['Locator']] = {}
            rsp['ram'][entry['Locator']]['size'] = int(entry['Size'].split(' ')[0])
            rsp['ram'][entry['Locator']]['manufacturer'] = entry['Manufacturer'].rstrip()
            rsp['ram'][entry['Locator']]['model'] = entry['Part Number'].rstrip()
            return
