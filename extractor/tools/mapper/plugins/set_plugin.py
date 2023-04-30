from .base import BasePlugin


class Set(BasePlugin):
    """Плагин, устанавливающий заданное значение в необходимом поле объекта.
    :param target: название поля целевого объекта, в которое устанавливается значение.
    :param value: устанавливаемое значение.
    :param save_as_list: Если равно True, то значение заносится в список в целевом поле, по умолчанию - False"""

    name = "set"
    value = None

    def __init__(self, target: str, value, name=None, save_as_list=False):
        self.target_field = self.get_fields(target)
        if save_as_list and not isinstance(self.value, list):
            self.value = [value]
        else:
            self.value = value

    def run(self, target, source):
        self.set_param(obj=target, attrs_dict=self.target_field, value=self.value)