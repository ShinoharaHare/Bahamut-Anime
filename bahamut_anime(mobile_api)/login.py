import base64
import random
import re

import requests

class API:
    login = 'https://api.gamer.com.tw/mobile_app/user/v1/login.php'
    do_login = 'https://api.gamer.com.tw/mobile_app/user/v2/do_login.php'

def randInt(i, i2):
    return random.randint(0, (i2 - i) + 1) + i

def decodeCoordinate(string):
    string = string.encode('UTF-8')
    xy = [-1, -1]
    string1 = string[12:16]
    string1 += string[7:12]
    string1 += string[0:7]
    string2 = base64.decodebytes(string1).decode('UTF-8')
    if not re.match(r'^[0-9]{12}$', string2):
        return xy
    xy[0] = int(string2[4:6])
    xy[1] = int(string2[8:10])
    return xy


def encodeCoordinate(i, i2):
    format1 = f'{i:02d}'
    format2 = f'{i2:02d}'
    format3 = f'{int(random.random() * 9999.0 + 1.0):04d}'
    format4 = f'{int(random.random() * 99.0 + 1.0):02d}'
    format5 = f'{int(random.random() * 99.0 + 1.0):02d}'
    string = format1 + format3 + format4 + format5 + format2
    format1 = base64.encodebytes(string.encode('UTF-8'))
    string2 = format1[9:16]
    string2 += format1[4:9]
    string2 += format1[0:4]
    return string2

def login(uid, passwd, session):
    token = '1'
    response = session.post(API.login, data={'token': token})
    code = response.json()['code']
    xy = decodeCoordinate(code)
    code = encodeCoordinate(*xy)
    data = {
            'token': token,
            'uid': uid,
            'code': code,
            'passwd': passwd
    }
    response = session.post(API.do_login, data=data)

if __name__ == "__main__":
    session = requests.session()
    uid = 'SinoharaHare'
    passwd = 'anna1822'
    

    login(uid, passwd, session)
    
    print(session.cookies['BAHAENUR'], session.cookies['BAHARUNE'])