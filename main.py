from domrl.engine.game import Game
from domrl.engine.state import Player
from domrl.engine.agent import StdinAgent
from domrl.agents.my_agents import *
from domrl.agents.layer_agent import *
from domrl.agents.random_agent import Random
from domrl.agents.big_money_agent import BigMoneyAgent
from domrl.engine.cards.base import * #BaseKingdom

"""
Run instances of the game.
"""

if __name__ == '__main__':
    default = DecisionLayersAgent([Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(),
                                   BuyDuchyIfTakingLastProvinceLoses, BuyProvince,
                                   BuyCopperIfLessThanFiveGold, never_buy_copper_or_estate])

    player_agent = DecisionLayersAgent([Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure()], StdinAgent())
    auto_player_agent = DecisionLayersAgent([default], StdinAgent())
    auto_player_chapel_agent = DecisionLayersAgent([default, AggressiveChapelSemiAgent()], StdinAgent())
    market_no_buys = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketSemiAgent, PassOnBuySemiAgent()], Random())
    my_heuristics_no_buy = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MyHeuristic, PassOnBuySemiAgent()], Random())
    my_heuristics_big_money = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MyHeuristic, big_money], Random())
    my_heuristics = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MyHeuristic], Random())
    market_big_money = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketSemiAgent, big_money], Random())
    market = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketSemiAgent], Random())
    market_no_smithy = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent, PassOnBuySemiAgent()], Random())
    market_no_smithy2 = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent2, PassOnBuySemiAgent()], Random())
    market_player = DecisionLayersAgent(
        [default, AggressiveChapelSemiAgent(), MarketSemiAgent], StdinAgent())
    smithy_agent = DecisionLayersAgent(
        [default, SmithySemiAgent, big_money], Random())
    big_money = DecisionLayersAgent([default, big_money, PassOnBuySemiAgent], Random())

    agents = [market, market_no_buys, market_big_money, my_heuristics, my_heuristics_no_buy, my_heuristics_big_money]
    #agents = [DecisionLayersAgent(
    #    [default, SmithySemiAgent, BuyToHaveProportion({'Market': 1, 'Militia': 0.001, 'Smithy': 0.001, 'Village': 0.2}), PassOnBuySemiAgent()], OldRandomAgent())]

    agents = [auto_player_agent]
    opponent = auto_player_agent
    teksts = []
    for agent in agents:
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
                game = Game(agents=playing_agents, players=players, verbose=True, kingdoms=[BaseKingdom])
            else:
                game = Game(agents=playing_agents_reverse, players=players_reverse, verbose=True, kingdoms=[BaseKingdom])

            try:
                game_state = game.run()
                winners = game_state.get_winners()
            except Exception as e:
                print(f"Error: {e}")
                fails += 1
                continue

            if len(winners) == 2:
                draws += 1
            else:
                if (str(winners[0]) == player_names[0]) ^ (idx > rounds / 2):
                    p1vs += 1
                if (str(winners[0]) == player_names[1]) ^ (idx > rounds / 2):
                    p2vs += 1

        tekst = f'\n{players[0]}: {p1vs}; {players[1]}: {p2vs}; draws: {draws}; fails: {fails}; out of {rounds}'
        teksts.append(tekst)

    for text in teksts:
        print(text)
