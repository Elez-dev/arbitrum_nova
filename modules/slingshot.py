from modules.approve import Approve, from_wei
from modules.tg_bot import TgBot
from requests import ConnectionError
from web3.exceptions import TransactionNotFound
from web3 import Web3
from settings import remainder_eth, swap_decimal
import requests
import json as js
import time

url_slingshot = 'https://slingshot.finance/api/v3/trade/'
eth = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'


class Slingshot(Approve, TgBot):

    def __init__(self, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.web3 = web3
        self.number = number
        self.log = log
        self.private_key = private_key
        self.address_wallet = self.web3.eth.account.from_key(private_key).address
        self.token_abi = js.load(open('./abi/Token.txt'))

    def buy_token(self, token_to_buy, prescale, retry=0):
        try:
            self.log.info(f'Buy {token_to_buy["name"]} token on Slingshot')

            balance = self.web3.eth.get_balance(self.address_wallet) - Web3.to_wei(remainder_eth, 'ether')
            if balance < 0:
                self.log.info('Insufficient funds')
                return 'balance'
            value = int(balance * prescale)
            value_wei = round(Web3.from_wei(value, 'ether'), swap_decimal)
            value = Web3.to_wei(value_wei, 'ether')

            json = {
                'from': eth,
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

            res = requests.post(url=url_slingshot, json=json, headers=headers)
            json_data = res.json()

            min_tok = round(from_wei(token_to_buy['decimal'], int(json_data['estimatedOutput'])), 5)

            txn = {
                'chainId': 42170,
                'data': json_data['txData'],
                'from': self.address_wallet,
                'to': Web3.to_checksum_address('0x970bec30E2c5A1e435761332bD3659ad6745D839'),
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
                'maxFeePerGas': self.web3.eth.gas_price,
                'maxPriorityFeePerGas': 0,
                'value': value
            }

            gas = self.web3.eth.estimate_gas(txn)
            txn.update({'gas': gas})

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.log.info('Отправил транзакцию')
            time.sleep(1)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=20)
            if tx_receipt.status == 1:
                self.log.info(f'Транзакция смайнилась успешно')
            else:
                self.log.error('Транзакция сфейлилась, пытаюсь еще раз')
                if TgBot.TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Buy token Slingshot', self.address_wallet,
                                             'Транзакция сфейлилась, пытаюсь еще раз')
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.buy_token(token_to_buy, prescale, retry)
                return

            self.log.info(f'[{self.number}] Buy {min_tok} {token_to_buy["name"]} Slingshot || https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, f'Buy {min_tok} {token_to_buy["name"]} Slingshot', self.address_wallet,
                                           f'https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}')

        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Buy token 1inch', self.address_wallet,
                                         'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.buy_token(token_to_buy, prescale, retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Buy token Slingshot', self.address_wallet,
                                         'Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.buy_token(prescale, prescale, retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'Buy token Slingshot', self.address_wallet,
                                                 'Ошибка, скорее всего нехватает комсы')
                    return 'balance'
                else:
                    self.log.info(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.buy_token(token_to_buy, prescale, retry)
            else:
                self.log.info(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.buy_token(token_to_buy, prescale, retry)

    def sold_token(self, token_to_sold, retry=0):
        try:
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
                'to': eth,
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

            res = requests.post(url=url_slingshot, json=json, headers=headers)
            json_data = res.json()

            min_tok = round(from_wei(int(token_to_sold["decimal"]), token_balance), 5)

            txn = {
                'chainId': 42170,
                'data': json_data['txData'],
                'from': self.address_wallet,
                'to': Web3.to_checksum_address('0x970bec30E2c5A1e435761332bD3659ad6745D839'),
                'maxFeePerGas': self.web3.eth.gas_price,
                'maxPriorityFeePerGas': 0,
                'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            }

            gas = self.web3.eth.estimate_gas(txn)
            txn.update({'gas': gas})

            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            self.log.info('Отправил транзакцию')
            time.sleep(1)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=20)
            if tx_receipt.status == 1:
                self.log.info(f'Транзакция смайнилась успешно')
            else:
                self.log.error('Транзакция сфейлилась, пытаюсь еще раз')
                if TgBot.TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Sold token Slingshot', self.address_wallet,
                                             'Транзакция сфейлилась, пытаюсь еще раз')
                time.sleep(30)
                retry += 1
                if retry > 5:
                    return 0
                self.sold_token(token_to_sold, retry)
                return

            self.log.info(f'[{self.number}] Sold {min_tok} {token_to_sold["name"]} Slingshot || https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}\n')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_success(self, self.number, f'Sold {min_tok} {token_to_sold["name"]} Slingshot', self.address_wallet,
                                           f'https://nova.arbiscan.io/tx/{Web3.to_hex(tx_hash)}')

        except TransactionNotFound:
            self.log.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Sold token Slingshot', self.address_wallet,
                                         'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.sold_token(token_to_sold, retry)

        except ConnectionError:
            self.log.error('Ошибка подключения к интернету или проблемы с РПЦ')
            if TgBot.TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, 'Sold token Slingshot', self.address_wallet,
                                         'Ошибка подключения к интернету или проблемы с РПЦ')
            time.sleep(60)
            retry += 1
            if retry > 5:
                return 0
            self.sold_token(token_to_sold, retry)

        except Exception as error:
            if isinstance(error.args[0], dict):
                if 'insufficient funds' in error.args[0]['message']:
                    self.log.error('Ошибка, скорее всего нехватает комсы')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'Sold token Slingshot', self.address_wallet,
                                                 'Ошибка, скорее всего нехватает комсы')
                    return 'balance'
                else:
                    self.log.error(error)
                    time.sleep(60)
                    retry += 1
                    if retry > 5:
                        return 0
                    self.sold_token(token_to_sold, retry)
            else:
                self.log.error(error)
                time.sleep(60)
                retry += 1
                if retry > 5:
                    return 0
                self.sold_token(token_to_sold, retry)
