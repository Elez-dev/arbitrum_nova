from web3 import Web3
from requests.adapters import Retry
from threading import Thread
from settings import *
from modules.zerius import Zerius
from modules.swaps import Swaps
from modules.bridge import OfBridge
import logging
import requests
import random
import time
import threading


def shuffle(wallets_list):
    if shuffle_wallets is True:
        numbered_wallets = list(enumerate(wallets_list, start=1))
        random.shuffle(numbered_wallets)
    elif shuffle_wallets is False:
        numbered_wallets = list(enumerate(wallets_list, start=1))
    else:
        raise ValueError("\nНеверное значение переменной 'shuffle_wallets'. Ожидается 'True' or 'False'.")
    return numbered_wallets


class Worker(Thread):
    def __init__(self, action):
        super().__init__()
        self.action = action

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
            retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            adapter = requests.adapters.HTTPAdapter(max_retries=retries)
            session = requests.Session()
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            web3 = Web3(Web3.HTTPProvider(RPC_NOVA, request_kwargs={'timeout': 60}, session=session))
            address = web3.eth.account.from_key(private_key).address

            log.info('----------------------------------------------------------------------------')
            log.info(f'|   Сейчас работает аккаунт - {address}   |')
            log.info('----------------------------------------------------------------------------\n\n')

            str_number = f'{number} / {all_wallets}'

            if self.action == 1:

                web3 = Web3(Web3.HTTPProvider(RPC_ETH, request_kwargs={'timeout': 60}, session=session))

                bridge = OfBridge(private_key, web3, str_number, log)
                value = random.uniform(prescale_bridge_min, prescale_bridge_max)
                bridge.deposit(value)
                time.sleep(random.randint(time_delay_min, time_delay_max))

            if self.action == 2:
                swap = Swaps(private_key, web3, str_number, log)
                swap.swap()

            elif self.action == 3:
                swap = Swaps(private_key, web3, str_number, log)
                swap.remove_liquidity()

            elif self.action == 4:
                nft = Zerius(private_key, web3, str_number, log)
                number = random.randint(number_nft_min, number_nft_max)
                log.info(f'Количество NFT для минта - {number}\n')
                for i in range(number):
                    log.info(f'NFT #{i}')
                    nft.mint_nft()
                    time.sleep(random.randint(time_delay_min, time_delay_max))

            elif self.action == 5:
                nft = Zerius(private_key, web3, str_number, log)
                nft.bridge_nft()
                time.sleep(random.randint(time_delay_min, time_delay_max))

            elif self.action == 6:
                nft = Zerius(private_key, web3, str_number, log)
                nft.mint_nft()
                time.sleep(random.randint(time_delay_min, time_delay_max))
                nft.bridge_nft()
                time.sleep(random.randint(time_delay_min, time_delay_max))

            elif self.action == 7:
                nft = Zerius(private_key, web3, str_number, log)
                nft.refuel()
                time.sleep(random.randint(time_delay_min, time_delay_max))

            elif self.action == 8:
                dick = {}
                nft = Zerius(private_key, web3, str_number, log)
                for chain in chain_arr:
                    price = nft.check_price_nft(chain)
                    dick.update({chain: price})
                    time.sleep(1)
                min_key = min(dick, key=dick.get)
                min_value = dick[min_key]
                log.info('')
                log.info(f'Cheapest network {min_key} - {min_value} ETH')
                return

            elif self.action == 9:
                dick = {}
                nft = Zerius(private_key, web3, str_number, log)
                for chain in gas_chain_arr:
                    price = nft.check_price_gas(chain)
                    dick.update({chain: price})
                    time.sleep(1)

                min_key = min(dick, key=dick.get)
                min_value = dick[min_key]
                log.info('')
                log.info(f'Cheapest network {min_key} - {min_value} ETH')
                return

            session.close()
            delay = random.randint(TIME_DELAY_ACC_MIN, TIME_DELAY_ACC_MAX)
            log.info(f'Аккаунт завершен, сплю {delay} секунд и перехожу к следующему')
            time.sleep(delay)


if __name__ == '__main__':
    with open("private_keys.txt", "r") as f:
        list1 = [row.strip() for row in f if row.strip()]
    keys_list = shuffle(list1)
    all_wallets = len(keys_list)
    print(f'Number of wallets: {all_wallets}\n')

    while True:
        print('1 - Main bridge from Ethereum to Nova')
        print('2 - Swap')
        print('3 - Remove liquidity')
        print('4 - Mint NFT')
        print('5 - Bridge NFT')
        print('6 - Mint + bridge NFT')
        print('7 - Refuel')
        print('8 - Check price for bridge NFT')
        print('9 - Check price for Refuel\n')
        var = int(input('Select module: '))
        if var in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            break

    for _ in range(number_of_threads):
        worker = Worker(var)
        worker.start()
        time.sleep(random.randint(TIME_DELAY_MIN, TIME_DELAY_MAX))
