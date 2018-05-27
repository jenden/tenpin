"""Challenge: correctly score a game of ten pin bowling"""

# game constants
FRAMES_PER_GAME = 10
PINS_PER_FRAME = 10
ROLLS_PER_FRAME = 2
SPARE_BONUS_ROLLS = 1
STRIKE_BONUS_ROLLS = 2


class Game:

    def __init__(self, rolls=None):
        self.new_game()
        if rolls:
            for roll in rolls:
                self.bowl(roll)

    def new_game(self):
        self.frames = [Frame(1)]
        self.game_over = False

    def bowl(self, roll):
        if self.game_over:
            return self

        current_frame = self.frames[-1]
        if current_frame.complete():
            self.frames.append(current_frame.next_frame())
            current_frame = self.frames[-1]
        current_frame.bowl(roll)

        self.check_game_over()
        return self
    
    def check_game_over(self):
        # complete iff ten frames have scores
        num_frames = len(self.frames)
        all_frames_complete = all([f.score() is not None for f in self.frames[:FRAMES_PER_GAME]])
        if num_frames >= FRAMES_PER_GAME and all_frames_complete:
            self.game_over = True

    def final_score(self):
        frame_scores = [frame.score() for frame in self.frames[:FRAMES_PER_GAME]]
        return sum(frame_scores)
    
    def __repr__(self):
        return ''.join([str(f) for f in self.frames])


class Frame:
    
    def __init__(self, frame_number, last_frame=None, next_frame=None):
        self.frame_number = frame_number
        self.rolls = []
        self.last = last_frame
        self.next = next_frame

    def bowl(self, roll):
        self.validate_bowl(roll)
        self.rolls.append(roll)

    def validate_bowl(self, roll):
        if not isinstance(roll, int):
            raise TypeError('The number of pins knocked down must be an integer')
        if roll < 0 or roll > PINS_PER_FRAME - sum(self.rolls):
            raise ValueError('Cannot knock down more than 10 or less than 0 pins')
        
    def complete(self):
        if sum(self.rolls) == PINS_PER_FRAME or len(self.rolls) == ROLLS_PER_FRAME:
            return True
        else:
            return False

    def last_frame(self):
        return self.last
    
    def next_frame(self):
        if self.next:
            return self.next
        else:
            self.next = Frame(self.frame_number + 1, self)
            return self.next

    def is_spare(self):
        if sum(self.rolls) == PINS_PER_FRAME and len(self.rolls) == ROLLS_PER_FRAME: return True

    def is_strike(self):
        if sum(self.rolls) == PINS_PER_FRAME and len(self.rolls) == 1: return True

    def score(self):
        if not self.complete():
            return None
        if self.frame_number > FRAMES_PER_GAME:
            return None

        score = sum(self.rolls)

        try:
            if self.is_spare():
                return score + self.next_frame().get_sum_of_next_n_rolls(SPARE_BONUS_ROLLS)
            elif self.is_strike():
                return score + self.next_frame().get_sum_of_next_n_rolls(STRIKE_BONUS_ROLLS)
        except TypeError:
            return None
        
        return score
        
    def get_sum_of_next_n_rolls(self, n):
        # return sum of next rolls or None if not complete
        available_rolls = len(self.rolls)
        if available_rolls >= n:
            return sum(self.rolls[:n])
        if self.complete() and len(self.rolls) < n:
            remaining_rolls = n - available_rolls
            return sum(self.rolls) + self.next_frame().get_sum_of_next_n_rolls(available_rolls)
            
    
    def __repr__(self):
        return_string = '\n{0:>2}: [{1}] {2}'
        score = self.score()
        score_string = '-> {}'.format(score) if score is not None else ''
        if self.is_strike():
            roll_string = '  X'
        elif self.is_spare():
            roll_string = '{} /'.format(self.rolls[0])
        else:
            padded_rolls = self.rolls + ['_']*(ROLLS_PER_FRAME - len(self.rolls))
            roll_string = '{} {}'.format(*padded_rolls)

        return return_string.format(self.frame_number, roll_string, score_string)

        
