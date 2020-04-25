from unittest import TestCase

from game import Game


class TestGame(TestCase):
    def test_not_master(self):
        game = Game()
        game.start()
        game.set_master(1)
        word = game.get_word(2)
        self.assertEqual('', word)

    def test_master(self):
        game = Game()
        game.start()
        game.set_master(1)
        word = game.get_word(1)
        self.assertEqual(game._current_word, word)

    def test_answered(self):
        game = Game()
        game.start()
        game.set_master(1)
        is_answered = game.is_word_answered(2, game._current_word)
        self.assertTrue(is_answered)

    def test_not_answered(self):
        game = Game()
        game.start()
        game.set_master(1)
        is_answered = game.is_word_answered(2, " ")
        self.assertFalse(is_answered)
