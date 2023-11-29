from modules.wallet import Wallet
from modules.retry import exception_handler
from web3 import Web3
from eth_abi.packed import encode_packed
from settings import chain_arr, nft_random_chain, nft_chain_to, gas_random_chain, gas_chain_to, gas_chain_arr, value_from, value_to, value_decimal
import json as js
import random


LAYERZERO_CHAINS_ID = {
    'avalanche' : 106,
    'polygon'   : 109,
    'ethereum'  : 101,
    'bsc'       : 102,
    'arbitrum'  : 110,
    'optimism'  : 111,
    'fantom'    : 112,
    'aptos'     : 108,
    'harmony'   : 116,
    'celo'      : 125,
    'moonbeam'  : 126,
    'fuse'      : 138,
    'gnosis'    : 145,
    'klaytn'    : 150,
    'metis'     : 151,
    'core'      : 153,
    'polygon_zkevm': 158,
    'canto'     : 159,
    'moonriver' : 167,
    'tenet'     : 173,
    'nova'      : 175,
    'kava'      : 177,
    'meter'     : 176,
    'base'      : 184,
    'zora'      : 195,
    'scroll'    : 214,
    'zksync'    : 165,
    'linea'     : 183,
    'mantle'    : 181,
}

REFUEL_CONTRACTS = {
    'optimism'      : '0x2076BDd52Af431ba0E5411b3dd9B5eeDa31BB9Eb',
    'bsc'           : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'arbitrum'      : '0x412aea168aDd34361aFEf6a2e3FC01928Fba1248',
    'polygon'       : '0x2ef766b59e4603250265EcC468cF38a6a00b84b3',
    'polygon_zkevm' : '0xBAf5C493a4c364cBD2CA83C355E75F0ff7042945',
    'zksync'        : '0xec8afef7afe586eb523c228b6baf3171b1f6dd95',
    'avalanche'     : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'gnosis'        : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E',
    'fantom'        : '0xBFd3539e4e0b1B29e8b08d17f30F1291C837a18E',
    'nova'          : '0x3Fc5913D35105f338cEfcB3a7a0768c48E2Ade8E',
    'harmony'       : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'core'          : '0xB47D82aA70f839dC27a34573f135eD6dE6CED9A5',
    'celo'          : '0xFF21d5a3a8e3E8BA2576e967888Deea583ff02f8',
    'moonbeam'      : '0xb0bea3bB2d6EDDD2014952ABd744660bAeF9747d',
    'base'          : '0x9415AD63EdF2e0de7D8B9D8FeE4b939dd1e52F2C',
    'scroll'        : '0xB074f8D92b930D3415DA6bA80F6D38f69ee4B9cf',
    'zora'          : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E',
    'linea'         : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD',
    'metis'         : '0x1b07F1f4F860e72c9367e718a30e38130114AD22',
    'mantle'        : '0x4F1C698e5cA32b28030E9d9F17C164F27aB5D866',
}


class Zerius(Wallet):

    def __init__(self, private_key, web3, number, log):
        super().__init__(private_key, web3, number, log)
        self.address_bridge = Web3.to_checksum_address('0x5188368a92b49f30f4cf9bef64635bcf8459c7a7')
        self.abi_bridge = js.load(open('./abi/bridge_nft.txt'))
        self.contract_bridge = self.web3.eth.contract(address=self.address_bridge, abi=self.abi_bridge)

        self.address_refuel = Web3.to_checksum_address('0x3Fc5913D35105f338cEfcB3a7a0768c48E2Ade8E')
        self.abi_refuel = js.load(open('./abi/refuel.txt'))
        self.contract_refuel = self.web3.eth.contract(address=self.address_refuel, abi=self.abi_refuel)

    @exception_handler('Mint NFT on Zerius')
    def mint_nft(self):

        txn = self.contract_bridge.functions.mint(Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')).build_transaction({
            'from': self.address_wallet,
            'value': Web3.to_wei(0.000011, 'ether'),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet)
        })

        self.send_transaction_and_wait(txn, 'Mint NFT on Zerius')

    @exception_handler('Bridge NFT on Zerius')
    def bridge_nft(self):

        if nft_random_chain is True:
            to_chain = random.choice(chain_arr)
        else:
            to_chain = nft_chain_to

        count = self.contract_bridge.functions.balanceOf(self.address_wallet).call()
        tokens_arr = [self.contract_bridge.functions.tokenOfOwnerByIndex(self.address_wallet, i).call() for i in range(count)]
        token_id = random.choice(tokens_arr)

        min_dst_gas = self.contract_bridge.functions.minDstGasLookup(LAYERZERO_CHAINS_ID[to_chain], 1).call()

        if min_dst_gas == 0:
            self.log.info(f'You cannot bridge on the {to_chain} network')
            if nft_random_chain is True:
                self.log.info(f'I choose another network and try again')
                raise ValueError('')
            else:
                return

        adapter_params = encode_packed(
            ["uint16", "uint256"],
            [1, min_dst_gas]
        )

        native_fee, _ = self.contract_bridge.functions.estimateSendFee(
            LAYERZERO_CHAINS_ID[to_chain],
            self.address_wallet,
            token_id,
            False,
            adapter_params
        ).call()

        contract_txn = self.contract_bridge.functions.sendFrom(
                self.address_wallet,
                LAYERZERO_CHAINS_ID[to_chain],
                self.address_wallet,
                token_id,
                self.address_wallet,
                '0x0000000000000000000000000000000000000000',
                adapter_params
            ).build_transaction(
                {
                    "from": self.address_wallet,
                    "value": native_fee,
                    "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
                }
            )

        self.send_transaction_and_wait(contract_txn, f'Bridge {token_id} NFT to {to_chain}')

    @exception_handler('Check price')
    def check_price_nft(self, to_chain):

        min_dst_gas = self.contract_bridge.functions.minDstGasLookup(LAYERZERO_CHAINS_ID[to_chain], 1).call()

        if min_dst_gas == 0:
            self.log.info(f'You cannot bridge on the {to_chain} network')
            return 1000

        adapter_params = encode_packed(
            ["uint16", "uint256"],
            [1, min_dst_gas]
        )

        native_fee, _ = self.contract_bridge.functions.estimateSendFee(
            LAYERZERO_CHAINS_ID[to_chain],
            self.address_wallet,
            1,
            False,
            adapter_params
        ).call()

        self.log.info(f'{to_chain} network bridge costs - {Web3.from_wei(native_fee, "ether")} ETH')

        return {Web3.from_wei(native_fee, "ether")}

    @exception_handler('Refuel')
    def refuel(self):

        if gas_random_chain is True:
            to_chain = random.choice(gas_chain_arr)
        else:
            to_chain = gas_chain_to

        amount = Web3.to_wei(round(random.uniform(value_from, value_to), value_decimal), 'ether')

        min_dst_gas = self.contract_refuel.functions.minDstGasLookup(LAYERZERO_CHAINS_ID[to_chain], 0).call()

        if min_dst_gas == 0:
            self.log.info(f'You cannot get gas on the {to_chain} network')
            if gas_random_chain is True:
                self.log.info(f'I choose another network and try again')
                raise ValueError('')
            else:
                return

        adapter_params = encode_packed(
            ["uint16", "uint256", "uint256", "address"],
            [2, min_dst_gas, amount, self.address_wallet]
        )

        dst_contract_address = encode_packed(["address"], [REFUEL_CONTRACTS[to_chain]])
        send_value = self.contract_refuel.functions.estimateSendFee(LAYERZERO_CHAINS_ID[to_chain], dst_contract_address, adapter_params).call()

        contract_txn = self.contract_refuel.functions.refuel(
            LAYERZERO_CHAINS_ID[to_chain],
            dst_contract_address,
            adapter_params
        ).build_transaction(
            {
                "from": self.address_wallet,
                "value": send_value[0],
                "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            }
        )

        self.send_transaction_and_wait(contract_txn, f'Refuel to {to_chain}')

    @exception_handler('Check refuel')
    def check_price_gas(self, to_chain):

        min_dst_gas = self.contract_refuel.functions.minDstGasLookup(LAYERZERO_CHAINS_ID[to_chain], 0).call()

        if min_dst_gas == 0:
            self.log.info(f'You cannot get refuel on the {to_chain} network')
            return 1000

        amount = Web3.to_wei(0.000000000000001, 'ether')

        adapter_params = encode_packed(
            ["uint16", "uint256", "uint256", "address"],
            [2, min_dst_gas, amount, self.address_wallet]
        )

        dst_contract_address = encode_packed(["address"], [REFUEL_CONTRACTS[to_chain]])

        send_value = self.contract_refuel.functions.estimateSendFee(LAYERZERO_CHAINS_ID[to_chain], dst_contract_address, adapter_params).call()

        self.log.info(f'{to_chain} network refuel costs - {Web3.from_wei(send_value[0], "ether")} ETH')

        return Web3.from_wei(send_value[0], "ether")
