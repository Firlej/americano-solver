from typing import List, Dict
from Deck import Deck
from collections import namedtuple
import random

from Solver import Solver, combinations

# Player = namedtuple("Player", ["name", "hand", "solver"])

class Player:
    def __init__(self, player_id, hand=None, solver=None):
        self.id = player_id
        self.hand = hand
        self.hand_count = 1
        self.solver = solver
        
    def __repr__(self) -> str:
        return f"Player(name={self.name}, hand={self.hand}, solver={self.solver})"

class GameOffline:
    def __init__(self, player_ids: List[str]):
            
        self.players = [
            Player(
                player_id = player_id,
                hand = None,
                solver = None
            )
            for player_id in player_ids
        ]
        
        self.player_turn_index = 0
        
    def deal(self):
    
        hands = Deck().get_hands([player.hand_count for player in self.players])
        
        self.cards = Deck.from_hands(hands)
        n = len(self.cards.cards)
        
        print([n for n in self.cards.combinations.keys()])
        
        for player, hand in zip(self.players, hands):
            player.hand = hand
            player.solver = Solver(hand, n)
        
        for i, player in enumerate(self.players):
            print(i, player.id, player.hand)
        
        self.last_bet = None
        
    def finish_deal(self, loser_player_index = None):
        
        loser = self.players[loser_player_index]
        
        print(f"Player {loser.id} lost the deal!")
        
        loser.hand_count += 1
        
        MAX_CARDS = 1
        
        if loser.hand_count > MAX_CARDS:
            print(f"Player {loser.id} is out!")
            del self.players[loser_player_index]
        
        self.player_turn_index = loser_player_index
    
    def end(self):
        assert len(self.players) == 1
        
        winner = self.players[0]
        
        print(f"The winner is {winner.id}!")
        
    def play(self):
        while len(self.players) >= 2:
        
            self.deal()
            
            while True:
                
                assert len(self.players) >= 2
                
                current_player = self.players[self.player_turn_index]
                
                bet = input(f"{current_player.id}, enter your bet: ")
                
                if bet == "check":
                    if self.last_bet is None:
                        print("You can't check on first turn. Try again.")
                        continue
                    
                    loser_player_index = self.player_turn_index
                    if not self.cards.combinations[self.last_bet]:
                        loser_player_index = (self.player_turn_index - 1) % len(self.players)
                        
                    self.finish_deal(loser_player_index)
                    break
                
                if bet not in self.cards.combinations:
                    print("Invalid bet. Try again.")
                    continue
                
                def bet_index(bet: str):
                    return list(self.cards.combinations.keys()).index(bet)
                
                # bet_index = lambda x: list(self.cards.combinations.keys()).index(bet)
                
                if self.last_bet is not None and bet_index(self.last_bet) >= bet_index(bet):
                    print("Your bet must be higher than the last one. Try again.")
                    continue
                    
                self.last_bet = bet
                
                self.player_turn_index = (self.player_turn_index + 1) % len(self.players)
        
        self.end()

if __name__ == "__main__":
    player_ids = ["A", "B", "C"]
    game = GameOffline(player_ids) # Initialize a game with 3 players
    game.play()