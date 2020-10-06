from backend.controller.strategy.tag_strategy import TagStrategy
from backend.controller.strategy.label_strategy import LabelStrategy
from backend.controller.strategy.company_strategy import ConpanyStrategy

class StrategyContext:

    def __init__(self,type):
        if type == 'tag':
            self.cs = TagStrategy()
        elif type == 'company':
            self.cs = ConpanyStrategy()
        else:
            self.cs =LabelStrategy()

    def getPossibleResult(self,words):
        return self.cs.getResult(words)


