from domrl.engine.game import Game
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
    player_agent = DecisionLayersAgent([Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure()], StdinAgent())
    auto_player_agent = DecisionLayersAgent([Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate,
                                             ProvinceNeverLoseSemiAgent()], StdinAgent())
    auto_player_chapel_agent = DecisionLayersAgent([Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate,
                                                    ProvinceNeverLoseSemiAgent(), AggressiveChapelSemiAgent()], StdinAgent())
    market_no_buys = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent(), PassOnBuySemiAgent()], OldRandomAgent())
    my_heuristics_no_buy = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent(), PassOnBuySemiAgent()], OldRandomAgent())
    my_heuristics_big_money = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent(), big_money], OldRandomAgent())
    my_heuristics = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent()], OldRandomAgent())
    market_big_money = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent(), big_money], OldRandomAgent())
    market = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent()], OldRandomAgent())
    market_no_smithy = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent(), PassOnBuySemiAgent()], OldRandomAgent())
    market_no_smithy2 = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent2(), PassOnBuySemiAgent()], OldRandomAgent())
    market_player = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent()], StdinAgent())
    smithy_agent = DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(), SmithySemiAgent(),
         big_money], OldRandomAgent())
    # agent1 = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), SmithySemiAgent(), BigMoneySemiAgent()], RandomAgent())
    # agent2 = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), BigMoneySemiAgent()], RandomAgent())
    agents = [market, market_no_buys, market_big_money, my_heuristics, my_heuristics_no_buy, my_heuristics_big_money]
    agents = [market_no_smithy2]
    agents = [DecisionLayersAgent(
        [Autoplay(), NeverChoose(["Buy: Curse"]), PlayAllTreasure(), never_buy_copper_or_estate, ProvinceNeverLoseSemiAgent(), SmithySemiAgent(),
         BuyToHaveProportion({'Market': 1, 'Militia': 0.001, 'Smithy': 0.001, 'Village': 0.2}), PassOnBuySemiAgent()], OldRandomAgent())]
    #opponent = market_no_smithy
    #opponent = auto_player_agent
    agents = [DecisionLayersAgent([Autoplay()], Random())]
    opponent = BigMoneyAgent()
    teksts = []
    for agent in agents:
        p1vs = 0
        p2vs = 0
        draws = 0
        fails = 0
        rounds = 100
        for idx in range(0, rounds):
            print(f"Starting round {idx}.")
            if idx < rounds / 2:
                game = Game([agent, opponent], verbose=False, kingdoms=[BaseKingdom])
            else:
                game = Game([opponent, agent], verbose=False, kingdoms=[BaseKingdom])

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
                if (str(winners[0]) == 'Player 1') ^ (idx > rounds / 2):
                    p1vs += 1
                if (str(winners[0]) == 'Player 2') ^ (idx > rounds / 2):
                    p2vs += 1

        tekst = f'\nPlayer 1: {p1vs}; Player 2: {p2vs}; draws: {draws}; fails: {fails}; out of {rounds}'
        teksts.append(tekst)

    for text in teksts:
        print(text)
