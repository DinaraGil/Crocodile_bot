# -*- coding: utf-8 -*-
import random
import settings


class Game:
    def __init__(self):
        self._master_user_id = 0
        self._word_list = []
        self._current_word = ''

    def start(self):
        self._word_list = settings.word_list.copy()
        self._current_word = self._create_word()
        self._master_user_id = 0

    def set_master(self, user_id):
        self._master_user_id = user_id

    def is_master(self, user_id: int):
        return user_id == self._master_user_id

    def _create_word(self):
        word = random.choice(self._word_list)
        del self._word_list[self._word_list.index(word)]
        return word

    def get_word(self, user_id: int):
        if self.is_master(user_id):
            return self._current_word
        else:
            return ''

    def change_word(self, user_id: int):
        if self.is_master(user_id):
            self._current_word = self._create_word()
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


