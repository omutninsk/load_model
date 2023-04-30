from .base import BasePlugin


class ConditionExists(BasePlugin):
    """Плагин, проверяющий условие наличия значения параметра в указанном списке.
        :param name: Условное название для вызова.
        :param field: название поля исходного объекта, которое проверяется на наличие значения.
        :return: True - при соблюдении условия, False - в противном случае"""

    name = "exists"
    def __init__(self, name, field: str):
        if name != self.name:
            raise AttributeError('Invalid widget name.')
        self.field = field.split('.')

    def run(self, source, target=None):
        try:
            self.get_param(obj=source, attrs_dict=self.field)
            return True
        except Exception:
            return False
