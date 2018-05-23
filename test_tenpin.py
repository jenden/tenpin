import unittest

from tenpin import Game, Frame


class TestFrame(unittest.TestCase):

    def test_frame_is_complete(self):
        f1 = Frame(1)
        self.assertFalse(f1.complete())
        f1.roll(6)
        self.assertFalse(f1.complete())
        f1.roll(2)
        self.assertTrue(f1.complete())
        
        f2 = Frame(2)
        f2.roll(10)
        self.assertTrue(f2.complete())
    
    def test_frame_recognizes_spare(self):
        f1 = Frame(1)
        f1.roll(8)
        self.assertFalse(f1.is_spare())
        f1.roll(2)
        self.assertTrue(f1.is_spare())

        f2 = Frame(2)
        f2.roll(10)
        self.assertFalse(f2.is_spare())


    def test_frame_recognizes_strike(self):
        f1 = Frame(1)
        f1.roll(10)
        self.assertTrue(f1.is_strike())
        self.assertFalse(f1.is_spare())

        f2 = Frame(2)
        self.assertFalse(f2.is_strike())
        f2.roll(8)
        f2.roll(2)
        self.assertFalse(f2.is_strike())



if __name__ == '__main__':
    unittest.main()
