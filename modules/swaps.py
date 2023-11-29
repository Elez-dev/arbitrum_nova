from modules.wallet import Wallet
from modules.arbswap import ArbSwap
from modules.rpcswap import RpcSwap
from modules.slingshot import Slingshot
from modules.sushiswap import SushiSwap
from settings import *
from web3 import Web3
import random
import time


token_arr = [

    {
        'name': 'USDC',
        'address': Web3.to_checksum_address('0x750ba8b76187092B0D1E87E28daaf484d1b5273b'),
        'decimal': 6,
        'lp arbswap': Web3.to_checksum_address('0xdBA61558A49c0A836A4106502cFbe5870DAD1743'),
        'lp rpc': Web3.to_checksum_address('0x66Ec0a03409E63Ae5b38f7bC5185F72e7191B17d'),
        'lp sushi': Web3.to_checksum_address('0x26d96cfC6DF8262b1bb327a2df0eDE02FDfC8874'),
    },

    {
        'name': 'DAI',
        'address': Web3.to_checksum_address('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1'),
        'decimal': 18,
        'lp arbswap': Web3.to_checksum_address('0x3a94C233A80d7aDA126C1a7A6657de4513AD5D76'),
        'lp rpc': Web3.to_checksum_address('0xCBFb05f74A0cf83BD8C091c5B6CFa46769e8E6a1'),
        'lp sushi': Web3.to_checksum_address('0x5c7966CebD4027266bd5163a8aB04331Ade9C78c'),
    },

    {
        'name': 'WBTC',
        'address': Web3.to_checksum_address('0x1d05e4e72cd994cdf976181cfb0707345763564d'),
        'decimal': 8,
    },

    {
        'name': 'ARB',
        'address': Web3.to_checksum_address('0xf823C3cD3CeBE0a1fA952ba88Dc9EEf8e0Bf46AD'),
        'decimal': 18,
        'lp arbswap': Web3.to_checksum_address('0x9Edb75c256d991D7b418fb81af6695c884495884'),
        'lp rpc': Web3.to_checksum_address('0xE1e16731E0F7F642Ec073AD1d10cba693ef272e8'),
        'lp sushi': Web3.to_checksum_address('0x39EC31B1D7eeC08F1b1af15b18826BFE4e26Af1D'),
    }
]

token_arr1 = token_arr.copy()
del token_arr1[2]


class Swaps(Wallet):
    def __init__(self, private_key, web3, str_number, log):
        super().__init__(private_key, web3, str_number, log)

    def swap(self):
        arr_buy = []

        if SLINGSHOT is True:
            sling = Slingshot(self.private_key, self.web3, self.number, self.log)
            arr_buy.append(sling)
        if SUSHISWAP is True:
            sushi = SushiSwap(self.private_key, self.web3, self.number, self.log)
            arr_buy.append(sushi)
        if ARBSWAP is True:
            arb = ArbSwap(self.private_key, self.web3, self.number, self.log)
            arr_buy.append(arb)
        if RPCSWAP is True:
            rpc = RpcSwap(self.private_key, self.web3, self.number, self.log)
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
        flag_liquiditi_arb = False
        flag_liquiditi_rpc = False

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
                    token_to_swap = random.choice(token_arr1)
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
                    token_to_swap = random.choice(token_arr1)
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
                    token_to_swap = random.choice(token_arr1)
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

                        self.log.info(f'Круг на конкретной свапалке - {k + 1}')
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
                            token_to_swap = random.choice(token_arr1)
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
                            token_to_swap = random.choice(token_arr1)
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
                            token_to_swap = random.choice(token_arr1)
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

            random.shuffle(arr_buy)

    def remove_liquidity(self):
        dexs = []
        if SUSHISWAP is True:
            sushi = SushiSwap(self.private_key, self.web3, self.number, self.log)
            dexs.append(sushi)

        if ARBSWAP is True:
            arb = ArbSwap(self.private_key, self.web3, self.number, self.log)
            dexs.append(arb)

        if RPCSWAP is True:
            rpc = RpcSwap(self.private_key, self.web3, self.number, self.log)
            dexs.append(rpc)

        random.shuffle(dexs)
        for dex in dexs:
            for token in token_arr1:
                res = dex.remove_liquidity(token)
                if res != 'token 0':
                    time.sleep(random.randint(time_delay_min, time_delay_max))
                else:
                    time.sleep(1)
