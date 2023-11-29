from web3 import Web3
import json as js
import time
from modules.tg_bot import TgBot
from modules.retry import exception_handler


class Wallet(TgBot):
    def __init__(self, private_key, web3, number, log):
        self.private_key = private_key
        self.number = number
        self.log = log
        self.web3 = web3
        self.address_wallet = self.web3.eth.account.from_key(private_key).address
        self.token_abi = js.load(open('./abi/Token.txt'))
        self.ETH = Web3.to_checksum_address('0x722e8bdd2ce80a4422e880164f2079488e115365')

    def send_transaction_and_wait(self, tx, message):
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        self.log.info('Отправил транзакцию')
        time.sleep(5)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=10)
        if tx_receipt.status == 1:
            self.log.info(f'Транзакция смайнилась успешно')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, message, self.address_wallet, f'https://nova.arbiscan.io/tx/{tx_hash.hex()}')
        else:
            self.log.info('Транзакция сфейлилась, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, message, self.address_wallet, 'Транзакция сфейлилась, пытаюсь еще раз')
            raise ValueError('')

        self.log.info(f'[{self.number}] {message} || https://nova.arbiscan.io/tx/{tx_hash.hex()}\n')
        return tx_hash

    @exception_handler(lable='approve')
    def approve(self, token_to_approve, address_to_approve):
        token_contract = self.web3.eth.contract(address=token_to_approve, abi=self.token_abi)
        max_amount = 2 ** 256 - 1
        dick = {
            'from': self.address_wallet,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        }
        txn = token_contract.functions.approve(address_to_approve, max_amount).build_transaction(dick)

        self.send_transaction_and_wait(txn, 'approve')


def to_wei(decimal, amount):
    if decimal == 6:
        unit = 'picoether'
    else:
        unit = 'ether'

    return Web3.to_wei(amount, unit)


def from_wei(decimal, amount):
    if decimal == 6:
        unit = 'picoether'
    elif decimal == 8:
        return float(amount / 10 ** 8)
    else:
        unit = 'ether'

    return Web3.from_wei(amount, unit)
