import unittest

from tenpin import Game, Frame


class TestGame(unittest.TestCase):

    def test_game_ends_after_tenth_frame_completed(self):
        rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
        g = Game()
        for roll in rolls:
            self.assertFalse(g.game_over)
            g.bowl(roll)
        self.assertTrue(g.game_over)
        final_score = g.final_score()
        g.bowl(10)
        self.assertEqual(final_score, g.final_score())

    def test_game_scores_valid_sequence_correctly(self):
        rolls = [10, 7, 3, 9, 0, 10, 0, 8, 8, 2, 0, 6, 10, 10, 10, 8, 1]
        expected_score = 167
        g = Game(rolls)
        print(g)
        actual_score = g.final_score()
        self.assertEqual(actual_score, expected_score)

    def test_game_raises_error_for_invalid_sequence(self):
        rolls = [10, 7, 4]
        with self.assertRaises(ValueError):
            g = Game(rolls)
            print(g)

    def test_perfect_game(self):
        g = Game()
        for _ in range(12):
            self.assertFalse(g.game_over)
            g.bowl(10)
        self.assertTrue(g.game_over)
        expected_score = 300
        actual_score = g.final_score()
        self.assertEqual(actual_score, expected_score)


class TestFrame(unittest.TestCase):

    def test_frame_is_complete(self):
        f1 = Frame(1)
        self.assertFalse(f1.complete())
        f1.bowl(6)
        self.assertFalse(f1.complete())
        f1.bowl(2)
        self.assertTrue(f1.complete())
        
        f2 = Frame(2)
        f2.bowl(10)
        self.assertTrue(f2.complete())
    
    def test_frame_recognizes_spare(self):
        f1 = Frame(1)
        f1.bowl(8)
        self.assertFalse(f1.is_spare())
        f1.bowl(2)
        self.assertTrue(f1.is_spare())

        f2 = Frame(2)
        f2.bowl(10)
        self.assertFalse(f2.is_spare())


    def test_frame_recognizes_strike(self):
        f1 = Frame(1)
        f1.bowl(10)
        self.assertTrue(f1.is_strike())
        self.assertFalse(f1.is_spare())

        f2 = Frame(2)
        self.assertFalse(f2.is_strike())
        f2.bowl(8)
        f2.bowl(2)
        self.assertFalse(f2.is_strike())

    def test_frame_accepts_only_valid_rolls(self):
        f1 = Frame(1)
        with self.assertRaises(TypeError):
            f1.bowl(1.2)
        with self.assertRaises(ValueError):
            f1.bowl(-2)
        with self.assertRaises(ValueError):
            f1.bowl(11)
        f1.bowl(4)
        with self.assertRaises(ValueError):
            f1.bowl(7)
            

if __name__ == '__main__':
    unittest.main()
