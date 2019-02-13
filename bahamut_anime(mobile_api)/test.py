import io
import json
import time

import requests

start = time.time()

session = requests.Session()

class API:
    login = 'https://api.gamer.com.tw/mobile_app/user/v1/login.php'
    do_login = 'https://api.gamer.com.tw/mobile_app/user/v2/do_login.php'

    video = 'https://api.gamer.com.tw/mobile_app/anime/v1/video.php' #?anime_sn=0&sn=11485
    token = 'https://api.gamer.com.tw/mobile_app/anime/v3/token.php' #?device=0246109813da3cd2dc9d76b9837dfb385b1f3f841837f8eb5c625cd91964&sn=11485
    m3u8 = 'https://api.gamer.com.tw/mobile_app/anime/v2/m3u8.php'   #?device=0246109813da3cd2dc9d76b9837dfb385b1f3f841837f8eb5c625cd91964&sn=11485
    ad = 'https://api.gamer.com.tw/mobile_app/anime/v1/stat_ad.php'  #?sn=11485&schedule=196718

sn = '1908'
device = '0246109813da3cd2dc9d76b9837dfb385b1f3f841837f8eb5c625cd91964'

token = 'e_DX0VJHbJ8'

response = session.post(API.login, data={'token': token})

uid = 'SinoharaHare'
passwd = 'anna1822'


'''
response = requests.get(API.video, params={'sn': sn})

with io.open(f'{sn}.json', 'w', encoding='UTF-8') as f:
    json.dump(response.json(), f, ensure_ascii=False)
'''
'''
params = {
    'sn': sn,
    'device': device,
}
session.get(API.ad, params={'sn': sn})
while True:
    session.get(API.ad, params={'sn': sn, 'ad': 'end'})
    response = session.get(API.m3u8, params=params)
    try:
        src = response.json()['src']
    except KeyError:
        time.sleep(0.1)
        continue
    break
'''

print(time.time() - start)
