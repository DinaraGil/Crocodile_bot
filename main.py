# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, Update

from game import Game
import settings

game = Game()


def start(update, context: CallbackContext):
    game.start()
    update.message.reply_text('Игра Крокодил началась', reply_to_message_id=True)


def master(update: Update, context):
    username = update.message.from_user.full_name
    print('master =' + str(update))
    game.set_master(update.message.from_user.id)
    update.message.reply_text('Ведущий {}'.format(username), reply_to_message_id=True)


def show_word(update, context):
    user_id = update.message.from_user.id
    word = game.get_word(user_id)
    update.message.reply_text(word, reply_to_message_id=True)


def change_word(update, context):
    user_id = update.message.from_user.id
    word = game.change_word(user_id)
    update.message.reply_text(word, reply_to_message_id=True)


def is_word_answered(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    if game.is_word_answered(user_id, text):
        username = update.message.from_user.full_name
        word = game.get_current_word()
        update.message.reply_text('Слово {} отгадал игрок {}'.format(word, username), reply_to_message_id=True)


def main():
    updater = Updater(settings.TOKEN, use_context=True, request_kwargs=settings.REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("master", master))
    dp.add_handler(CommandHandler("show_word", show_word))
    dp.add_handler(CommandHandler("change_word", change_word))

    dp.add_handler(MessageHandler(Filters.text, is_word_answered))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
