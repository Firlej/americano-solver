import pandas as pd
import streamlit as st
from Card import Card
from Deck import Deck
from counts import init_counts
from Solver import Solver
from helpers import RANKS, SUITS, RANK_PAIRS, RANK_PAIRS_DESCENDING

# Initialize Session State
if 'hand' not in st.session_state:
    st.session_state.hand = set()
if 'n' not in st.session_state:
    st.session_state.n = 1
            
st.title('Liars Poker Combinations Probability')

st.session_state.n = st.slider('Number of cards in play', min_value=1, max_value=24, value=1, step=1)

def toogle_card(card: Card):
    if card in st.session_state.hand:
        st.session_state.hand.remove(card)
    else:
        st.session_state.hand.add(card)

# Create a grid of buttons
for i, col in enumerate(st.columns(len(RANKS))):
    for suit in SUITS:
        card = Card(RANKS[i], suit)
        checkbox = col.checkbox(
            label = str(card),
            key = str(card),
            value=(card in st.session_state.hand),
            on_change=toogle_card, args = [card]
        )

solver = Solver(
    hand = list(st.session_state.hand),
    unknown_cards_in_play_num = st.session_state.n - len(st.session_state.hand)
)

s = pd.Series()

for rank in RANKS:
    s[f'probability_high_card_{rank}'] = solver.probability_high_card(rank = rank)
    
for rank in RANKS:
    s[f'probability_pair_{rank}'] = solver.probability_pair(rank = rank)
    
for a, b in RANK_PAIRS_DESCENDING:
    s[f'probability_two_pair_{a}_{b}'] = solver.probability_two_pair(rank_a = a, rank_b = b)
    
s[f'probability_small_straight'] = solver.probability_small_straight()

s[f'probability_big_straight'] = solver.probability_big_straight()

for rank in RANKS:
    s[f'probability_three_{rank}'] = solver.probability_three(rank = rank)
    
for a, b in RANK_PAIRS:
    s[f'probability_full_{a}_{b}'] = solver.probability_full(rank_a = a, rank_b = b)
    
for rank in RANKS:
    s[f'probability_quad_{rank}'] = solver.probability_quad(rank = rank)

for suit in SUITS:
    s[f'probability_flush_{suit}'] = solver.probability_flush(suit)
    
for suit in SUITS:
    s[f'probability_small_poker_{suit}'] = solver.probability_small_poker(suit)
    
for suit in SUITS:
    s[f'probability_big_poker_{suit}'] = solver.probability_big_poker(suit)
    
df = pd.DataFrame(s, columns=["Combinations"])
df = df.reset_index()

st.table(df)