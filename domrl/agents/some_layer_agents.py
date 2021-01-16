from domrl.engine.game import Game
from domrl.engine.state import Player
from domrl.engine.agent import StdinAgent
from domrl.agents.my_agents import *
from domrl.agents.layer_agent import *
from domrl.agents.random_agent import Random
from domrl.agents.big_money_agent import BigMoneyAgent
from domrl.engine.cards.base import BaseKingdom

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
