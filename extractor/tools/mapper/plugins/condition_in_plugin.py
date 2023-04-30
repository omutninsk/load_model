from .base import BasePlugin


class ConditionIn(BasePlugin):
    """Плагин, проверяющий условие наличия значения параметра в указанном списке.
        :param name: Условное название для вызова.
        :param field: название поля исходного объекта, значение которого проверяется.
        :param values: список значений, при соответствии одному из них возвращается True.
        :return: True - при соблюдении условия, False - в противном случае"""

    name = "in"

    def __init__(self, name, field: str, values: []):
        if name != self.name:
            raise AttributeError('Invalid widget name.')
        self.field = field.split('.')
        self.values = values

    def run(self, source, target=None):
        value = self.get_param(obj=source, attrs_dict=self.field)
        return value in self.values
