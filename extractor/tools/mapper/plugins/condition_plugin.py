from .base import BasePlugin
from .condition_in_plugin import ConditionIn
from .condition_and_plugin import ConditionAnd
from .condition_exists_plugin import ConditionExists
from .copy_plugin import Copy
from .set_plugin import Set

operations = [Copy, Set]
bool_operations = [ConditionIn, ConditionAnd, ConditionExists]


class Condition(BasePlugin):
    """Плагин, проверяющий указанное условие и выполняющий сценарии.
        :param bool_operation: Логическая операция.
        :param negative: список операций если bool_operation возвращает False.
        :param positive: список операций если bool_operation возвращает True."""
    name = "condition"
    handler = None
    bool_operation = None
    negative = []
    positive = []

    def __init__(self, bool_operation, negative, positive):
        self.bool_operation = bool_operation
        self.handler = next((op for op in bool_operations if op.name == bool_operation["name"]), None)
        if not self.handler:
            raise ValueError('Invalid plugin name')

        self.negative = [op(**item) for item in negative for op in operations if item["name"] == op.name]
        self.positive = [op(**item) for item in positive for op in operations if item["name"] == op.name]

    def run(self, target=None, source=None):
        result = self.handler(**self.bool_operation).run(target=target, source=source)
        if result:
            for item in self.positive:
                item.run(target=target, source=source)
            return True
        else:
            for item in self.negative:
                item.run(target=target, source=source)
            return False
