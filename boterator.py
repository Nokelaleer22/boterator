from functools import partial

from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line, print_help

from globals import get_db, get_telegram


@coroutine
def main():
    @coroutine
    def forward_message(message):
        yield bot.forward_message(message['chat']['id'], message['chat']['id'], message['message_id'])

    @coroutine
    def parce_command(message):
        yield bot.parce_command(message['chat']['id'], message['text'])

    @coroutine
    def new_chat(message):
        if message['new_chat_member']['id'] == bot.me['id']:
            msg = 'Hi there, @%s, thank you!' % message['from']['username']
            yield bot.send_message(message['chat']['id'], msg)
        else:
            return False

    @coroutine
    def left_chat(message):
        if message['left_chat_member']['id'] == bot.me['id']:
            yield bot.send_message(message['from']['id'], 'Whyyyy?! :\'(')
        else:
            return False

    bot = get_telegram()
    bot.add_handler(parce_command,'/start')
    bot.add_handler(parce_command,'/reg')
    bot.add_handler(forward_message)
    bot.add_handler(partial(print, 'Non-command message'))
    bot.add_handler(new_chat, msg_type=bot.MSG_NEW_CHAT_MEMBER)
    bot.add_handler(left_chat, msg_type=bot.MSG_LEFT_CHAT_MEMBER)
    yield bot.wait_commands()


if __name__ == '__main__':
    define('token', type=str, help='TelegramBot\'s token')
    define('db', type=str, help='DB connection DSN, e.g. "dbname=bot user=bot host=localhost port=5432"')

    parse_command_line()

    if not options.token:
        print_help()
        exit(1)

    ioloop = IOLoop.instance()

    ioloop.run_sync(main)