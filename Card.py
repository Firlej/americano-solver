import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import random
from typing import List
from functools import partial

from helpers import RANKS, SUITS

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def is_rank(self, rank):
        return self.rank == rank
    
    def is_rank_higher(self, rank):
        return RANKS.index(rank) > RANKS.index(self.rank)
    
    def is_suit(self, suit):
        return self.suit == suit
    
    def __str__(self):
        return f"Card({self.rank + self.suit})"
    
    def __repr__(self):
        return f"Card({self.rank + self.suit})"
    
if __name__ == "__main__":
    for (rank, suit) in itertools.product(RANKS, SUITS):
        print(Card(rank, suit))