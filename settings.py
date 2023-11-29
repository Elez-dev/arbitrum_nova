
RPC_NOVA = "https://nova.arbitrum.io/rpc"
RPC_ETH  = "https://rpc.ankr.com/eth"


class Telegram:
    TG_BOT_SEND = False            # Включить уведомления в тг или нет             [True or False]
    TG_TOKEN    = ''               # API токен тг-бота - создать его можно здесь - https://t.me/BotFather
    TG_ID       = 0                # id твоего телеграмма можно узнать тут       - https://t.me/getmyid_bot


SLINGSHOT = True
ARBSWAP   = True
RPCSWAP   = True
SUSHISWAP = True

remainder_eth  = 0                     # Сколько ETH оставлять на аккаунте (Нужно чтобы хватило на комсу при продаже токенов)
SLIPPAGE       = 5  # %

shuffle_wallets = True                 # Перемешивание кошельков

number_of_threads = 1                  # Количество потоков

time_delay_min = 50                    # Максимальная и
time_delay_max = 100                    # Минимальная задержка между ТРАНЗАКЦИЯМИ

TIME_DELAY_MIN = 5                     # Минимальное и
TIME_DELAY_MAX = 10                    # Максимальное время задержки между ПОТОКАМИ

TIME_DELAY_ACC_MIN = 100              # Минимальная и
TIME_DELAY_ACC_MAX = 200              # Максимальная задержка между АККАУНТАМИ

FLAG = True                           # Если свапалок включено несколько, но надо только какую то одну рандомную

RETRY_COUNT = 5                       # Кол-во повторений при ошибках

# Выбор суммы свапа и количества повторений -----------------------------------------------------------------------------------------------------------------------------------------------

prescale_swap_min = 0.001                   # Минимальный
prescale_swap_max = 0.002                   # Максимальный множитель свапа баланса -> Будет среднее (Берется вся сумма вашего баланса и умножается на данный множитель
                                            # 1 - Своп всего баланса, 0.5 - 50% от текущего баланса, 0.1 - 10% от текущего баланса

swap_decimal   = 8                         # Округление, количество знаов после запятой

total_number_of_repetitions_min = 1        # Минимальное и
total_number_of_repetitions_max = 1        # Максимальное количество повторений (Кругов) (Всех свапалок)

number_of_repetitions_min = 1              # Минимальное и
number_of_repetitions_max = 1              # Максимальное количество повторений для одной свапалки (Если включено несколько свапалок то
                                           #                                                        будет работать для каждой включеной!!!
                                           #                                                        Если включена только одна свапалка то этот параметр учитываться небудет)

# Liquidity ---------------------------------------------------------------------------------------------------------------------------------------------------------

liquiditi_sushi     = True                # Ликвидность SushiSwap     [True or False]
liquiditi_arb       = True                # Ликвидность ArbSwap       [True or False]
liquiditi_rpc       = True                # Ликвидность RPCswap       [True or False]

liquidity_prescale_min = 0.001            # Минимальное и
liquidity_prescale_max = 0.002            # Максимальное значение в токенах ETH -> Будет рандомное среднее

liquidity_decimal   = 8                   # Округление, количество знаов после запятой

# Official Bridge -------------------------------------------------------------------------------------------------------------------------------------------------------

prescale_bridge_min = 0.6                   # Минимальный
prescale_bridge_max = 0.4                   # Максимальный множитель бриджа баланса -> Будет среднее (Берется вся сумма вашего баланса и умножается на данный множитель)
                                            # 1 - Бридж всего баланса, 0.5 - 50% от текущего баланса, 0.1 - 10% от текущего баланса

bridge_decimal   = 5                         # Округление, количество знаов после запятой

# Mint NFT ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

number_nft_min = 1                          # Минимальное и
number_nft_max = 1                          # Максимальное количество нфт для минта

# Bridge NFT ---------------------------------------------------------------------------------------------------------------------------------------------

nft_random_chain = False                    # Рандомный выбор сети для бриджа из списка ниже True/False
chain_arr = ['avalanche', 'polygon', 'ethereum', 'bsc', 'arbitrum',
             'optimism', 'fantom', 'aptos', 'celo',
             'moonbeam', 'fuse', 'gnosis', 'klaytn', 'metis',
             'core', 'polygon_zkevm', 'canto', 'moonriver', 'tenet',
             'kava', 'meter', 'base', 'zora', 'scroll', 'zksync', 'linea', 'mantle']

nft_chain_to = 'polygon'                     # Ручной выбор, если nft_random_chain = False

# Get GAS ---------------------------------------------------------------------------------------------------------------------------------------------------------

gas_random_chain = False                    # Рандомный выбор сети для бриджа из списка ниже True/False
gas_chain_arr = ['avalanche', 'polygon', 'ethereum', 'bsc', 'arbitrum',
                 'optimism', 'fantom', 'aptos', 'moonbeam', 'fuse', 'klaytn', 'metis',
                 'moonriver', 'tenet', 'kava', 'meter', 'base', 'zksync', 'mantle']


gas_chain_to = 'moonbeam'                     # Ручной выбор, если gas_random_chain = False

value_from = 0.00000001  # Obtain from a certain amount of native token of the to_chain network
value_to   = 0.0000001   # Obtain up to a certain amount of native token of the to_chain network
value_decimal = 9
