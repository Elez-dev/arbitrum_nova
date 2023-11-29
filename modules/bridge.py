from modules.wallet import Wallet
from web3 import Web3
from settings import remainder_eth, bridge_decimal
from modules.retry import exception_handler
import time


class OfBridge(Wallet):

    def __init__(self, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.address = Web3.to_checksum_address('0xc4448b71118c9071Bcb9734A0EAc55D18A153949')

    @exception_handler('Deposit Eth from Ethereum to Arbitrum Nova')
    def deposit(self, prescale):
        gas = 200_000
        gas_cost = self.web3.eth.gas_price * gas
        balance = self.web3.eth.get_balance(self.address_wallet) - Web3.to_wei(remainder_eth, 'ether') - gas_cost
        if balance < 0:
            self.log.info('Insufficient funds')
            return 'balance'
        value = int(balance * prescale)
        value_wei = round(Web3.from_wei(value, 'ether'), bridge_decimal)
        value = Web3.to_wei(value_wei, 'ether')
        self.log.info(f'Deposit {value_wei} Eth from Ethereum to Arbitrum Nova')

        txn = {
            'chainId': 1,
            'data': '0x439370b1',
            'from': self.address_wallet,
            'to': self.address,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'value': value
        }

        gas = self.web3.eth.estimate_gas(txn)
        txn.update({'gas': gas})

        self.send_transaction_and_wait(txn, f'Deposit {value_wei} Eth from Ethereum to Arbitrum Nova')
