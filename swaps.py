from web3 import Web3
from modules.arbswap import ArbSwap
from modules.rpcswap import RpcSwap
from modules.slingshot import Slingshot
from modules.sushiswap import SushiSwap
from requests.adapters import Retry
from threading import Thread
from settings import *
import logging
import requests
import random
import time
import threading


token_arr = [

    {
        'name': 'USDC',
        'address': Web3.to_checksum_address('0x750ba8b76187092B0D1E87E28daaf484d1b5273b'),
        'decimal': 6
    },

    {
        'name': 'DAI',
        'address': Web3.to_checksum_address('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1'),
        'decimal': 18
    },

    {
        'name': 'WBTC',
        'address': Web3.to_checksum_address('0x1d05e4e72cd994cdf976181cfb0707345763564d'),
        'decimal': 8
    },

    {
        'name': 'ARB',
        'address': Web3.to_checksum_address('0xf823C3cD3CeBE0a1fA952ba88Dc9EEf8e0Bf46AD'),
        'decimal': 18
    }
]


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
    def __init__(self):
        super().__init__()

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

            arr_buy = []

            if SLINGSHOT is True:
                sling = Slingshot(private_key, web3, str_number, log)
                arr_buy.append(sling)
            if SUSHISWAP is True:
                sushi = SushiSwap(private_key, web3, str_number, log)
                arr_buy.append(sushi)
            if ARBSWAP is True:
                arb = ArbSwap(private_key, web3, str_number, log)
                arr_buy.append(arb)
            if RPCSWAP is True:
                rpc = RpcSwap(private_key, web3, str_number, log)
                arr_buy.append(rpc)

            len_way = len(arr_buy)
            random.shuffle(arr_buy)

            if liquiditi_sushi is True and SUSHISWAP is True:
                if len_way == 1:
                    liquidity_sushi_index = 0
                else:
                    liquidity_sushi_index = random.randint(0, len_way - 1)

            if liquiditi_arb is True and ARBSWAP is True:
                if len_way == 1:
                    liquidity_arb_index = 0
                else:
                    liquidity_arb_index = random.randint(0, len_way - 1)

            if liquiditi_rpc is True and RPCSWAP is True:
                if len_way == 1:
                    liquidity_rpc_index = 0
                else:
                    liquidity_rpc_index = random.randint(0, len_way - 1)

            flag_liquiditi_sushi = False
            flag_liquiditi_arb   = False
            flag_liquiditi_rpc   = False

            total_number_of_repetitions = random.randint(total_number_of_repetitions_min, total_number_of_repetitions_max)

            for i in range(total_number_of_repetitions):

                if len_way == 1:

                    token_to_swap = random.choice(token_arr)

                    value_swap = round(random.uniform(prescale_swap_min, prescale_swap_max), swap_decimal)
                    res = arr_buy[0].buy_token(token_to_swap, value_swap)
                    if res == 'balance':
                        break
                    time.sleep(random.randint(time_delay_min, time_delay_max))

                    res = arr_buy[0].sold_token(token_to_swap)
                    if res == 'balance':
                        break
                    time.sleep(random.randint(time_delay_min, time_delay_max))

                    if liquiditi_sushi is True and flag_liquiditi_sushi is False:
                        token_to_swap = random.choice(token_arr)
                        value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                        res = sushi.buy_token(token_to_swap, value_liquid)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        res = sushi.add_liquidity(token_to_swap)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        flag_liquiditi_sushi = True

                    if liquiditi_rpc is True and flag_liquiditi_rpc is False:
                        token_to_swap = random.choice(token_arr)
                        value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                        res = rpc.buy_token(token_to_swap, value_liquid)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        res = rpc.add_liquidity(token_to_swap)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        flag_liquiditi_rpc = True

                    if liquiditi_arb is True and flag_liquiditi_arb is False:
                        token_to_swap = random.choice(token_arr)
                        value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                        res = arb.buy_token(token_to_swap, value_liquid)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        res = arb.add_liquidity(token_to_swap)
                        if res == 'balance':
                            break
                        time.sleep(random.randint(time_delay_min, time_delay_max))
                        flag_liquiditi_arb = True

                else:

                    for j in range(len_way - 1):

                        number_of_repetitions = random.randint(number_of_repetitions_min, number_of_repetitions_max)
                        for k in range(number_of_repetitions):

                            token_to_swap = random.choice(token_arr)

                            log.info(f'Круг на конкретной свапалке - {k+1}')
                            value_swap = round(random.uniform(prescale_swap_min, prescale_swap_max), swap_decimal)
                            res = arr_buy[j].buy_token(token_to_swap, value_swap)
                            if res == 'balance':
                                break
                            time.sleep(random.randint(time_delay_min, time_delay_max))

                            res = arr_buy[j].sold_token(token_to_swap)
                            if res == 'balance':
                                break
                            time.sleep(random.randint(time_delay_min, time_delay_max))

                        if FLAG is True:
                            break

                        if liquiditi_sushi is True and flag_liquiditi_sushi is False:
                            if liquidity_sushi_index == j:
                                token_to_swap = random.choice(token_arr)
                                value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                                res = sushi.buy_token(token_to_swap, value_liquid)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                res = sushi.add_liquidity(token_to_swap)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                flag_liquiditi_sushi = True

                        if liquiditi_rpc is True and flag_liquiditi_rpc is False:
                            if liquidity_rpc_index == j:
                                token_to_swap = random.choice(token_arr)
                                value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                                res = rpc.buy_token(token_to_swap, value_liquid)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                res = rpc.add_liquidity(token_to_swap)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                flag_liquiditi_rpc = True

                        if liquiditi_arb is True and flag_liquiditi_arb is False:
                            if liquidity_arb_index == j:
                                token_to_swap = random.choice(token_arr)
                                value_liquid = random.uniform(liquidity_prescale_min, liquidity_prescale_max)
                                res = arb.buy_token(token_to_swap, value_liquid)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                res = arb.add_liquidity(token_to_swap)
                                if res == 'balance':
                                    break
                                time.sleep(random.randint(time_delay_min, time_delay_max))
                                flag_liquiditi_arb = True

            session.close()


if __name__ == '__main__':
    with open("private_keys.txt", "r") as f:
        list1 = [row.strip() for row in f if row.strip()]
    keys_list = shuffle(list1)
    all_wallets = len(keys_list)
    print(f'Number of wallets: {all_wallets}\n')
    for _ in range(number_of_threads):
        worker = Worker()
        worker.start()
        time.sleep(random.randint(TIME_DELAY_MIN, TIME_DELAY_MAX))
