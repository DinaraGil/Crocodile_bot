# -*- coding: utf-8 -*-
import logging

from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, Update

from game import Game
import settings

game = Game()
rating_dict = {}

logger = None


def setup_logger():
    global logger
    file_handler = logging.FileHandler('crocodile.log', 'w', 'utf-8')
    stream_handler = logging.StreamHandler()
    logger = logging.getLogger("main_log")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def command_start(update, context: CallbackContext):
    logger.info('Got command /start,'
                'chatId={},'
                'text="{}"'.format(update.message.chat.id,
                                   update.message.text))
    game.start()
    update.message.reply_text('Игра Крокодил началась', reply_to_message_id=True)


def set_master(update, context):
    username = update.message.from_user.full_name
    game.set_master(update.message.from_user.id)
    logger.info('New master is "{}"({})'.format(update.message.from_user.full_name,
                                                update.message.from_user.id))

    update.message.reply_text('Ведущий {}'.format(username), reply_to_message_id=True)


def command_master(update: Update, context):
    logger.info('Got command /master,'
                'chatId={},'
                'text="{}",'
                'user="{}"({})'.format(update.message.chat.id,
                                       update.message.text,
                                       update.message.from_user.full_name,
                                       update.message.from_user.id))

    if game.is_game_started():
        set_master(update, context)


def command_show_word(update, context):
    user_id = update.message.from_user.id
    word = game.get_word(user_id)

    logger.info('Got command /show_word, ' 
                'chatId={}, '
                'user="{}"({}),'
                'is_user_master={},'
                'word={}'.format(update.message.chat.id,
                                 update.message.from_user.full_name,
                                 update.message.from_user.id,
                                 game.is_master(user_id),
                                 word))

    update.message.reply_text(word, reply_to_message_id=True)


def command_change_word(update, context):
    user_id = update.message.from_user.id
    word = game.change_word(user_id)

    logger.info('Got command /change_word,'
                'chatId={},'
                'user="{}"({}),'
                'is_user_master={},'
                'word={}'.format(update.message.chat.id,
                                 update.message.from_user.full_name,
                                 update.message.from_user.id,
                                 game.is_master(user_id),
                                 word))

    update.message.reply_text(word, reply_to_message_id=True)


def command_rating(update, context):
    rating_str = ''
    for elem in rating_dict:
        rating_str += elem.split()[1] + ": " + str(rating_dict[elem]) + " "

    logger.info('Got command /rating,'
                'chatId={},'
                'rating={}'.format(update.message.chat.id,
                                   rating_str))

    update.message.reply_text(rating_str, reply_to_message_id=True)


def is_word_answered(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    word = game.get_current_word()

    if game.is_word_answered(user_id, text):
        user_id = update.message.from_user.id
        username = update.message.from_user.full_name

        if str(user_id) + ' ' + username in rating_dict:
            rating_dict[str(user_id) + ' ' + username] += 1
        else:
            rating_dict[str(user_id) + ' ' + username] = 1

        update.message.reply_text('Слово {} отгадал игрок {}'.format(word, username), reply_to_message_id=True)

        set_master(update, context)

    logger.info('Guessing word,'
                'chadId={},'
                'user="{}"({}),'
                'is_master={},'
                'text="{}",'
                'word="{}"'.format(update.message.chat.id,
                                   update.message.from_user.full_name,
                                   update.message.from_user.id,
                                   game.is_master(user_id),
                                   text,
                                   word))


def main():
    setup_logger()

    updater = Updater(settings.TOKEN, use_context=True, request_kwargs=settings.REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("master", command_master))
    dp.add_handler(CommandHandler("show_word", command_show_word))
    dp.add_handler(CommandHandler("change_word", command_change_word))
    dp.add_handler(CommandHandler("rating", command_rating))

    dp.add_handler(MessageHandler(Filters.text, is_word_answered))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
