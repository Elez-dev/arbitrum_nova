from web3.exceptions import TransactionNotFound
from modules.tg_bot import TgBot
from settings import RETRY_COUNT
import time


def exception_handler(lable):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for _ in range(RETRY_COUNT):
                try:
                    return func(self, *args, **kwargs)
                except TransactionNotFound:
                    self.log.info('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, lable, self.address_wallet,
                                                 'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                    time.sleep(30)
                except ConnectionError:
                    self.log.info('Ошибка подключения к интернету или проблемы с РПЦ')
                    if TgBot.TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, lable, self.address_wallet,
                                                 'Ошибка подключения к интернету или проблемы с РПЦ')
                    time.sleep(30)
                except Exception as error:
                    if isinstance(error.args[0], dict):
                        if 'nsufficient' in error.args[0]['message']:
                            self.log.info('Ошибка, скорее всего нехватает комсы')
                            if TgBot.TG_BOT_SEND is True:
                                TgBot.send_message_error(self, self.number, lable, self.address_wallet,
                                                         'Ошибка, скорее всего нехватает комсы')
                            return 'balance'
                        else:
                            self.log.info(error)
                            time.sleep(30)
                    else:
                        self.log.info(error)
                        time.sleep(30)
        return wrapper
    return decorator
