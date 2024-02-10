import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import random
from typing import List
from functools import partial
import pickle

from Card import Card
from Cards import Cards
from Deck import Deck



filename = 'counts.pickle'

deck = Deck()

def init_counts():
    combination_names = [combination_name for combination_name, _ in deck.combinations]
    cards_in_play_n_list = list(range(2,19))
    counts = pd.DataFrame(0, index=combination_names, columns=cards_in_play_n_list)
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


def run():

    counts = get_counts()

    n = 600

    while True:

        for _ in tqdm(range(n)):

            time.sleep(0.1)
            
            for cards_in_play_n in counts.columns:
                
                cards_in_play = deck.sample(cards_in_play_n)
                
                for combination_name, func in cards_in_play.combinations[:]:
                    counts.loc[combination_name, cards_in_play_n] += int(func())

        counts.attrs["n"] += n
        
        save_counts(counts)

if __name__ == "__main__":
    run()

