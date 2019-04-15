import sys
import time

def a():
    print("in a!")
    time.sleep(5)


def b():
    print("in b!")
    time.sleep(10)


def c():
    print("in c!")
    time.sleep(10)


funcmap = {"a" : a, "b" : b, "c" : c}

if __name__ == "__main__":
    func = sys.argv[1]
    try:
        funcmap[func]()
    except KeyboardInterrupt:
        print("interrupted, exiting")
        sys.exit()
