from domrl.engine.agent import Agent
import numpy


class Random(Agent):

    def policy(self, decision, state):
        sample_size = decision.num_select
        if decision.optional:
            sample_size = min(decision.num_select, len(decision.moves))
            sample_size = numpy.random.binomial(n=sample_size, p=0.5, size=1)
        elif decision.num_select > len(decision.moves):
            raise Exception("Okay this is really weird, random has to choose more than possible.")


        to_return = numpy.random.choice(range(0, len(decision.moves)), replace=False, size=sample_size)
        return to_return
