from typing import Literal
from helpers import RANKS, SUITS


class Card:
    def __init__(self, rank: str, suit: str):
        assert rank in RANKS
        assert suit in SUITS
        self.rank = rank
        self.suit = suit

    def is_rank(self, rank: str):
        assert rank in RANKS
        return self.rank == rank

    def is_rank_higher(self, rank: str):
        assert rank in RANKS
        return RANKS.index(rank) > RANKS.index(self.rank)

    def is_suit(self, suit: str):
        assert suit in SUITS
        return self.suit == suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, other):
        assert isinstance(other, Card)
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.rank}{self.suit}"
