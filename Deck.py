import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import random
from typing import List
from functools import partial

from Card import Card

from helpers import RANKS, SUITS, SMALL_STRAIGHT_RANKS, BIG_STRAIGHT_RANKS, RANK_PAIRS, RANK_PAIRS_DESCENDING


class Deck:
    def __init__(self, cards_list: List[Card] = None):
        
        if cards_list is None:
            self.cards = self.get_all_cards()
        else:
            self.cards = cards_list

        self.combinations = []
        self.combinations.extend([(f'is_high_card_{rank}', partial(self.is_high_card, rank=rank)) for rank in RANKS])
        self.combinations.extend([(f'is_pair_{rank}', partial(self.is_pair, rank=rank)) for rank in RANKS])
        self.combinations.extend([(f'is_two_pair_{a}_{b}', partial(self.is_two_pair, rank_a = a, rank_b = b)) for (a, b) in RANK_PAIRS_DESCENDING])
        self.combinations.extend([(f'is_small_straight', partial(self.is_small_straight))])
        self.combinations.extend([(f'is_big_straight', partial(self.is_big_straight))])
        self.combinations.extend([(f'is_three_{rank}', partial(self.is_three, rank=rank)) for rank in RANKS])
        self.combinations.extend([(f'is_full_{a}_{b}', partial(self.is_full, rank_three = a, rank_pair = b)) for (a, b) in RANK_PAIRS])
        self.combinations.extend([(f'is_quad_{rank}', partial(self.is_quad, rank=rank)) for rank in RANKS])
        self.combinations.extend([(f'is_flush_{suit}', partial(self.is_flush, suit=suit)) for suit in SUITS])
        self.combinations.extend([(f'is_small_poker_{suit}', partial(self.is_small_poker, suit=suit)) for suit in SUITS])
        self.combinations.extend([(f'is_big_poker_{suit}', partial(self.is_big_poker, suit=suit)) for suit in SUITS])

    @staticmethod
    def get_all_cards():
        return [Card(rank, suit) for (rank, suit) in itertools.product(RANKS, SUITS)]
    
    @staticmethod
    def from_hands(hands: List[List[Card]]):

        def flatten_comprehension(matrix):
            return [item for row in matrix for item in row]
        
        return Deck(cards_list = flatten_comprehension(hands))
    
    def get_hands(self, cards_per_hands: List[int]) -> List[List[Card]]:
        
        deck = self.cards
        random.shuffle(deck)

        assert sum(cards_per_hands) <= len(deck), "Not enough cards in deck!"

        hands = []
        for cards_per_hand in cards_per_hands:
            hands.append(deck[:cards_per_hand]) 
            deck = deck[cards_per_hand:]

        hands_chain = list(itertools.chain(*hands))
        assert len(hands_chain) == len(set(hands_chain)), "Duplicate cards in hand!"

        return hands
    
    def sample(self, n):
        return Deck(random.sample(self.cards, n))
    

    # COMBINATION HELPERS
    def __count_rank(self, rank):
        return sum(1 for card in self.cards if card.is_rank(rank))

    def __count_suit(self, suit):
        return sum(1 for card in self.cards if card.is_suit(suit))
    
    def __get_card_ranks(self):
            return {card.rank for card in self.cards}
    
    # COMBINATION CHECKS

    def is_high_card(self, rank) -> bool:
        return self.__count_rank(rank) >= 1

    def is_pair(self, rank):
        return self.__count_rank(rank) >= 2

    def is_two_pair(self, rank_a, rank_b):
        return self.__count_rank(rank_a) >= 2 and self.__count_rank(rank_b) >= 2

    def is_small_straight(self):
        return SMALL_STRAIGHT_RANKS.issubset(self.__get_card_ranks())

    def is_big_straight(self):
        return BIG_STRAIGHT_RANKS.issubset(self.__get_card_ranks())

    def is_three(self, rank):
        return self.__count_rank(rank) >= 3

    def is_full(self, rank_three, rank_pair):
        return self.__count_rank(rank_three) >= 3 and self.__count_rank(rank_pair) >= 2

    def is_quad(self, rank):
        return self.__count_rank(rank) >= 4

    def is_flush(self, suit):
        return self.__count_suit(suit) >= 5

    def is_small_poker(self, suit):
        return len([
            card for card in self.cards if 
                card.rank in SMALL_STRAIGHT_RANKS and
                card.is_suit(suit) 
        ]) == 5

    def is_big_poker(self, suit):
        return len([
            card for card in self.cards if 
                card.rank in BIG_STRAIGHT_RANKS and
                card.is_suit(suit)
        ]) == 5
    
    # STR & REPR

    def __str__(self):
        return f"Deck({str(self.cards)})"
    
    def __repr__(self):
        return f"Deck({str(self.cards)})"


if __name__ == "__main__":
    cards_list = [Card(rank, suit) for (rank, suit) in itertools.product(RANKS, SUITS)]
    cards = Deck(cards_list)
    print(cards)