import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import random
from typing import List
from functools import partial
import pickle
import re
import multiprocessing

from Card import Card
from Cards import Cards
from Deck import Deck

filename = 'counts.pickle'

deck = Deck()

def init_counts():
    combination_names = [combination_name for combination_name, _ in deck.combinations]
    cards_in_play_n_list = list(range(2,19))
    counts = pd.DataFrame(0, index=cards_in_play_n_list, columns=combination_names)
    counts.attrs = {"n": 0}
    return counts

def load_counts():
    with open(filename, 'rb') as f:
        df = pickle.load(f)
    return df

def save_counts(counts: pd.DataFrame):
    with open(filename, 'wb') as f:
        pickle.dump(counts, f)

def get_counts():
    try:
        return load_counts()
    except FileNotFoundError:
        return init_counts()

def get_counts_probabilities():
    df = load_counts()
    return df / df.attrs["n"]

def get_counts_probabilities_average():

    counts = get_counts()
    combs = [
        'is_high_card',
        'is_pair',
        'is_two_pair',
        'is_small_straight',
        'is_big_straight',
        'is_three',
        'is_full',
        'is_quad',
        'is_flush',
        'is_small_poker',
        'is_big_poker'
    ]

    df = pd.DataFrame()

    for comb in combs:
        matching_cols = [col for col in counts.columns if re.search(comb, col)]
        df[comb] = counts[matching_cols].mean(axis=1) / counts.attrs["n"]
    return df



def compute_counts(id):
    from os import getpid
    # print(id, getpid())

    deck = Deck()
    counts = init_counts()

    n = 600

    for _ in tqdm(range(n), desc=f"{getpid()}"):
        
        for cards_in_play_n in counts.index:
            
            cards_in_play = deck.sample(cards_in_play_n)
            
            for combination_name, func in cards_in_play.combinations[:]:
                counts.loc[cards_in_play_n, combination_name] += int(func())

            del cards_in_play

    counts.attrs["n"] += n

    return counts

def run():

    workers = multiprocessing.cpu_count() - 1

    while True:

        counts = get_counts()

        pool = multiprocessing.Pool(processes = workers)
        new_counts_list = pool.map(compute_counts, range(workers))

        for new_counts in new_counts_list:
            counts += new_counts
            counts.attrs["n"] += new_counts.attrs["n"]
            
        save_counts(counts)

if __name__ == "__main__":
    run()
