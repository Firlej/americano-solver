import random
import itertools

from Card import Card
from Cards import Cards

from helpers import RANKS, SUITS

class Deck(Cards):

    def __init__(self):
        cards_list = [Card(rank, suit) for (rank, suit) in itertools.product(RANKS, SUITS)]
        super().__init__(cards = cards_list)

        pass

    def sample(self, n) -> Cards:
        return Cards(random.sample(self.cards, n))
    
    # STR & REPR

    def __str__(self):
        return f"Deck({str(self.cards)})"
    
    def __repr__(self):
        return f"Deck({str(self.cards)})"

if __name__ == "__main__":
    deck = Deck()
    print(deck)
    print(deck.sample(5))





