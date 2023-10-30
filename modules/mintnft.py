from modules.tg_bot import TgBot
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from web3 import Web3
import time


class Mint(TgBot):

    def __init__(self, private_key, web3, number, log):
        self.web3 = web3
        self.number = number
        self.log = log
        self.private_key = private_key
        self.address_wallet = self.web3.eth.account.from_key(private_key).address

    def mint_nft(self, retry=0):
        try:

            txn = {
                'chainId': 42170,
                'data': '0x1249c58b',
                'from': self.address_wallet,
                'to': Web3.to_checksum_address('0x5188368a92b49f30f4cf9bef64635bcf8459c7a7'),
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'maxFeePerGas': self.web3.eth.gas_price,
                'maxPriorityFeePerGas': 0,
                'value': Web3.to_wei(0.000056, 'ether')
            }

            gas = self.web3.eth.estimate_gas(txn)
            txn.update({'gas': gas})

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.log.info('Отправил транзакцию')
            time.sleep(1)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=10)
            if tx_receipt.status == 1:
                self.log.info(f'Транзакция смайнилась успешно')
            else:
                self.log.error('Транзакция сфейлилась, пытаюсь еще раз')
                if TgBot.TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Mint NFT on Zerius', self.address_wallet,
                                             'Транзакция сфейлилась, пытаюсь еще раз')
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.mint_nft(retry)
                return

            self.log.info(f'[{self.number}] Mint NFT on Zerius || https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, f'Mint NFT on Zerius', self.address_wallet,
                                           f'https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}')

        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Mint NFT on Zerius', self.address_wallet,
                                         'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.mint_nft(retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Mint NFT on Zerius', self.address_wallet,
                                         'Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.mint_nft(retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'Mint NFT on Zerius', self.address_wallet,
                                                 'Ошибка, скорее всего нехватает комсы')
                    return 'balance'
                else:
                    self.log.info(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.mint_nft(retry)
            else:
                self.log.info(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.mint_nft(retry)
