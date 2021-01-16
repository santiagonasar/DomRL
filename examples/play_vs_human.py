from domrl.engine.game import Game
from domrl.engine.agent import StdinAgent
import domrl.engine.cards.base as base


if __name__ == '__main__':
    """
    Run instances of the game.
    """
    game = Game(
        agents=[StdinAgent(), StdinAgent()],
        kingdoms=[base.BaseKingdom],
    )
    game.run()

