from web3 import Web3
import requests
import json as js
import random
import time
import threading

# Option
number_of_threads = 1
amount_max = 0.00005          #
amount_min = 0.00001          # price in ETH
liquidity_amount = 0.000001   #

time_delay_min = 30  # Минимальная и
time_delay_max = 60  # Максимальная задержка между акками в секундах

gas = 400000
RPC = "https://nova.arbitrum.io/rpc"
# --------------------------------------


token_arr = [
    {'symbol': 'USDC',
     'address': Web3.to_checksum_address('0x750ba8b76187092B0D1E87E28daaf484d1b5273b')},

    {'symbol': 'DAI',
     'address': Web3.to_checksum_address('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1')},

    {'symbol': 'WBTC',
     'address': Web3.to_checksum_address('0x1d05e4e72cd994cdf976181cfb0707345763564d')},

    {'symbol': 'ARB',
     'address': Web3.to_checksum_address('0xf823C3cD3CeBE0a1fA952ba88Dc9EEf8e0Bf46AD')}
]

lock = threading.Lock()


class Router:
    eth = Web3.to_checksum_address('0x722e8bdd2ce80a4422e880164f2079488e115365')
    sushi_router = Web3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')
    rpc_router = Web3.to_checksum_address('0x28e0f3ebab59a998c4f1019358388b5e2ca92cfa')
    arb_router = Web3.to_checksum_address('0xee01c0cd76354c383b8c7b4e65ea88d00b06f36f')
    slingshot_router = Web3.to_checksum_address('0xa135b6189d2e073dfbc33c30c86bb4ecea4e2ee5')
    abi_arb = '[{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_factory","internalType":"address"},{"type":"address","name":"_WETH","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"WETH","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"amountADesired","internalType":"uint256"},{"type":"uint256","name":"amountBDesired","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"},{"type":"uint256","name":"liquidity","internalType":"uint256"}],"name":"addLiquidityETH","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"amountTokenDesired","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"factory","inputs":[]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"}],"name":"getAmountIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"}],"name":"getAmountOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"reserveIn","internalType":"uint256"},{"type":"uint256","name":"reserveOut","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsIn","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"getAmountsOut","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"}]},{"type":"function","stateMutability":"pure","outputs":[{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"quote","inputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"reserveA","internalType":"uint256"},{"type":"uint256","name":"reserveB","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidity","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETH","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountToken","internalType":"uint256"},{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHWithPermit","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountETH","internalType":"uint256"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","inputs":[{"type":"address","name":"token","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountTokenMin","internalType":"uint256"},{"type":"uint256","name":"amountETHMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"amountA","internalType":"uint256"},{"type":"uint256","name":"amountB","internalType":"uint256"}],"name":"removeLiquidityWithPermit","inputs":[{"type":"address","name":"tokenA","internalType":"address"},{"type":"address","name":"tokenB","internalType":"address"},{"type":"uint256","name":"liquidity","internalType":"uint256"},{"type":"uint256","name":"amountAMin","internalType":"uint256"},{"type":"uint256","name":"amountBMin","internalType":"uint256"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"},{"type":"bool","name":"approveMax","internalType":"bool"},{"type":"uint8","name":"v","internalType":"uint8"},{"type":"bytes32","name":"r","internalType":"bytes32"},{"type":"bytes32","name":"s","internalType":"bytes32"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapETHForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactETHForTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForETH","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapExactTokensForTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256","name":"amountIn","internalType":"uint256"},{"type":"uint256","name":"amountOutMin","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactETH","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256[]","name":"amounts","internalType":"uint256[]"}],"name":"swapTokensForExactTokens","inputs":[{"type":"uint256","name":"amountOut","internalType":"uint256"},{"type":"uint256","name":"amountInMax","internalType":"uint256"},{"type":"address[]","name":"path","internalType":"address[]"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"deadline","internalType":"uint256"}]},{"type":"receive","stateMutability":"payable"}]'
    abi_rpc = '[{"type":"function","name":"getAmountsOut","inputs":[{"type":"uint256"},{"type":"address[]"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"},{"type":"bool"},{"type":"uint8"},{"type":"bytes32"},{"type":"bytes32"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactETHForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidityETH","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"getAmountIn","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapETHForExactTokens","inputs":[{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"getAmountsIn","inputs":[{"type":"uint256"},{"type":"address[]"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"WETH","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"quote","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"getAmountOut","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"addLiquidity","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidityWithPermit","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"},{"type":"bool"},{"type":"uint8"},{"type":"bytes32"},{"type":"bytes32"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidityETHWithPermit","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"},{"type":"bool"},{"type":"uint8"},{"type":"bytes32"},{"type":"bytes32"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactTokensForETHSupportingFeeOnTransferTokens","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactETHForTokens","inputs":[{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidity","inputs":[{"type":"address"},{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactTokensForTokens","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"addLiquidityETH","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapTokensForExactETH","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapTokensForExactTokens","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"factory","inputs":[],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactTokensForETH","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","inputs":[{"type":"uint256"},{"type":"uint256"},{"type":"address[]"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]},{"type":"function","name":"removeLiquidityETHSupportingFeeOnTransferTokens","inputs":[{"type":"address"},{"type":"uint256"},{"type":"uint256"},{"type":"uint256"},{"type":"address"},{"type":"uint256"}],"outputs":[{"type":"unknown"}]}]'
    abi_sushi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
    abi_token = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"usr","type":"address"}],"name":"Deny","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"usr","type":"address"}],"name":"Rely","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"usr","type":"address"}],"name":"deny","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"deploymentChainId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"usr","type":"address"}],"name":"rely","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"wards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def swap_slingshot(private_key, token_to_buy, token_to_sold, amount, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    url = 'https://slingshot.finance/api/v3/trade/'
    if token_to_sold == Router.eth:
        token_to_sold = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        amount_ = str(int(amount * 1000000000000000000))
    else:
        token_sold = web3.eth.contract(address=token_to_sold, abi=Router.abi_token)
        token_balance = Web3.from_wei(token_sold.functions.balanceOf(address_wallet).call(), 'ether')
        token_to_buy = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        amount_ = str(int(token_balance * 1000000000000000000))
    json = {
        'from': token_to_sold,
        'fromAmount': amount_,
        'gasOptimized': True,
        'limit': '99',
        'recipient': address_wallet,
        'source': 'web',
        'threeHop': True,
        'to': token_to_buy,
        '_unsafe': False
    }
    headers = {
        'accept': '*/*',
        'liquidityzone': 'nova',
        'origin': 'https://app.slingshot.finance',
        'referer': 'https://app.slingshot.finance/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    try:
        res = requests.post(url=url, json=json, headers=headers)
        jres = js.loads(res.text)
        txn = {
            'data': jres['txData'],
            'gas': gas,
            'from': address_wallet,
            'to': Web3.to_checksum_address('0x970bec30E2c5A1e435761332bD3659ad6745D839'),
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(address_wallet),
        }
        if token_to_sold == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            txn['value'] = Web3.to_wei(amount, 'ether')
        else:
            allowance = check_allowance(private_key, token_to_sold, Router.slingshot_router)
            if allowance < 10:
                approve(private_key, token_to_sold, Router.slingshot_router, symbol)
                time.sleep(25)
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Swap {symbol} Slingshot| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> swap {symbol} Slingshot error | {error}', flush=True)
        print(f'    {address_wallet}\n\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_slingshot(private_key, token_to_buy, token_to_sold, amount, symbol, retry)


def slingshot_swap(private_key, token_to_buy, token_to_sold, amount, symbol):
    swap_slingshot(private_key, token_to_buy, token_to_sold, amount, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))
    swap_slingshot(private_key, token_to_sold, token_to_buy, amount, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))


def swap_arb_buy(private_key, token_to_buy, amount, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.arb_router, abi=Router.abi_arb)
        contract_txn = contract.functions.swapExactETHForTokens(
            0,  # amountOutMin
            [Router.eth, token_to_buy],  # TokenSold, TokenBuy
            address_wallet,  # receiver
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': address_wallet,
            'value': web3.to_wei(amount, 'ether'),
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Buy {symbol} ArbSwap| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> {symbol} Buy ArbSwap error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_arb_buy(private_key, token_to_buy, amount, symbol, retry)


def swap_arb_sold(private_key, token_to_sold, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.arb_router, abi=Router.abi_arb)
        token_sold = web3.eth.contract(address=token_to_sold, abi=Router.abi_token)
        token_balance = token_sold.functions.balanceOf(address_wallet).call()
        allowance = check_allowance(private_key, token_to_sold, Router.arb_router)
        if allowance < 10:
            approve(private_key, token_to_sold, Router.arb_router, symbol)
            time.sleep(25)
        contract_txn = contract.functions.swapExactTokensForETH(
            token_balance,
            0,
            [token_to_sold, Router.eth],
            address_wallet,
            (int(time.time()) + 100000)
        ).build_transaction({
            'from': address_wallet,
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet),
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Sold {symbol} ArbSwap | https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> {symbol} Sold error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_arb_sold(private_key, token_to_sold, symbol, retry)


def arb_swap(private_key, token_to_buy, token_to_sold, amount, symbol):
    swap_arb_buy(private_key, token_to_buy, amount, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))
    swap_arb_sold(private_key, token_to_buy, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))


def swap_rpc_buy(private_key, token_to_buy, amount, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.rpc_router, abi=Router.abi_rpc)
        contract_txn = contract.functions.swapExactETHForTokens(
            0,  # amountOutMin
            [Router.eth, token_to_buy],  # TokenSold, TokenBuy
            address_wallet,  # receiver
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': address_wallet,
            'value': web3.to_wei(amount, 'ether'),
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Buy {symbol} RPC| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> {symbol} sold RPC error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_rpc_buy(private_key, token_to_buy, amount, symbol, retry)


def swap_rpc_sold(private_key, token_to_sold, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.rpc_router, abi=Router.abi_rpc)
        token_sold = web3.eth.contract(address=token_to_sold, abi=Router.abi_token)
        token_balance = token_sold.functions.balanceOf(address_wallet).call()
        allowance = check_allowance(private_key, token_to_sold, Router.rpc_router)
        if allowance < 10:
            approve(private_key, token_to_sold, Router.rpc_router, symbol)
            time.sleep(25)
        contract_txn = contract.functions.swapExactTokensForETH(
            token_balance,
            0,
            [token_to_sold, Router.eth],
            address_wallet,
            (int(time.time()) + 100000)
        ).build_transaction({
            'from': address_wallet,
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet),
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Sold {symbol} RPC| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> {symbol} sold RPC error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_rpc_sold(private_key, token_to_sold, symbol, retry)


def rpc_swap(private_key, token_to_buy, token_to_sold, amount, symbol):
    swap_rpc_buy(private_key, token_to_buy, amount, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))
    swap_rpc_sold(private_key, token_to_buy, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))


def swap_sushi_buy(private_key, token_to_buy, amount, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.sushi_router, abi=Router.abi_sushi)
        contract_txn = contract.functions.swapExactETHForTokens(
            0,  # amountOutMin
            [Router.eth, token_to_buy],
            address_wallet,  # receiver
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': address_wallet,
            'value': web3.to_wei(amount, 'ether'),
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Buy {symbol} Sushiswap| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> Buy {symbol} Sushiswap error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_sushi_buy(private_key, token_to_buy, amount, symbol, retry)


def swap_sushi_sold(private_key, token_to_sold, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        contract = web3.eth.contract(address=Router.sushi_router, abi=Router.abi_sushi)
        token_sold = web3.eth.contract(address=token_to_sold, abi=Router.abi_token)
        token_balance = token_sold.functions.balanceOf(address_wallet).call()
        allowance = check_allowance(private_key, token_to_sold, Router.sushi_router)
        if allowance < 10:
            approve(private_key, token_to_sold, Router.sushi_router, symbol)
            time.sleep(25)
        contract_txn = contract.functions.swapExactTokensForETH(
            token_balance,
            0,
            [token_to_sold, Router.eth],
            address_wallet,  # receiver
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': address_wallet,
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> Sold {symbol} Sushiswap| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> Sold {symbol} Sushiswap error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            swap_sushi_sold(private_key, token_to_sold, symbol, retry)


def sushi_swap(private_key, token_to_buy, token_to_sold, amount, symbol):
    swap_sushi_buy(private_key, token_to_buy, amount, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))
    swap_sushi_sold(private_key, token_to_buy, symbol)
    time.sleep(random.randint(time_delay_min, time_delay_max))


def approve(private_key, token_to_approve, address_to_approve, symbol, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    token_contract = web3.eth.contract(address=token_to_approve, abi=Router.abi_token)
    max_amount = web3.to_wei(2 ** 32 - 1, 'ether')
    try:
        tx = token_contract.functions.approve(address_to_approve, max_amount).build_transaction({
            'from': address_wallet,
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> {symbol} approve : https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}')
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> {symbol} approve error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            approve(private_key, token_to_approve, address_to_approve, symbol, retry)


def check_allowance(private_key, token_to_buy, router):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    token_contract = web3.eth.contract(address=token_to_buy, abi=Router.abi_token)
    allowance = Web3.from_wei(token_contract.functions.allowance(address_wallet, router).call(), 'ether')
    return allowance


def add_liquidity(private_key, token_to_buy, amount, symbol, router, retry=0):
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(private_key)
    address_wallet = account.address
    try:
        match router:
            case Router.arb_router:
                contract = web3.eth.contract(address=Router.arb_router, abi=Router.abi_arb)
            case Router.rpc_router:
                contract = web3.eth.contract(address=Router.rpc_router, abi=Router.abi_rpc)
            case Router.sushi_router:
                contract = web3.eth.contract(address=Router.sushi_router, abi=Router.abi_sushi)
        allowance = check_allowance(private_key, token_to_buy, router)
        if allowance < 10:
            approve(private_key, token_to_buy, router, symbol)
            time.sleep(25)
        amount_ = Web3.to_wei(amount, 'ether')
        contract_txn = contract.functions.addLiquidityETH(
            token_to_buy,
            amount_,
            0,
            0,
            address_wallet,
            (int(time.time()) + 10000)
        ).build_transaction({
            'from': address_wallet,
            'gasPrice': web3.eth.gas_price,
            'gas': gas,
            'value': amount_,
            'nonce': web3.eth.get_transaction_count(address_wallet)
        })
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Отправил транзакцию')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt.status == 1:
            print(f'Транзакция смайнилась успешно')
        else:
            raise ValueError("Транзакция сфейлилась, пытаюсь еще раз")
        lock.acquire()
        print(f'\n>>> add liquidity {symbol} | https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
    except Exception as error:
        lock.acquire()
        print(f'\n>>> add liquidity {symbol} error | {error}', flush=True)
        print(f'    {address_wallet}\n', flush=True)
        lock.release()
        retry += 1
        if retry > 10:
            return 0
        else:
            add_liquidity(private_key, token_to_buy, amount, symbol, router, retry)


swap_arr = (arb_swap, sushi_swap, rpc_swap, slingshot_swap)
addr_router_arr = [Router.arb_router, Router.sushi_router, Router.rpc_router]

if __name__ == '__main__':
    print('  _  __         _               _                                      _ _         ')
    print(' | |/ /___   __| | ___ _ __ ___| | ____ _ _   _  __ _   _____   ____ _| | | ____ _ ')
    print(" | ' // _ \ / _` |/ _ \ '__/ __| |/ / _` | | | |/ _` | / __\ \ / / _` | | |/ / _` |")
    print(r' | . \ (_) | (_| |  __/ |  \__ \   < (_| | |_| | (_| | \__ \\ V / (_| | |   < (_| |')
    print(' |_|\_\___/ \__,_|\___|_|  |___/_|\_\__,_|\__, |\__,_| |___/ \_/ \__,_|_|_|\_\__,_|')
    print('                                          |___/                                    ', '\n')
    print('https://t.me/developercode1')
    print('https://t.me/developercode1')
    print('https://t.me/developercode1\n')
    with open("private_keys.txt", "r") as f:
        keys_list = [row.strip() for row in f]

    def main():
        while keys_list:
            privatekey = keys_list.pop(0)
            lock.acquire()
            swaps = list(swap_arr)
            random.shuffle(swaps)
            lock.release()
            for router in swaps:
                rand = random.randint(0, 3)
                _amount1 = round(random.uniform(amount_min, amount_max), 8)
                router(privatekey, token_arr[rand]['address'], Router.eth, _amount1, token_arr[rand]['symbol'])
            rand = random.randint(0, 2)
            rand_ = random.randint(0, 1)
            swap_arb_buy(privatekey,  token_arr[rand_]['address'], liquidity_amount, token_arr[rand_]['symbol'])
            time.sleep(25)
            add_liquidity(privatekey, token_arr[rand_]['address'], liquidity_amount * 0.9, token_arr[rand_]['symbol'], addr_router_arr[rand])
    for _ in range(number_of_threads):
        threading.Thread(target=main).start()
