import numpy
import copy
from domrl.engine.agent import Agent
from domrl.agents.layer_agent import DecisionLayersAgent
from domrl.engine.util import TurnPhase, CardType

"""
class StdinAgent(Agent):
    def choose(self, decision, state):

        # Autoplay
        if len(decision.moves) == 1:
            return [0]

        player = decision.player

        print(f" ==== Decision to be made by {player} ==== ")
        print(f"Actions: {player.actions} | Buys: {player.buys} | Coins: {player.coins}")
        print("Hand: ", list(map(str, player.hand)))
        print(decision.prompt)

        for idx, move in enumerate(decision.moves):
            print(f"{idx}: {move}")

        # Get user input and process it.
        while True:
            user_input = input()
            if user_input == "?":
                state.event_log.print(player)
                print(state)
            else:
                try:
                    ans = list(map(lambda x: int(x.strip()), user_input.split(',')))
                except:
                    print('Clearly invalid input. Please try again.')
                    continue

                break
        return ans
"""


class OldRandomAgent(Agent):

    def policy(self, decision, state):
        if 'Trash up to 4' in decision.prompt:  # for chapel
            my_list = []
            range_max = numpy.random.randint(0, min(len(decision.moves), 4) + 1, 1, int)
            for idx in range(0, range_max[0]):
                new_item = -1
                while new_item == -1 or new_item in my_list:
                    new_item = numpy.random.randint(0, len(decision.moves), 1, int)[0]
                my_list.append(new_item)

            return my_list

        if len(decision.moves) == 0:
            return []

        if 'Discard down to 3 cards' in decision.prompt:  # for militia
            my_list = []
            range_max = max(len(decision.player.hand) - 3, 0)
            for idx in range(0, range_max):
                new_item = -1
                while new_item == -1 or new_item in my_list:
                    new_item = numpy.random.randint(0, len(decision.moves), 1, int)[0]
                my_list.append(new_item)

            return my_list

        value = list(numpy.random.randint(0, len(decision.moves), 1, int))
        return value


class PassOnBuySemiAgent(Agent):

    def policy(self, decision, state):
        if decision.player.phase == TurnPhase.BUY_PHASE:  #'Buy' in decision.prompt:
            return [0]


class Autoplay(Agent):
    def policy(self, decision, state):
        if len(decision.moves) == 1:
            return [0]

        if len(decision.moves) == 0:
            return []


class PlayAllTreasure(Agent):

    def policy(self, decision, state):

        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if decision.player.phase == TurnPhase.TREASURE_PHASE and hasattr(move, "card") and \
                    move.card.is_type(CardType.TREASURE):
                return [idx]


class ConditionalChoose(Agent):
    def __init__(self, choose, condition=lambda decision, state: False):
        self.choose = choose
        self.condition = condition

    def policy(self, decision, state):
        if not self.condition(decision, state):
            return

        for desired in self.choose:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if desired in str(move):
                    return [idx]


def AlwaysChoose(always):
    return ConditionalChoose(always, lambda decision, state: True)


big_money = AlwaysChoose(["Buy: Gold", "Buy: Silver"])


class NeverChoose(Agent):
    def __init__(self, never):
        self.never = never

    def policy(self, decision, state):
        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            for never in self.never:
                if never in str(move):
                    decision.moves.pop(idx)


never_buy_copper_or_estate = NeverChoose(["Buy: Copper", "Buy: Estate"])


class MyHeuristicSemiAgent(Agent):
    def policy(self, decision, state):
        for stringDesired in []:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in str(move):
                    return [idx]

        if 'Action' in decision.prompt:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if 'Militia' in str(move) or 'Smithy' in str(move):
                    return [idx]

        if 'Buy' not in decision.prompt and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        desired_deck = {'Festival': 1, 'Market': 1, 'Militia': 1, 'Smithy': 0.1, 'Village': 0.2}
        if numpy.random.randint(0, 2, 1, int) == 1:
            desired_deck = {'Market': 1, 'Festival': 1, 'Smithy': 0.1, 'Militia': 1, 'Village': 0.2}

        for wish in desired_deck:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move) and (
                        sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                        decision.player.all_cards) < desired_deck[wish]):
                    return [idx]


class BuyToHaveProportion(Agent):
    def __init__(self, proportions_desired):
        self.proportions_desired = proportions_desired

    def policy(self, decision, state):

        if decision.player.phase != TurnPhase.BUY_PHASE and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        for wish in self.proportions_desired:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move):
                    if sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                            decision.player.all_cards) < self.proportions_desired[wish]:
                        return [idx]


SmithySemiAgent = DecisionLayersAgent([AlwaysChoose(["Play: Smithy"]), BuyToHaveProportion([{"Smithy": 0.1}])])


MarketNoSmithySemiAgent = DecisionLayersAgent([ConditionalChoose(["Play: Smithy"], lambda decision, state: decision.player.actions > 1),
                                               AlwaysChoose(["Play: Militia"]),
                                               BuyToHaveProportion({'Market': 1, 'Militia': 0.1, 'Village': 0.2})])


MarketNoSmithySemiAgent2 = DecisionLayersAgent([ConditionalChoose(["Play: Smithy"], lambda decision, state: decision.player.actions > 1),
                                               AlwaysChoose(["Play: Militia"]),
                                               BuyToHaveProportion({'Market': 1, 'Militia': 0.2, 'Village': 0.2})])


MarketSemiAgent = DecisionLayersAgent([ConditionalChoose(["Play: Smithy"], lambda decision, state: decision.player.actions > 1),
                                       AlwaysChoose(["Play: Militia"]),
                                       BuyToHaveProportion({'Market': 1, 'Militia': 0.001, 'Smithy': 0.001, 'Village': 0.2})])


OnlyBuyCopperIfSemiAgent = ConditionalChoose(["Buy: Silver", "Buy: Copper"], lambda decision, state: decision.player.coins_in_all_cards() < 5)


class ChapelSemiAgent(Agent):

    def policy(self, decision, state):
        if 'Action' in decision.prompt:
            for c in decision.player.hand:
                if 'Estate' in str(c):
                    for idx in range(0, len(decision.moves)):
                        if 'Play: Chapel' in str(decision.moves[idx]):
                            return [idx]

        if 'Trash up to 4' in decision.prompt:
            moves = []
            for idx in range(0, len(decision.moves)):
                if len(moves) >= 4:
                    break
                try:
                    move = decision.moves[idx]
                except:
                    break

                if "Choose: Estate" in str(move):
                    moves.append(idx)

            for idx in range(0, len(decision.moves)):
                if len(moves) >= 4:
                    break
                try:
                    move = decision.moves[idx]
                except:
                    break

                if "Choose: Copper" in str(move) and (
                        sum(c.coins for c in decision.player.all_cards) -
                        sum(1 for planned_move in moves if 'Copper' in str(planned_move)) > 5):
                    moves.append(idx)

            return moves

        if 'Buy' in decision.prompt:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if 'Buy: Chapel' in str(move) and decision.player.coins < 4 and (
                        sum(1 for c in decision.player.all_cards if 'Chapel' in str(c)) == 0):
                    return [idx]


class AggressiveChapelSemiAgent(ChapelSemiAgent):

    def policy(self, decision, state):
        if 'Action' in decision.prompt:
            for c in decision.player.hand:
                if 'Estate' in str(c) or ('Copper' in str(c) and sum(c.coins for c in decision.player.all_cards) > 5):
                    for idx in range(0, len(decision.moves)):
                        if 'Play: Chapel' in str(decision.moves[idx]):
                            return [idx]

        if 'Trash' in decision.prompt:
            moves = []
            for idx in range(0, len(decision.moves)):
                if len(moves) >= 4:
                    break
                try:
                    move = decision.moves[idx]
                except:
                    break

                if "Choose: Estate" in str(move):
                    moves.append(idx)

            for idx in range(0, len(decision.moves)):
                if len(moves) >= 4:
                    break
                try:
                    move = decision.moves[idx]
                except:
                    break

                if "Choose: Copper" in str(move) and (
                        sum(c.coins for c in decision.player.all_cards) -
                        sum(1 for planned_move in moves if 'Copper' in str(decision.moves[planned_move])) > 5):
                    moves.append(idx)

            return moves

        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if "Buy: Chapel" in str(move) and (sum(1 for c in decision.player.all_cards if 'Chapel' in str(c)) > 0):
                decision.moves.pop(idx)

            if "Buy: Chapel" in str(move) and decision.player.coins < 4 and (
                    sum(1 for c in decision.player.all_cards if 'Chapel' in str(c)) == 0):
                return [idx]


BuyProvince = AlwaysChoose(["Buy: Province"])


BuyDuchyIfTakingLastProvinceLoses = ConditionalChoose(["Buy: Duchy"], lambda decision, state:
                (state.supply_piles['Province'].qty == 1 and
                (6 + decision.player.total_vp() <
                max(state.other_players, key=lambda pr: pr.total_vp).total_vp)))


BuyDuchyIfThreeProvincesLeft = ConditionalChoose(["Buy: Duchy"], lambda decision, state:
                (state.supply_piles['Province'].qty <= 3))
