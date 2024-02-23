import pandas as pd
import streamlit as st
from Card import Card
from Deck import Deck
from simulate import init_counts
from Solver import Solver, combinations
from helpers import RANKS, SUITS, RANK_PAIRS, RANK_PAIRS_DESCENDING

# Initialize Session State
if 'hand' not in st.session_state:
    st.session_state.hand = set()
if 'n' not in st.session_state:
    st.session_state.n = 2
            
st.title('Liars Poker Combinations Probability')

st.session_state.n = st.slider('Number of cards in play', min_value=2, max_value=24, value=1, step=1)

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

for name, method, kwargs in combinations:
    s[name] = getattr(solver, method)(**kwargs)
    
df = pd.DataFrame(s, columns=["Combinations"])
df = df.reset_index()

st.table(df)