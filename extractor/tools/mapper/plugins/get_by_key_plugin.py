from .base import BasePlugin


class GetByKey(BasePlugin):
    """Плагин, находящий в массиве объект по ключу и возвращающий указанное значение.
            :param target: название поля целевого объекта, в которое устанавливается значение.
            :param source: название поля исходного объекта, откуда берется значение.
            :param default: значение, если source = None.
            :param save_as_list: Если равно True, то значение заносится в список в целевом поле, по умолчанию - False"""

    name = "get_by_key"

    def __init__(self, target: str, source: str, key: str, key_value: str, return_key=None, name=None, default=None, save_as_list=False):
        self.target_field = self.get_fields(target)
        self.source_field = self.get_fields(source)
        self.key = key
        self.key_value = key_value
        self.return_key = return_key
        self.default = default
        self.save_as_list = save_as_list

    def run(self, target, source):
        value = self.get_param(obj=source, attrs_dict=self.source_field, default=self.default)
        if isinstance(value, list):
            element = next(item for item in value if item[self.key] == self.key_value)
            if self.return_key:
                self.set_param(obj=target, attrs_dict=self.target_field, value=element.get(self.return_key,None))
            else:
                self.set_param(obj=target, attrs_dict=self.target_field, value=element)