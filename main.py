# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, Update

from game import Game
import settings

game = Game()
rating_dict = {}


def command_start(update, context: CallbackContext):
    game.start()
    update.message.reply_text('Игра Крокодил началась', reply_to_message_id=True)


def set_master(update, context):
    username = update.message.from_user.full_name
    game.set_master(update.message.from_user.id)
    update.message.reply_text('Ведущий {}'.format(username), reply_to_message_id=True)


def command_master(update: Update, context):
    if game.is_game_started():
        set_master(update, context)


def command_show_word(update, context):
    user_id = update.message.from_user.id
    word = game.get_word(user_id)
    update.message.reply_text(word, reply_to_message_id=True)


def command_change_word(update, context):
    user_id = update.message.from_user.id
    word = game.change_word(user_id)
    update.message.reply_text(word, reply_to_message_id=True)


def command_rating(update, context):
    rating_str = ''
    for elem in rating_dict:
        rating_str += elem.split()[1] + ": " + str(rating_dict[elem]) + " "

    update.message.reply_text(rating_str, reply_to_message_id=True)


def is_word_answered(update, context):
    user_id = update.message.from_user.id
    text = update.message.text
    if game.is_word_answered(user_id, text):
        user_id = update.message.from_user.id
        username = update.message.from_user.full_name

        if str(user_id) + ' ' + username in rating_dict:
            rating_dict[str(user_id) + ' ' + username] += 1
        else:
            rating_dict[str(user_id) + ' ' + username] = 1

        word = game.get_current_word()
        update.message.reply_text('Слово {} отгадал игрок {}'.format(word, username), reply_to_message_id=True)

        set_master(update, context)


def main():
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
