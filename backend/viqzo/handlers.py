from logging import Handler, LogRecord

import telebot


class TelegramBotHandler(Handler):
    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self.token = token
        self.chat_id = chat_id
        self.msg_limit = 4056  # настоящий лимит 4096

    def emit(self, record: LogRecord):
        bot = telebot.TeleBot(self.token)
        record_len = len(self.format(record))

        if record_len >= self.msg_limit:
            messages_amount = record_len // self.msg_limit + 1

            for numb in range(0, messages_amount):
                format_message = self.format(
                    record)[numb * self.msg_limit: (numb + 1) * self.msg_limit]

                bot.send_message(
                    self.chat_id,
                    f'{numb + 1}/{messages_amount}\n' + format_message
                )
        else:
            bot.send_message(
                self.chat_id,
                self.format(record)
            )
