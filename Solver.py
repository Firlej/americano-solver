import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import random
from typing import List, Dict
from functools import partial
import pickle
import math
from math import comb
import re
from collections import namedtuple

pd.set_option("display.max_rows", 83)
pd.set_option("display.max_columns", 83)


from helpers import (
    RANKS,
    SUITS,
    RANK_PAIRS,
    SMALL_STRAIGHT_RANKS,
    BIG_STRAIGHT_RANKS,
    TOTAL_CARDS_NUM,
    EACH_RANK_COUNT,
    EACH_SUIT_COUNT,
    RANK_PAIRS_DESCENDING,
)
from Card import Card

from Deck import Deck
from simulate import init_counts


class Solver:
    def __init__(
        self,
        hand: List[Card],
        cards_in_play_num: int
    ):
        assert cards_in_play_num >= len(hand)
        assert cards_in_play_num <= TOTAL_CARDS_NUM
        
        self.hand = Deck(hand)
        self.deck = Deck([card for card in Deck.get_all_cards() if card not in self.hand.cards])
        self.n = cards_in_play_num - len(hand)
    
    def __probabilty_n_ranks(self, rank_need_dict: Dict[str, int]):
        
        rank_need_real_dict = {
            rank: need - self.hand.count_rank(rank)
            for rank, need in rank_need_dict.items() if need - self.hand.count_rank(rank) > 0
        }
        
        if len(rank_need_real_dict) == 0:
            return 1
        
        need_real_sum = sum([need_real for need_real in rank_need_real_dict.values()])
        if need_real_sum > self.n:
            return 0
        
        ranks = rank_need_real_dict.keys()
        
        # Create a list of ranges for each key in the dictionary
        ranges = [range(need_real,  EACH_RANK_COUNT + 1) for need_real in rank_need_real_dict.values()]
        # Use itertools.product to generate all combinations of the ranges
        combinations = list(itertools.product(*ranges))
        # Create the resulting list of dictionaries
        rank_num_dict_list = [dict(zip(ranks, combo)) for combo in combinations]
    
        ways_positive = 0
        for rank_num_dict in rank_num_dict_list:
            ways_positive += self.deck.ways_ranks_nums(self.n, rank_num_dict)
        
        assert ways_positive > 0
        
        ways_total = self.deck.total_ways(self.n)
        
        return ways_positive / ways_total
    
    def probability_flush(self, suit):
        
        need = 5
        need_real = need - self.hand.count_suit(suit)
        
        if need_real <= 0:
            return 1
        
        if need_real > self.n:
            return 0
        
        
        ways_positive = 0
        for suit_num in range(need_real, EACH_SUIT_COUNT + 1):
            ways_positive += self.deck.ways_suit(self.n, suit, suit_num)
        
        assert ways_positive > 0
        
        ways_total = self.deck.total_ways(self.n)
        
        return ways_positive / ways_total
    
    def probability_small_poker(self, suit):
        
        need = 5
        need_real = need - self.hand.small_poker_count(suit)
        
        if need_real <= 0:
            return 1
        
        if need_real > self.n:
            return 0
        
        ways_positive = self.deck.ways_small_poker(self.n, suit, need_real)
        
        ways_total = self.deck.total_ways(self.n)
        
        return ways_positive / ways_total 
       
    def probability_big_poker(self, suit):
        
        need = 5
        need_real = need - self.hand.big_poker_count(suit)
        
        # print(need_real)
        
        if need_real <= 0:
            return 1
        
        if need_real > self.n:
            return 0
        
        ways_positive = self.deck.ways_big_poker(self.n, suit, need_real)
        
        ways_total = self.deck.total_ways(self.n)
        
        return ways_positive / ways_total
    
    def probability_high_card(self, rank):
        return self.__probabilty_n_ranks({
            rank: 1
        })
    
    def probability_pair(self, rank):
        return self.__probabilty_n_ranks({
            rank: 2
        })
    
    def probability_three(self, rank):
        return self.__probabilty_n_ranks({
            rank: 3
        })
    
    def probability_quad(self, rank):
        return self.__probabilty_n_ranks({
            rank: 4
        })
    
    def probability_two_pair(self, rank_a, rank_b):
        return self.__probabilty_n_ranks({
            rank_a: 2,
            rank_b: 2
        })
    
    def probability_full(self, rank_a, rank_b):
        return self.__probabilty_n_ranks({
            rank_a: 3,
            rank_b: 2
        })
    
    def probability_small_straight(self):
        return self.__probabilty_n_ranks({
            "9": 1,
            "T": 1,
            "J": 1,
            "Q": 1,
            "K": 1
        })
    
    def probability_big_straight(self):
        return self.__probabilty_n_ranks({
            "T": 1,
            "J": 1,
            "Q": 1,
            "K": 1,
            "A": 1
        })

Combination = namedtuple("Combination", ["name", "method", "kwargs"])

combinations = []
combinations.extend([Combination(f"high_card_{rank}", "probability_high_card", {"rank": rank}) for rank in RANKS])
combinations.extend([Combination(f"pair_{rank}", "probability_pair", {"rank": rank}) for rank in RANKS])
combinations.extend([Combination(f"two_pair_{a}_{b}", "probability_two_pair", {"rank_a": a, "rank_b": b}) for a, b in RANK_PAIRS_DESCENDING])
combinations.extend([Combination(f"small_straight", "probability_small_straight", {})])
combinations.extend([Combination(f"big_straight", "probability_big_straight", {})])
combinations.extend([Combination(f"three_{rank}", "probability_three", {"rank": rank}) for rank in RANKS])
combinations.extend([Combination(f"full_{a}_{b}", "probability_full", {"rank_a": a, "rank_b": b}) for a, b in RANK_PAIRS])
combinations.extend([Combination(f"quad_{rank}", "probability_quad", {"rank": rank}) for rank in RANKS])
combinations.extend([Combination(f"flush_{suit}", "probability_flush", {"suit": suit}) for suit in SUITS])
combinations.extend([Combination(f"small_poker_{suit}",  "probability_small_poker", {"suit": suit}) for suit in SUITS])
combinations.extend([Combination(f"big_poker_{suit}", "probability_big_poker", {"suit": suit}) for suit in SUITS])
