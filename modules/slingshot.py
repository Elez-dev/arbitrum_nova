from web3 import Web3
from settings import remainder_eth, swap_decimal
from modules.wallet import Wallet, from_wei
from modules.retry import exception_handler
import requests
import time


class Slingshot(Wallet):

    def __init__(self, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.ETH = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        self.url = 'https://slingshot.finance/api/v3/trade/'

    @exception_handler('Buy token Slingshot')
    def buy_token(self, token_to_buy, prescale):
        self.log.info(f'Buy {token_to_buy["name"]} token on Slingshot')

        balance = self.web3.eth.get_balance(self.address_wallet) - Web3.to_wei(remainder_eth, 'ether')
        if balance < 0:
            self.log.info('Insufficient funds')
            return 'balance'
        value = int(balance * prescale)
        value_wei = round(Web3.from_wei(value, 'ether'), swap_decimal)
        value = Web3.to_wei(value_wei, 'ether')

        json = {
            'from': self.ETH,
            'fromAmount': str(value),
            'gasOptimized': True,
            'limit': '99',
            'recipient': self.address_wallet,
            'source': 'web',
            'threeHop': True,
            'to': token_to_buy['address'],
            'useGasAwareV2': True,
            '_unsafe': False
        }
        headers = {
            'accept': '*/*',
            'liquidityzone': 'nova',
            'origin': 'https://app.slingshot.finance',
            'referer': 'https://app.slingshot.finance/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        res = requests.post(url=self.url, json=json, headers=headers)
        json_data = res.json()

        min_tok = round(from_wei(token_to_buy['decimal'], int(json_data['estimatedOutput'])), 5)

        txn = {
            'chainId': 42170,
            'data': json_data['txData'],
            'from': self.address_wallet,
            'to': Web3.to_checksum_address('0x970bec30E2c5A1e435761332bD3659ad6745D839'),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'maxFeePerGas': self.web3.eth.gas_price,
            'maxPriorityFeePerGas': self.web3.eth.max_priority_fee,
            'value': value
        }

        gas = self.web3.eth.estimate_gas(txn)
        txn.update({'gas': gas})

        self.send_transaction_and_wait(txn, f'Buy {min_tok} {token_to_buy["name"]} Slingshot')

    @exception_handler('Sold token Slingshot')
    def sold_token(self, token_to_sold):
        self.log.info(f'Sold {token_to_sold["name"]} token on Slingshot')

        token_contract = self.web3.eth.contract(address=token_to_sold['address'], abi=self.token_abi)
        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            self.log.info(f'Balance {token_to_sold["name"]} - 0\n')
            return
        decimal = token_contract.functions.decimals().call()
        spender = Web3.to_checksum_address('0xa135b6189d2e073dfbc33c30c86bb4ecea4e2ee5')
        allowance = token_contract.functions.allowance(self.address_wallet, spender).call()
        if allowance < 10000 * 10 ** decimal:
            self.log.info('Нужен аппрув, делаю')
            self.approve(token_to_sold['address'], spender)
            time.sleep(60)

        json = {
            'from': token_to_sold['address'],
            'fromAmount': str(token_balance),
            'gasOptimized': True,
            'limit': '99',
            'recipient': self.address_wallet,
            'source': 'web',
            'threeHop': True,
            'to': self.ETH,
            'useGasAwareV2': True,
            '_unsafe': False
        }
        headers = {
            'accept': '*/*',
            'liquidityzone': 'nova',
            'origin': 'https://app.slingshot.finance',
            'referer': 'https://app.slingshot.finance/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        res = requests.post(url=self.url, json=json, headers=headers)
        json_data = res.json()

        min_tok = round(from_wei(int(token_to_sold["decimal"]), token_balance), 5)

        txn = {
            'chainId': 42170,
            'data': json_data['txData'],
            'from': self.address_wallet,
            'to': Web3.to_checksum_address('0x970bec30E2c5A1e435761332bD3659ad6745D839'),
            'maxFeePerGas': self.web3.eth.gas_price,
            'maxPriorityFeePerGas': self.web3.eth.max_priority_fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        }

        gas = self.web3.eth.estimate_gas(txn)
        txn.update({'gas': gas})

        self.send_transaction_and_wait(txn, f'Sold {min_tok} {token_to_sold["name"]} Slingshot')
