from .base import BasePlugin


class Copy(BasePlugin):
    """Плагин, копирующий значение параметра исходного объекта в заданный параметр целевого объекта.
            :param target: название поля целевого объекта, в которое устанавливается значение.
            :param source: название поля исходного объекта, откуда берется значение.
            :param default: значение, если source = None.
            :param save_as_list: Если равно True, то значение заносится в список в целевом поле, по умолчанию - False"""

    name = "copy"

    def __init__(self, target: str, source: str, name=None, default=None, save_as_list=False):
        self.target_field = self.get_fields(target)
        self.source_field = self.get_fields(source)
        self.default = default
        self.save_as_list = save_as_list

    def run(self, target, source):
        value = self.get_param(obj=source, attrs_dict=self.source_field, default=self.default)
        if self.save_as_list and not isinstance(self.value, list):
            value = [value]
        self.set_param(obj=target, attrs_dict=self.target_field, value=value)
