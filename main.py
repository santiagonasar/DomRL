from domrl.engine.game import Game
from domrl.engine.agent import StdinAgent
from domrl.agents.my_agents import RandomAgent, PassOnBuySemiAgent, CleverSemiAgent, BigMoneySemiAgent, ApplySemiAgent, RulesSemiAgent, SmithySemiAgent, MyHeuristicSemiAgent, MarketSemiAgent, ChapelSemiAgent, AggressiveChapelSemiAgent, ProvinceSemiAgent, ProvinceNeverLoseSemiAgent, OnlyBuyCopperIfSemiAgent, DontBuyCopperOrEstateSemiAgent, MarketNoSmithySemiAgent, MarketNoSmithySemiAgent2, CustomHeuristicsSemiAgent
from domrl.agents.big_money_agent import BigMoneyAgent

"""
Run instances of the game.
"""

if __name__ == '__main__':
    player_agent = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent()], StdinAgent())
    auto_player_agent = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(),
                                        ProvinceNeverLoseSemiAgent()], StdinAgent())
    auto_player_chapel_agent = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(),
                                        ProvinceNeverLoseSemiAgent(), AggressiveChapelSemiAgent()], StdinAgent())
    market_no_buys = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent(), PassOnBuySemiAgent()], RandomAgent())
    my_heuristics_no_buy = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent(), PassOnBuySemiAgent()], RandomAgent())
    my_heuristics_big_money = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent(), BigMoneySemiAgent()], RandomAgent())
    my_heuristics = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MyHeuristicSemiAgent()], RandomAgent())
    market_big_money = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent(), BigMoneySemiAgent()], RandomAgent())
    market = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent()], RandomAgent())
    market_no_smithy = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent(), PassOnBuySemiAgent()], RandomAgent())
    market_no_smithy2 = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketNoSmithySemiAgent2(), PassOnBuySemiAgent()], RandomAgent())
    market_player = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(),
         AggressiveChapelSemiAgent(), MarketSemiAgent()], StdinAgent())
    smithy_agent = ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), SmithySemiAgent(),
         BigMoneySemiAgent()], RandomAgent())
    # agent1 = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), SmithySemiAgent(), BigMoneySemiAgent()], RandomAgent())
    # agent2 = ApplySemiAgent([RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), BigMoneySemiAgent()], RandomAgent())
    agents = [market, market_no_buys, market_big_money, my_heuristics, my_heuristics_no_buy, my_heuristics_big_money]
    agents = [market_no_smithy2]
    agents = [ApplySemiAgent(
        [RulesSemiAgent(), CleverSemiAgent(), DontBuyCopperOrEstateSemiAgent(), ProvinceNeverLoseSemiAgent(), SmithySemiAgent(),
         CustomHeuristicsSemiAgent({'Market': 1, 'Militia': 0.001, 'Smithy': 0.001, 'Village': 0.2}), PassOnBuySemiAgent()], RandomAgent())]
    #opponent = market_no_smithy
    #opponent = auto_player_agent
    agents = [auto_player_agent]
    opponent = smithy_agent
    teksts = []
    for agent in agents:
        p1vs = 0
        p2vs = 0
        draws = 0
        fails = 0
        rounds = 1
        for idx in range(0, rounds):
            if idx < rounds / 2:
                game = Game([agent, opponent])
            else:
                game = Game([opponent, agent])

            try:
                winners = game.run()
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
