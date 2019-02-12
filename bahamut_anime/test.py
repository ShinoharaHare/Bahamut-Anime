import time
from functools import wraps

from anime import *


def timer(func):
    @wraps(func)
    def wrapper(*args):
        start_time = time.time()
        func(*args)
        print(time.time() - start_time)
    return wrapper

@timer
def main():
    sao3 = Anime(10849)
    print(sao3.m3u8().segments[0].absolute_uri)
if __name__ == "__main__":
    main()
