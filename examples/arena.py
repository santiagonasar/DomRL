from domrl.engine.game import Game
from domrl.engine.state import Player
from domrl.engine.agent import StdinAgent
from domrl.agents.my_agents import *
from domrl.agents.layer_agent import *
from domrl.agents.random_agent import Random
from domrl.agents.big_money_agent import BigMoneyAgent
from domrl.agents.some_layer_agents import *
from domrl.engine.cards.base import * #BaseKingdom

agent = smithy_agent
opponent = BigMoneyAgent()
player_names = ["Market", "Smithy"]
playing_agents = [agent, opponent]
playing_agents_reverse = [opponent, agent]
players = [Player(player_names[i], i, playing_agents[i]) for i in range(0, 2)]
players_reverse = [Player(player_names[1-i], i, playing_agents_reverse[i]) for i in range(0, 2)]
p1vs = 0
p2vs = 0
draws = 0
fails = 0
rounds = 200
for idx in range(0, rounds):
    print(f"Starting round {idx}.")
    if idx < rounds / 2:
        game = Game(agents=playing_agents, players=players, verbose=False, kingdoms=[BaseKingdom])
    else:
        game = Game(agents=playing_agents_reverse, players=players_reverse, verbose=False, kingdoms=[BaseKingdom])

    try:
        game_state = game.run()
        winners = game_state.get_winners()
    except Exception as e:
        print(f"Error: {e}")
        fails += 1
        continue

    if len(winners) == 2:
        draws += 1
        print(f"It's a draw!")
    else:
        if (str(winners[0]) == player_names[0]) ^ (idx > rounds / 2):
            p1vs += 1
            print(f"{player_names[0]} wins!")
        if (str(winners[0]) == player_names[1]) ^ (idx > rounds / 2):
            p2vs += 1
            print(f"{player_names[1]} wins!")

text = f'\n{players[0]}: {p1vs}; {players[1]}: {p2vs}; draws: {draws}; fails: {fails}; out of {rounds}'

print(text)
