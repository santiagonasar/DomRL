from domrl.engine.agent import Agent


class DecisionLayersAgent(Agent):
    def __init__(self, decision_layers, final_instance=None):
        self.decision_layers = decision_layers
        self.final_instance = final_instance

    def policy(self, decision, state):
        for layer in self.decision_layers:
            value = layer.policy(decision, state)
            if value is not None:
                return value

        if self.final_instance is not None:
            return self.final_instance.policy(decision, state)
