import sys
import json
from os.path import isfile, isdir
from hashlib import pbkdf2_hmac
from binascii import hexlify
from jinja2 import Environment, BaseLoader

WPA_SUPPLICANT = '''ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=JP

network = {
    ssid="{{ wifi.ssid }}"
    psk="{{ wifi.password }}"
    key_mgmt=WPA-PSK
}\n\n'''

def wpa_psk(ssid, password):
    return hexlify(pbkdf2_hmac(
        'sha1', password.encode(), ssid.encode(), 4096, 32)).decode('utf-8')

def new_wifi():
    ssid = input('    ssid: ')
    password = input('password: ')
    passphrase = wpa_psk(ssid, password)
    return {'ssid': ssid, 'password': password, 'passphrase': passphrase}

def main():
    data = []
    if isfile('wpa.json'):
        with open('wpa.json', encoding='utf-8')as file:
            data = json.load(file)
    if len(data) != 0:
        print('0: 新規作成')
        for i, wifi in enumerate(data):
            print(f'{i+1}: {wifi["ssid"]}')
        index = 0
        while True:
            string = input(f'index[0-{len(data)}](q to exit.): ')
            if string == 'q':
                sys.exit()
            index = int(string)
            if 0 <= index and index <= len(data):
                break
        if index == 0:
            wifi = new_wifi()
        else:
            wifi = data[index-1]
    else:
        index = 0
        wifi = new_wifi()
    if index == 0:
        # 新規作成時
        data.append(wifi)
        with open('wpa.json', 'w')as file:
            json.dump(data, file, indent=4)
    drive = choice_drive()
    gen(f'{drive}:', wifi)

def choice_drive():
    while True:
        drive = input('Choice Drive[e.g. C/D/E/F...](q to exit.): ')
        if drive == 'q':
            sys.exit()
        drive = drive.upper()[:1]
        if isdir(f'{drive}:'):
            break
    return drive

def gen(dir, wifi):
    # wpa_supplicant.conf file
    env = Environment(loader=BaseLoader, trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(WPA_SUPPLICANT)
    file_name = 'wpa_supplicant.conf'
    with open(f'{dir}/{file_name}', "w", encoding='utf-8')as file:
        file.write(template.render(wifi=wifi))

    # ssh file
    with open(f'{dir}/ssh', "w")as file:
        file.write('')

if __name__ == '__main__':
    print('raspberrypi-init\nBy Alma-field')
    main()
