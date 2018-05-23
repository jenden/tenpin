"""Challenge: correctly score a game of ten pin bowling"""

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
        all_frames_complete = all([f.score() is not None for f in self.frames[:10]])
        if num_frames >= 10 and all_frames_complete:
            self.game_over = True

    def score(self):
        return [frame.score() for frame in self.frames[:10]]

    def final_score(self):
        return sum(self.score())
    
    def __repr__(self):
        return ''.join([str(f) for f in self.frames])


class Frame:
    
    def __init__(self, frame_number, last=None, next=None):
        self.number = frame_number
        self.rolls = []
        self.last = last
        self.next = next

    def bowl(self, roll):
        self.validate_bowl(roll)
        self.rolls.append(roll)

    def validate_bowl(self, roll):
        if not isinstance(roll, int):
            raise TypeError('The number of pins knocked down must be an integer')
        if roll < 0 or roll > 10 - sum(self.rolls):
            raise ValueError('Cannot knock down more than 10 or less than 0 pins')
        
    def complete(self):
        if sum(self.rolls) == 10 or len(self.rolls) == 2:
            return True
        else:
            return False

    def last_frame(self):
        return self.last
    
    def next_frame(self):
        if self.next:
            return self.next
        else:
            self.next = Frame(self.number + 1, self)
            return self.next

    def is_spare(self):
        if sum(self.rolls) == 10 and len(self.rolls) == 2: return True

    def is_strike(self):
        if sum(self.rolls) == 10 and len(self.rolls) == 1: return True

    def score(self):
        if not self.complete():
            return None
        if self.number > 10:
            return None

        score = sum(self.rolls)

        try:
            if self.is_spare():
                return score + self.next_frame().get_sum_of_next_n_rolls(1)
            elif self.is_strike():
                return score + self.next_frame().get_sum_of_next_n_rolls(2)
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
            padded_rolls = self.rolls + ['_']*(2-len(self.rolls))
            roll_string = '{} {}'.format(*padded_rolls)

        return return_string.format(self.number, roll_string, score_string)

        
