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

pd.set_option("display.max_rows", 83)
pd.set_option("display.max_columns", 83)

from helpers import RANKS, SUITS, RANK_PAIRS, SMALL_STRAIGHT_RANKS, BIG_STRAIGHT_RANKS, TOTAL_CARDS_NUM, NUM_EACH_RANK, NUM_EACH_SUIT, RANK_PAIRS_DESCENDING

from Card import Card
from Deck import Deck
from counts import init_counts

class DeckSolver(Deck):
    def __init__(self, cards_list: List[Card] = None):
        
        super().__init__(cards_list = cards_list)

        self.ranks_counts = {rank: 0 for rank in RANKS}
        for card in self.cards:
            self.ranks_counts[card.rank] += 1

        self.suits_counts = {rank: 0 for rank in SUITS}
        for card in self.cards:
            self.suits_counts[card.suit] += 1
            
    def __poker_count(self, ranks, suit):
        return sum([1 for card in self.cards if card.is_suit(suit) and card.rank in ranks])
            
    def small_poker_count(self, suit):
        small_poker_ranks = ["9", "T", "J", "Q", "K"]        
        return self.__poker_count(small_poker_ranks, suit)
            
    def big_poker_count(self, suit):
        small_poker_ranks = ["T", "J", "Q", "K", "A"]        
        return self.__poker_count(small_poker_ranks, suit)

    def total_ways(self, n):
        return comb(len(self.cards), n)
    
    def ways_ranks_nums(self, n, rank_num_dict: Dict[str, int]):
        
        nums = [num for num in rank_num_dict.values()]
        
        assert min(nums) >= 0
        
        if n - sum(nums) < 0:
            return 0
        
        ways = 1
        
        for rank, num in rank_num_dict.items():
            rank_count = self.ranks_counts[rank]
            ways *= comb(rank_count, num)
            
        rank_counts_sum = sum([self.ranks_counts[rank] for rank in rank_num_dict.keys()])
        
        return ways * comb(len(self.cards) - rank_counts_sum, n - sum(nums))
    
    def ways_suit(self, n, suit, suit_num):
        if n - suit_num < 0:
            return 0
        suit_count = self.suits_counts[suit]
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


class Solver:
    def __init__(
        self,
        hand: List[Card],
        unknown_cards_in_play_num: int
    ):
        assert unknown_cards_in_play_num >= 0
        
        assert unknown_cards_in_play_num <= 24 - len(hand)
        
        self.hand = DeckSolver(hand)
        self.deck = DeckSolver([card for card in Deck.get_all_cards() if card not in self.hand.cards])
        self.unknown_cards_in_play_num = unknown_cards_in_play_num
    
    def __probabilty_n_ranks(self, rank_need_dict: Dict[str, int]):
        
        rank_need_real_dict = {
            rank: need - self.hand.ranks_counts[rank] 
            for rank, need in rank_need_dict.items() if need - self.hand.ranks_counts[rank] > 0
        }
        
        if len(rank_need_real_dict) == 0:
            return 1
    
        n = self.unknown_cards_in_play_num
        
        need_real_sum = sum([need_real for need_real in rank_need_real_dict.values()])
        if need_real_sum > n:
            return 0
        
        ranks = rank_need_real_dict.keys()
        
        # Create a list of ranges for each key in the dictionary
        ranges = [range(need_real,  NUM_EACH_RANK + 1) for need_real in rank_need_real_dict.values()]
        # Use itertools.product to generate all combinations of the ranges
        combinations = list(itertools.product(*ranges))
        # Create the resulting list of dictionaries
        rank_num_dict_list = [dict(zip(ranks, combo)) for combo in combinations]
    
        ways_positive = 0
        for rank_num_dict in rank_num_dict_list:
            ways_positive += self.deck.ways_ranks_nums(n, rank_num_dict)
        
        assert ways_positive > 0
        
        ways_total = self.deck.total_ways(n)
        
        return ways_positive / ways_total
    
    def probability_flush(self, suit):
        
        need = 5
        need_real = need - self.hand.suits_counts[suit]
        
        if need_real <= 0:
            return 1
        
        n = self.unknown_cards_in_play_num
        
        if need_real > n:
            return 0
        
        
        ways_positive = 0
        for suit_num in range(need_real, NUM_EACH_SUIT + 1):
            ways_positive += self.deck.ways_suit(n, suit, suit_num)
        
        assert ways_positive > 0
        
        ways_total = self.deck.total_ways(n)
        
        return ways_positive / ways_total
    
    def probability_small_poker(self, suit):
        
        need = 5
        need_real = need - self.hand.small_poker_count(suit)
        
        if need_real <= 0:
            return 1
        
        n = self.unknown_cards_in_play_num
        
        if need_real > n:
            return 0
        
        ways_positive = self.deck.ways_small_poker(n, suit, need_real)
        
        ways_total = self.deck.total_ways(n)
        
        return ways_positive / ways_total 
       
    def probability_big_poker(self, suit):
        
        need = 5
        need_real = need - self.hand.big_poker_count(suit)
        
        # print(need_real)
        
        if need_real <= 0:
            return 1
        
        n = self.unknown_cards_in_play_num
        
        if need_real > n:
            return 0
        
        ways_positive = self.deck.ways_big_poker(n, suit, need_real)
        
        ways_total = self.deck.total_ways(n)
        
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
        