# My imports
import ftdi_uart
import parse

from collections import deque
#from multiprocessing import Process
from threading import Thread,Event
from time import sleep

def main():
    run_event = Event()
    run_event.set()

    q = deque()
    ftdi_thread = Thread(target=ftdi_uart.ftdi_trx,
            kwargs = {'run_event':run_event,'q':q})
    parse_thread = Thread(target=parse.parse,
            kwargs = {'run_event':run_event,'q':q})

    ftdi_thread.start()
    parse_thread.start()

    try:
        while True:
            sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        run_event.clear()
        ftdi_thread.join()
        parse_thread.join()
        raise
    except:
        run_event.clear()
        ftdi_thread.join()
        parse_thread.join()
        raise

if __name__ == "__main__":
    main()
