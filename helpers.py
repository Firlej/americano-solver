import itertools

RANKS = ["9", "T", "J", "Q", "K", "A"]
SUITS = ["♠", "♣", "♦", "♥"]

EACH_RANK_COUNT = len(SUITS) # number of each rank (eg. 4 Aces in a deck)
EACH_SUIT_COUNT = len(RANKS) # number of each suit (eg. 6 Hearts in a deck)
TOTAL_CARDS_NUM = EACH_RANK_COUNT * EACH_SUIT_COUNT

SMALL_STRAIGHT_RANKS = {"9", "T", "J", "Q", "K"}
BIG_STRAIGHT_RANKS = {"T", "J", "Q", "K", "A"}

def is_rank_higher(rank_a, rank_b):
    return RANKS.index(rank_a) > RANKS.index(rank_b)

RANK_PAIRS = [(a,b) for (a,b) in list(itertools.product(RANKS, RANKS)) if a != b]
RANK_PAIRS_DESCENDING = [(a,b) for (a,b) in RANK_PAIRS if is_rank_higher(a, b)]

