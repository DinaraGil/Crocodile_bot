# -*- coding: utf-8 -*-
import random
import settings


class User:
    def __init__(self, user_id, username):
        self.user_id: int = user_id
        self.username: str = username
        self.rating = 0

    def update_rating(self):
        self.rating += 1

    def get_rating_str(self):
        return self.username + ": " + str(self.rating) + " "


class Game:
    def __init__(self):
        self._master_user_id = 0
        self._word_list = []
        self._current_word = ''
        self._game_started = False
        self._users = {}

    def start(self):
        self._word_list = settings.word_list.copy()
        self._master_user_id = 0
        self._game_started = True
        self._users = {}

    def is_game_started(self):
        return self._game_started

    def set_master(self, user_id):
        self._create_word()
        self._master_user_id = user_id

    def is_master(self, user_id: int):
        return user_id == self._master_user_id

    def _create_word(self):
        self._current_word = random.choice(self._word_list)
        del self._word_list[self._word_list.index(self._current_word)]

    def get_word(self, user_id: int):
        if self.is_master(user_id):
            return self._current_word
        else:
            return ''

    def change_word(self, user_id: int):
        if self.is_master(user_id):
            self._create_word()
            return self._current_word
        else:
            return ''

    def is_word_answered(self, user_id, text):
        if not self.is_master(user_id):
            self._master_user_id = user_id
            return text.lower() == self._current_word.lower()
        return False

    def get_current_word(self):
        return self._current_word

    def update_rating(self, user_id, username):
        if user_id not in self._users:
            self._users[user_id] = User(user_id, username)

        self._users[user_id].update_rating()

    def get_str_rating(self):
        rating_str = ''
        for user_id in self._users:
            rating_str += self._users[user_id].get_rating_str()

        return rating_str
