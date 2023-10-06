import time
from settings import *
from threading import Thread
import threading
from requests.adapters import Retry
import requests
import random
from web3 import Web3
from modules.bridge import OfBridge
import logging


def shuffle(wallets_list):
    if shuffle_wallets is True:
        random.shuffle(wallets_list)
        numbered_wallets = list(enumerate(wallets_list, start=1))
    elif shuffle_wallets is False:
        numbered_wallets = list(enumerate(wallets_list, start=1))
    else:
        raise ValueError("\nНеверное значение переменной 'shuffle_wallets'. Ожидается 'True' or 'False'.")
    return numbered_wallets


class Worker(Thread):
    def __init__(self, dep_or_with):
        super().__init__()
        self.dep_or_with = dep_or_with

    def run(self):

        log = logging.getLogger(threading.current_thread().name)
        console_out = logging.StreamHandler()
        basic_format1 = logging.Formatter('%(asctime)s : [%(name)s] : %(message)s')
        basic_format = logging.Formatter('%(asctime)s : %(message)s')
        console_out.setFormatter(basic_format1)
        file_handler = logging.FileHandler(f"LOGS/{threading.current_thread().name}.txt", 'a', 'utf-8')
        file_handler.setFormatter(basic_format)
        log.setLevel(logging.DEBUG)
        log.addHandler(console_out)
        log.addHandler(file_handler)

        while keys_list:
            account = keys_list.pop(0)
            number = account[0]
            private_key = account[1]
            rpc = RPC_ETH
            retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            adapter = requests.adapters.HTTPAdapter(max_retries=retries)
            session = requests.Session()
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            web3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 60}, session=session))

            str_number = f'{number} / {all_wallets}'
            address = web3.eth.account.from_key(private_key).address
            log.info('----------------------------------------------------------------------------')
            log.info(f'|   Сейчас работает аккаунт - {address}   |')
            log.info('----------------------------------------------------------------------------\n\n')

            bridge = OfBridge(private_key, web3, str_number, log)
            value = random.uniform(prescale_bridge_min, prescale_bridge_max)
            bridge.deposit(value)
            time.sleep(random.randint(time_delay_min, time_delay_max))
            session.close()


if __name__ == '__main__':
    with open("private_keys.txt", "r") as f:
        list1 = [row.strip() for row in f if row.strip()]
    keys_list = shuffle(list1)
    all_wallets = len(keys_list)
    print(f'Number of wallets: {all_wallets}\n')

    while True:
        print('1 - Deposit ETH')

        var = int(input('Select module: '))
        if var == 1:
            break

    for _ in range(number_of_threads):
        worker = Worker(var)
        worker.start()
        time.sleep(random.randint(TIME_DELAY_MIN, TIME_DELAY_MIN))
