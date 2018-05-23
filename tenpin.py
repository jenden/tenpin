


class Game:

    def __init__(self, rolls=None):

        self.new_game()
        
        if rolls:
            for roll in rolls:
                self.bowl(roll)

    def new_game(self):
        self.frames = [Frame(1)]

    def bowl(self, pins):
     
        current_frame = self.frames[-1]
        if current_frame.complete():
            self.frames.append(current_frame.next_frame())
            current_frame = self.frames[-1]
        current_frame.roll(pins)

        return self
    
    def score(self):
        return [frame.score() for frame in self.frames]

    def __repr__(self):
        return str(self.frames)


    

class Frame:
    
    def __init__(self, frame_number, last=None, next=None):
        self.number = frame_number
        self.rolls = []
        self.last = last
        self.next = next

    def roll(self, pins):
        self.validate_roll(pins)
        self.rolls.append(pins)

    def validate_roll(self, pins):
        if not isinstance(pins, int):
            raise TypeError('The number of pins knocked down must be an integer')
        if pins < 0 or pins > 10 - sum(self.rolls):
            raise ValueError('Cannot knock down more than 10 or less than 0 pins')
        
    def complete(self):
        # frame is complete iff
        # - score is equal to 10
        # - two rolls

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

        score = sum(self.rolls)

        try:
            if self.is_spare():
                return score + self.next_frame().get_sum_of_n_next_rolls(1)
            elif self.is_strike():
                return score + self.next_frame().get_sum_of_n_next_rolls(2)
        except TypeError:
            return None
        
        return score
        
    def get_sum_of_n_next_rolls(self, n):
        # return sum of next rolls or None if not complete
        available_rolls = len(self.rolls)
        if available_rolls >= n:
            return sum(self.rolls[:n])
        if self.complete() and len(self.rolls) < n:
            remaining_rolls = n - available_rolls
            return sum(self.rolls) + self.next_frame().get_sum_of_n_next_rolls(available_rolls)
            
    
    def __repr__(self):
        return_string = 'Frame {}: '.format(self.number)
        if self.is_strike():
            return return_string + '[  X]'
        if self.is_spare():
            return return_string + '[{} /]'.format(self.rolls[0])

        rolls = self.rolls + ['_']*(2-len(self.rolls))
        return return_string + '[{} {}]'.format(*rolls)
