import string

import numpy
import copy


class Agent(object):
    def choose(self, decision, state):
        return decision.moves[0]


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


class APIAgent(Agent):

    def choose(self, decision, state):

        # Autoplay
        # if len(decision.moves) == 1:
        #     return [0]

        player = decision.player
        actions = player.actions
        buys = player.buys
        coins = player.coins
        moves = decision.moves
        hand = player.hand
        state

        while True:
            user_input = input()
            if user_input == "?":
                state.event_log.print(player)
                print(state)
            else:
                ans = list(map(lambda x: int(x.strip()), user_input.split(',')))

                break
        return ans


class RandomAgent(Agent):

    def choose(self, decision, state):
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

    def choose(self, decision, state):
        if 'Buy' in decision.prompt:
            return [0]


class CleverAgentOld(Agent):

    def __init__(self, agent):
        self.agent = agent

    def choose(self, decision, state):
        initialDecision = copy.deepcopy(decision)

        # Automove If One Move
        if len(decision.moves) == 1:
            return [0]

        for idx in range(0, len(initialDecision.moves)):
            move = initialDecision.moves[idx]
            if "Buy: Curse" in move.__str__():
                decision.moves.pop(idx)
            if hasattr(move, "card") and (
                    move.card.add_actions > 0 or ("treasure" in decision.prompt.lower() and move.card.coins > 0)):
                return self.restrictDecision(decision.moves, initialDecision.moves, idx)

        restrictedChoice = self.agent.choose(self, decision, state)
        return self.restrictDecision(decision.moves, initialDecision.moves, restrictedChoice[0])

    def restrictDecision(self, moves, initialMoves, chosen):
        for idx in range(0, len(initialMoves)):
            if str(initialMoves[idx]) == str(moves[chosen]):
                return list([idx])

        return [chosen]


class RulesSemiAgent(Agent):
    def choose(self, decision, state):
        # Automove If One Move
        if len(decision.moves) == 1:
            return [0]

        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if "Bandit" in str(move):  # currently does not work
                decision.moves.pop(idx)

            if "Remodel" in str(move):  # currently does not work
                decision.moves.pop(idx)


class CleverSemiAgent(Agent):

    def choose(self, decision, state):
        # Automove If One Move
        if len(decision.moves) == 1:
            return [0]

        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if "Buy: Curse" in move.__str__():
                decision.moves.pop(idx)
            if hasattr(move, "card") and (
                    move.card.add_actions > 0 or ("treasure" in decision.prompt.lower() and move.card.coins > 0)):
                return [idx]


class ApplySemiAgent(Agent):
    def __init__(self, semiAgents, agent):
        self.semiAgents = semiAgents
        self.agent = agent

    def choose(self, decision, state):
        for semiAgent in self.semiAgents:
            value = semiAgent.choose(decision, state)
            if value is not None:
                return value

        return self.agent.choose(self.agent, decision, state)


class BigMoneySemiAgent(Agent):
    def choose(self, decision, state):
        for stringDesired in ["Buy: Province", "Buy: Gold", "Buy: Silver"]:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in move.__str__():
                    return [idx]


class SmithySemiAgent(Agent):
    def choose(self, decision, state):
        for stringDesired in ["Play: Smithy"]:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in move.__str__():
                    return [idx]

        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if "Buy: Smithy" in move.__str__() and (
                    sum(1 for c in decision.player.all_cards if 'Smithy' in str(c)) / len(
                decision.player.all_cards) < 0.1):
                return [idx]


class DontBuyCopperOrEstateSemiAgent(Agent):

    def choose(self, decision, state):
        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if 'Buy: Copper' in str(move) or 'Buy: Estate' in str(move):
                decision.moves.pop(idx)


class MyHeuristicSemiAgent(Agent):
    def choose(self, decision, state):
        for stringDesired in []:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in move.__str__():
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


class MarketSemiAgent(Agent):
    def choose(self, decision, state):

        if 'Action' in decision.prompt:
            for stringDesired in ['Empty']:
                for idx in range(0, len(decision.moves)):
                    try:
                        move = decision.moves[idx]
                    except:
                        break

                    if 'Militia' in str(move):
                        return [idx]

                    if 'Smithy' in str(move) and decision.player.actions > 1:
                        return [idx]

                    if stringDesired in str(move):
                        return [idx]

        if 'Buy' not in decision.prompt and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        desired_deck = {'Market': 1, 'Militia': 0.001, 'Smithy': 0.001, 'Village': 0.2}

        for wish in desired_deck:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move):
                    if sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                            decision.player.all_cards) < desired_deck[wish]:
                        return [idx]


class CustomHeuristicsSemiAgent(Agent):
    def __init__(self, desired_decks):
        self.desired_decks = desired_decks

    def choose(self, decision, state):

        if 'Action' in decision.prompt:
            for stringDesired in ['Empty']:
                for idx in range(0, len(decision.moves)):
                    try:
                        move = decision.moves[idx]
                    except:
                        break

                    if 'Militia' in str(move):
                        return [idx]

                    if 'Smithy' in str(move) and decision.player.actions > 1:
                        return [idx]

                    if stringDesired in str(move):
                        return [idx]

        if 'Buy' not in decision.prompt and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        for wish in self.desired_deck:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move):
                    if sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                            decision.player.all_cards) < self.desired_deck[wish]:
                        return [idx]


class MarketNoSmithySemiAgent(Agent):
    def choose(self, decision, state):

        if 'Action' in decision.prompt:
            for stringDesired in ['Empty']:
                for idx in range(0, len(decision.moves)):
                    try:
                        move = decision.moves[idx]
                    except:
                        break

                    if 'Militia' in str(move):
                        return [idx]

                    if 'Smithy' in str(move) and decision.player.actions > 1:
                        return [idx]

                    if stringDesired in str(move):
                        return [idx]

        if 'Buy' not in decision.prompt and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        desired_deck = {'Market': 1, 'Militia': 0.1, 'Village': 0.2}

        for wish in desired_deck:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move):
                    if sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                            decision.player.all_cards) < desired_deck[wish]:
                        return [idx]


class MarketNoSmithySemiAgent2(Agent):
    def choose(self, decision, state):

        if 'Action' in decision.prompt:
            for stringDesired in ['Empty']:
                for idx in range(0, len(decision.moves)):
                    try:
                        move = decision.moves[idx]
                    except:
                        break

                    if 'Militia' in str(move):
                        return [idx]

                    if 'Smithy' in str(move) and decision.player.actions > 1:
                        return [idx]

                    if stringDesired in str(move):
                        return [idx]

        if 'Buy' not in decision.prompt and 'Choose a pile to gain card from.' not in decision.prompt:
            return

        desired_deck = {'Market': 1, 'Militia': 0.2, 'Village': 0.2}

        for wish in desired_deck:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if wish in str(move):
                    if sum(1 for c in decision.player.all_cards if wish in str(c)) / len(
                            decision.player.all_cards) < desired_deck[wish]:
                        return [idx]


class OnlyBuyCopperIfSemiAgent(Agent):
    def choose(self, decision, state):
        for idx in range(0, len(decision.moves)):
            try:
                move = decision.moves[idx]
            except:
                break

            if "Buy: Copper" in str(move):
                if sum(c.coins for c in decision.player.all_cards) < 5:
                    return [idx]
                else:
                    decision.moves.pop(idx)


class ChapelSemiAgent(Agent):

    def choose(self, decision, state):
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

                if "Choose: Estate" in move.__str__():
                    moves.append(idx)

            for idx in range(0, len(decision.moves)):
                if len(moves) >= 4:
                    break
                try:
                    move = decision.moves[idx]
                except:
                    break

                if "Choose: Copper" in move.__str__() and (
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

    def choose(self, decision, state):
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


class ProvinceSemiAgent(Agent):
    def choose(self, decision, state):
        for stringDesired in ["Buy: Province"]:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in move.__str__():
                    return [idx]


class ProvinceNeverLoseSemiAgent(Agent):
    def choose(self, decision, state):
        desired_strings = ["Buy: Province"]
        if (state.supply_piles['Province'].qty == 1 and
                (6 + decision.player.total_vp() <
                 max(state.all_players, key=lambda pr: pr.total_vp()).total_vp())):
            desired_strings = ["Buy: Duchy"]

        for stringDesired in desired_strings:
            for idx in range(0, len(decision.moves)):
                try:
                    move = decision.moves[idx]
                except:
                    break

                if stringDesired in str(move):
                    return [idx]
