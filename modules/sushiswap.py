from web3 import Web3
from settings import remainder_eth, SLIPPAGE, swap_decimal
from modules.wallet import Wallet, from_wei
from modules.retry import exception_handler
import json as js
import time


class SushiSwap(Wallet):

    def __init__(self, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.address = Web3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')
        self.abi = js.load(open('./abi/sushi.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        self.token_remove_abi = js.load(open('./abi/Token_remove.txt'))

    @exception_handler('Buy token on SushiSwap')
    def buy_token(self, token_to_buy, prescale):
        self.log.info(f'Buy {token_to_buy["name"]} token on SushiSwap')

        balance = self.web3.eth.get_balance(self.address_wallet) - Web3.to_wei(remainder_eth, 'ether')
        if balance < 0:
            self.log.info('Insufficient funds')
            return 'balance'
        value = int(balance * prescale)
        value_wei = round(Web3.from_wei(value, 'ether'), swap_decimal)
        value = Web3.to_wei(value_wei, 'ether')

        amount_out = self.contract.functions.getAmountsOut(value, (self.ETH, token_to_buy['address'])).call()[1]
        min_tokens = int(amount_out - (amount_out * SLIPPAGE // 100))
        min_tok = round(from_wei(token_to_buy["decimal"], min_tokens), 5)

        contract_txn = self.contract.functions.swapExactETHForTokens(
            min_tokens,
            [self.ETH, token_to_buy['address']],
            self.address_wallet,
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        })

        self.send_transaction_and_wait(contract_txn, f'Buy {min_tok} {token_to_buy["name"]} SushiSwap')

    @exception_handler('Sold token SushiSwap')
    def sold_token(self, token_to_sold):
        self.log.info(f'Sold {token_to_sold["name"]} token on SushiSwap')

        token_contract = self.web3.eth.contract(address=token_to_sold['address'], abi=self.token_abi)
        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            self.log.info(f'Balance {token_to_sold["name"]} - 0\n')
            return
        decimal = token_contract.functions.decimals().call()
        allowance = token_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < 10000 * 10 ** decimal:
            self.log.info('Нужен аппрув, делаю')
            self.approve(token_to_sold['address'], self.address)
            time.sleep(60)

        amount_out = self.contract.functions.getAmountsOut(token_balance, [token_to_sold['address'], self.ETH]).call()[1]
        min_tokens = int(amount_out - (amount_out * SLIPPAGE // 100))
        min_tok = round(from_wei(token_to_sold["decimal"], token_balance), 5)

        contract_txn = self.contract.functions.swapExactTokensForETH(
            token_balance,
            min_tokens,
            [token_to_sold['address'], self.ETH],
            self.address_wallet,
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
        })

        self.send_transaction_and_wait(contract_txn, f'Sold {min_tok} {token_to_sold["name"]} SushiSwap')

    @exception_handler('Add token SushiSwap')
    def add_liquidity(self, token_to_add):
        self.log.info(f'Add Liquidity {token_to_add["name"]} token on SushiSwap')

        token_contract = self.web3.eth.contract(address=token_to_add['address'], abi=self.token_abi)
        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            self.log.info(f'Balance {token_to_add["name"]} - 0\n')
            return
        decimal = token_contract.functions.decimals().call()
        allowance = token_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < 10000 * 10 ** decimal:
            self.log.info('Нужен аппрув, делаю')
            self.approve(token_to_add['address'], self.address)
            time.sleep(60)

        amount_out = self.contract.functions.getAmountsOut(token_balance, [token_to_add['address'], self.ETH]).call()[1]
        amount_out_eth = int(amount_out - (amount_out * SLIPPAGE // 100))
        min_tok = round(from_wei(token_to_add["decimal"], token_balance), 5)

        contract_txn = self.contract.functions.addLiquidityETH(
            token_to_add['address'],
            token_balance,
            int(token_balance - (token_balance * SLIPPAGE // 100)),
            amount_out_eth,
            self.address_wallet,
            (int(time.time()) + 10000),  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'value': amount_out
        })

        self.send_transaction_and_wait(contract_txn, f'Add {min_tok} {token_to_add["name"]} SushiSwap')

    @exception_handler('Remove liquidity SushiSwap')
    def remove_liquidity(self, token_to_remove):
        self.log.info(f'Remove Liquidity {token_to_remove["name"]} token on SushiSwap')

        token_contract = self.web3.eth.contract(address=token_to_remove['lp sushi'], abi=self.token_remove_abi)
        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            self.log.info(f'Balance {token_to_remove["name"]} - 0\n')
            return 'token 0'
        decimal = token_contract.functions.decimals().call()
        allowance = token_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < 10000 * 10 ** decimal:
            self.log.info('Нужен аппрув, делаю')
            self.approve(token_to_remove['lp sushi'], self.address)
            time.sleep(60)

        price_eth1, price_token1, _ = token_contract.functions.getReserves().call()
        price_eth = int(price_eth1 / token_balance)
        price_token = int(price_token1 / token_balance)

        amount_eth_min = int(price_eth - (price_eth * SLIPPAGE // 100))
        amount_token_min = int(price_token - (price_token * SLIPPAGE // 100))

        contract_txn = self.contract.functions.removeLiquidityETH(
            token_to_remove['address'],
            token_balance,
            amount_token_min,
            amount_eth_min,
            self.address_wallet,
            (int(time.time()) + 10000),  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet)
        })

        self.send_transaction_and_wait(contract_txn, f'Remove {token_to_remove["name"]} SushiSwap')
