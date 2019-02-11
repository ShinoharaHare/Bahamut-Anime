import re
import time
import weakref
from urllib.parse import *
from collections import OrderedDict

import m3u8
import requests
from bs4 import BeautifulSoup

__all__ = ['Anime', 'Series']

_BASE_URL = 'https://ani.gamer.com.tw'
_ANIME_URL = urljoin(_BASE_URL, 'animeVideo.php')
_CASTCISHU_URL = urljoin(_BASE_URL, 'ajax/videoCastcishu.php')
_M3U8_URL = urljoin(_BASE_URL, 'ajax/m3u8.php')
_DEVICE_URL = urljoin(_BASE_URL, 'ajax/getdeviceid.php')
_HEADERS = {
    'Origin': _BASE_URL,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

class Score:
    def __init__(self, div):
        self.score = None
        self.reviewers = None
        self.percentage = {}
    
    def __str__(self):
        return self.score

class Category:
    def __init__(self, div):
        pass

class _Anime:

    def __init__(self, sn):
        self.sn = sn
        self._session = requests.session()
        self._session.headers = _HEADERS

        self._ad_id = None
        self._device_id = None
        self._playlist = None
        self._m3u8s = [None, None, None, None]
        self._load_basic_info()
    
    def _load_basic_info(self):
        response = self._session.get(_ANIME_URL, params={'sn': self.sn})
        self._soup = BeautifulSoup(response.content, 'html.parser')

        #重要資訊
        pattern = re.compile(r'animefun.videoSn')
        script = self._soup.find('script', string=pattern).string
        
        self.title = re.search(r'title = (.*);', script).group(1)
        self.episode = re.search(r'\[(.*)\]', self.title).group(1)
        self.next_sn = re.search(r'nextSn = (.*);', script).group(1)
        self.previous_sn = re.search(r'preSn = (.*);', script).group(1)

        '''
        if ul:
            get_sn_from_href = lambda x: parse_qs(urlparse(x).query)['sn'][0]
            sn_list = list(map(lambda x: get_sn_from_href(x.a['href']), ul))

            for i, li in enumerate(ul.children):
                if 'playing' in li['class']: current = i
                latest = i
            
            self.episode = current + 1
            self.first_sn = sn_list[0] if current != 0 else None
            self.latest_sn = sn_list[latest] if current != latest else None
            self.next_sn = sn_list[current + 1] if self.latest_sn else None
            self.previous_sn = sn_list[current - 1] if self.first_sn else None
        '''

        #無用資訊
        pattern = re.compile(r'上架時間：(.*)')
        string = self._soup.find('p', string=pattern).string
        self.upload_date = pattern.search(string).group(1)
        self.description = self._soup.find('meta', attrs={"name":"description"})['content']
        self.score = Score(self._soup.find('div', class_='data_acgbox'))
        self.category = Category(self._soup.find('div', class_='data_type'))

    '''
    def get_first_episode(self):
        return Anime(self.first_sn) if self.first_sn else self
    
    def get_latest_episode(self):
        return Anime(self.latest_sn) if self.latest_sn else self
    '''

    def next(self):
        return Anime(self.next_sn) if self.next_sn != '0' else None

    def previous(self):
        return Anime(self.previous_sn) if self.previous_sn != '0' else None
    
    def series(self):
        return Series(self.sn)

    def reload(self):
        self._playlist = None
        self._m3u8s = [None, None, None, None]

    @property
    def device_id(self):
        if not self._device_id: self._receive_device_id()
        return self._device_id
    
    @property
    def playlist(self):
        if not self._playlist: self._receive_playlist()
        return self._playlist

    def m3u8(self, resolution=None):
        key = ['360p', '540p', '720p', '1080p']
        
        if resolution is None:
            resolution = len(self.playlist.playlists) - 1
        elif resolution in res:
            resolution = key.index(resolution)
        
        if not self._m3u8s[resolution]:
            self._receive_m3u8(resolution)

        return self._m3u8s[resolution]

    def m3u8s(self):
        for i in range(len(self.playlist.playlists)):
            if not self._m3u8s[i]:
                self._receive_m3u8(i)
        
        return self._m3u8s

    '''
    @property
    def ad_id(self):
        if not self._ad_id: self._receive_ad_id()
        return self._ad_id

    def _receive_ad_id(self):
        src = self._soup.find('script', src=re.compile(r'animeVideo.js'))['src']
        response = self._session.get(src)
        js = response.text
        pattern = re.compile(r'var adlist = (.*);')
        adlist = eval(pattern.search(js).group(1))
        self._ad_id = random.choice(adlist)[0]
    '''

    def _receive_device_id(self):
        response = self._session.get(_DEVICE_URL)
        json = response.json()
        self._device_id = json['deviceid']

    def _receive_playlist(self):
        params = {'sn': self.sn}
        self._session.get(_CASTCISHU_URL, params=params)
        params.update({'ad': 'end'})
        while True:
            self._session.get(_CASTCISHU_URL, params=params)
            response = self._session.get(_M3U8_URL, params={'sn': self.sn, 'device': self.device_id})
            json = response.json()
            src = json['src']
            if src: break
            else: time.sleep(0.1)
        src = 'https:' + src.replace(r'\/', r'/')
        response = self._session.get(src)
        self._playlist = m3u8.loads(response.text, uri=src)

    def _receive_m3u8(self, index):
        p = self.playlist.playlists[index]
        response = self._session.get(p.absolute_uri)
        self._m3u8s[index] = m3u8.loads(response.text, uri=p.absolute_uri)
            
    def __str__(self):
        return self.title

    def __del__(self):
        self._session.close()


class _Series:
    def __init__(self, sn):
        anime = Anime(sn)

        pattern = re.compile(r'(.*)\[.*\]')
        self.title = pattern.search(anime.title).group(1).strip()

        ul = anime._soup.find('ul', id='vul0_000')
        self._sns = OrderedDict()
        self._cached = set([anime])

        if ul:
            get_sn = lambda x: parse_qs(urlparse(x).query)['sn'][0]
            for li in ul:
                self._sns[li.string] = get_sn(li.a['href'])
        else:
            self._sns[anime.episode] = sn
    
    def cache(self):
        list(self)

    def __getitem__(self, key):
        if type(key) is int:
            keys = list(self._sns.keys())
            #key = key - 1 if key > 0 else key
            key = keys[key]

        anime = Anime(self._sns[key])    
        self._cached.add(anime)
        return anime

    def __len__(self):
        return len(self._sns)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
            
    def __str__(self):
        return self.title

def Anime(sn):
    if not hasattr(Anime, 'cache'):
        Anime.cache = weakref.WeakSet()

    sn = str(sn)
    for a in Anime.cache: 
        if sn == a.sn:
            return a
    
    anime = _Anime(sn)
    Anime.cache.add(anime)
    return anime

def Series(sn):
    if not hasattr(Series, 'cache'): 
        Series.cache = weakref.WeakSet()

    sn = str(sn)
    
    for s in Series.cache:
        if sn == list(s._sns.values())[0]:
            return s
    
    series = _Series(sn)
    Series.cache.add(series)
    return series