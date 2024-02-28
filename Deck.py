import itertools
import random
from typing import List, Dict
from functools import partial
from math import comb

from Card import Card

from helpers import (
    RANKS,
    SUITS,
    SMALL_STRAIGHT_RANKS,
    BIG_STRAIGHT_RANKS,
    RANK_PAIRS,
    RANK_PAIRS_DESCENDING,
)


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
    
    # WAYS OF PICKING COMBINATIONS

    def total_ways(self, n):
        """
            Total ways of picking n cards from self.cards
        """
        return comb(len(self.cards), n)
    
    def ways_ranks_nums(self, n, rank_num_dict: Dict[str, int]):
        
        nums = [num for num in rank_num_dict.values()]
        
        assert min(nums) >= 0
        
        if n - sum(nums) < 0:
            return 0
        
        ways = 1
        
        for rank, num in rank_num_dict.items():
            rank_count = self.count_rank(rank)
            ways *= comb(rank_count, num)
            
        rank_counts_sum = sum([self.count_rank(rank) for rank in rank_num_dict.keys()])
        
        return ways * comb(len(self.cards) - rank_counts_sum, n - sum(nums))
    
    def ways_suit(self, n, suit, suit_num):
        if n - suit_num < 0:
            return 0
        suit_count = self.count_suit(suit)
        return comb(suit_count, suit_num) * comb(len(self.cards) - suit_count, n - suit_num)
    
    def ways_small_poker(self, n, suit, num):
        if n - num < 0:
            return 0
        poker_count = self.small_poker_count(suit)
        return comb(poker_count, num) * comb(len(self.cards) - poker_count, n - num)
    
    def ways_big_poker(self, n, suit, num):
        if n - num < 0:
            return 0
        poker_count = self.big_poker_count(suit)
        return comb(poker_count, num) * comb(len(self.cards) - poker_count, n - num)
    

    # COMBINATION HELPERS
            
    def __poker_count(self, ranks, suit):
        return sum([1 for card in self.cards if card.is_suit(suit) and card.rank in ranks])
            
    def small_poker_count(self, suit):    
        return self.__poker_count(SMALL_STRAIGHT_RANKS, suit)
            
    def big_poker_count(self, suit):   
        return self.__poker_count(BIG_STRAIGHT_RANKS, suit)
    
    def count_rank(self, rank):
        return sum(1 for card in self.cards if card.is_rank(rank))

    def count_suit(self, suit):
        return sum(1 for card in self.cards if card.is_suit(suit))
    
    def __get_card_ranks(self):
        return {card.rank for card in self.cards}
    
    # COMBINATION CHECKS

    def is_high_card(self, rank) -> bool:
        return self.count_rank(rank) >= 1

    def is_pair(self, rank):
        return self.count_rank(rank) >= 2

    def is_two_pair(self, rank_a, rank_b):
        return self.count_rank(rank_a) >= 2 and self.count_rank(rank_b) >= 2

    def is_small_straight(self):
        return SMALL_STRAIGHT_RANKS.issubset(self.__get_card_ranks())

    def is_big_straight(self):
        return BIG_STRAIGHT_RANKS.issubset(self.__get_card_ranks())

    def is_three(self, rank):
        return self.count_rank(rank) >= 3

    def is_full(self, rank_three, rank_pair):
        return self.count_rank(rank_three) >= 3 and self.count_rank(rank_pair) >= 2

    def is_quad(self, rank):
        return self.count_rank(rank) >= 4

    def is_flush(self, suit):
        return self.count_suit(suit) >= 5

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