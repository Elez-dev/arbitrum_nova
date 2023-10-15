from modules.tg_bot import TgBot
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from web3 import Web3
from settings import remainder_eth, bridge_decimal
import time


class OfBridge(TgBot):

    def __init__(self, private_key, web3, number, log):
        self.web3 = web3
        self.number = number
        self.log = log
        self.private_key = private_key
        self.address_wallet = self.web3.eth.account.from_key(private_key).address
        self.address = Web3.to_checksum_address('0xc4448b71118c9071Bcb9734A0EAc55D18A153949')

    def deposit(self, prescale, retry=0):
        try:
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

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.log.info('Отправил транзакцию')
            self.log.info(f'Ожидаю подтверждения транзакции || https://etherscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            time.sleep(1)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=600, poll_latency=20)
            if tx_receipt.status == 1:
                self.log.info(f'Транзакция смайнилась успешно')
            else:
                self.log.error('Транзакция сфейлилась, пытаюсь еще раз')
                if TgBot.TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Deposit Eth from Ethereum to Arbitrum Nova', self.address_wallet,
                                             'Транзакция сфейлилась, пытаюсь еще раз')
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.deposit(prescale, retry)
                return

            self.log.info(f'[{self.number}] Deposit {value_wei} Eth from Ethereum to Arbitrum Nova || https://etherscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, f'Deposit {value_wei} Eth from Ethereum to Arbitrum Nova', self.address_wallet,
                                           f'https://etherscan.io/tx/{Web3.to_hex(tx_hash)}')

        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Deposit Eth from Ethereum to Arbitrum Nova', self.address_wallet,
                                         'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.deposit(prescale, retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Deposit Eth from Ethereum to Arbitrum Nova', self.address_wallet,
                                         'Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.deposit(prescale, retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'Deposit Eth from Ethereum to Arbitrum Nova', self.address_wallet,
                                                 'Ошибка, скорее всего нехватает комсы')
                    return 'balance'
                else:
                    self.log.error(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.deposit(prescale, retry)
            else:
                self.log.error(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.deposit(prescale, retry)
