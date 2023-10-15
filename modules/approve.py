from web3 import Web3
import json as js
import time
from modules.tg_bot import TgBot
from web3.exceptions import TransactionNotFound


class Approve(TgBot):
    def __init__(self, private_key, web3, number, log):
        self.private_key = private_key
        self.number = number
        self.log = log
        self.web3 = web3
        self.address_wallet = self.web3.eth.account.from_key(private_key).address
        self.token_abi = js.load(open('./abi/Token.txt'))

    def approve(self, token_to_approve, address_to_approve, retry=0):
        token_contract = self.web3.eth.contract(address=token_to_approve, abi=self.token_abi)
        max_amount = 2 ** 256 - 1
        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        }
        try:
            txn = token_contract.functions.approve(address_to_approve, max_amount).build_transaction(dick)
            signed_tx = self.web3.eth.account.sign_transaction(txn, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.log.info('Отправил транзакцию')
            time.sleep(5)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=20)
            if tx_receipt.status == 1:
                self.log.info(f'Транзакция смайнилась успешно')
            else:
                self.log.error(f'Транзакция сфейлилась, пытаюсь еще раз')
                if TgBot.TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'approve', self.address_wallet, 'Транзакция сфейлилась, пытаюсь еще раз')
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.approve(token_to_approve, address_to_approve, retry)
                return

            self.log.info(f'[{self.number}] approve || https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, 'approve', self.address_wallet,
                                           f'https://explorer.zksync.io/tx/{Web3.to_hex(tx_hash)}')
        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'approve', self.address_wallet,
                                         'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.approve(token_to_approve, address_to_approve, retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'approve', self.address_wallet,
                                         'Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.approve(token_to_approve, address_to_approve, retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'approve', self.address_wallet,
                                                 'Ошибка, скорее всего нехватает комсы')
                    return 0
                else:
                    self.log.error(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.approve(token_to_approve, address_to_approve, retry)
            else:
                self.log.error(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.approve(token_to_approve, address_to_approve, retry)


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
