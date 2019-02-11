import time

from anime import *


def _timer(func):
    def wrapper(*args):
        start_time = time.time()
        func(*args)
        print(time.time() - start_time)
    return wrapper

@_timer
def main():
    sao3 = Anime(10849)
    print(sao3.next())

if __name__ == "__main__":
    main()
