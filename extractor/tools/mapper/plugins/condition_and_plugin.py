from .base import BasePlugin
from .condition_exists_plugin import ConditionExists
from .condition_in_plugin import ConditionIn

class ConditionAnd(BasePlugin):
    name = "and"
    operands = []

    def __init__(self, operands):
        bool_operations = [ConditionExists, ConditionIn, ConditionAnd]
        for operand in operands:
            for item in bool_operations:
                if item.name == operand['name']:
                    self.operands.push(item(**operand))

    def run(self, target=None, source=None):
        result = False
        for item in self.operands:
            result = result and item.run(target=target, source=source)
        return result
