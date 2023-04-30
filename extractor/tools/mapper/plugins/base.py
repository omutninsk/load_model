import copy
from abc import abstractmethod

class BasePlugin:
    name = None
    target = None
    source = None

    @abstractmethod
    def run(self, source, target):
        pass

    def get_fields(self, fields):
        """
        :param fields: Строка с перечислением полей, разделенных точкой, например "first.2.third". Целым числом
        обозначается индекс в массиве. Исходный объект: { 'first': [None, {'third':'value'}]}
        :return: Список полей.
        """
        if len(fields) == 0:
            raise ValueError('Invalid field format')
        try:
            array = []
            result = fields.split('.')
            for item in result:
                try:
                    array.append(int(item))
                except Exception as e:
                    array.append(item)
            return array
        except Exception as e:
            raise ValueError('Invalid field format', str(e))
        return None

    def get_param(self, obj, attrs_dict, default=None):
        """
        :param obj: Объект в котором происходит поиск нужного значения
        :param attrs_dict: Список полей по порядку вложенности
        :param default: Значение по умолчанию, если искомый параметр равен None
        :return: Искомое значение
        """
        if len(attrs_dict) == 1:
            if obj[attrs_dict[0]] is not None:
                return obj[attrs_dict[0]]
            else:
                return default
        else:
            return self.get_param(obj[attrs_dict[0]], attrs_dict[1:], default)

    def set_param(self, obj, attrs_dict, value):
        """
        :param obj: Объект, которому нужно присвоить значение
        :param attrs_dict: Список полей по порядку вложенности(число - это индекс в списке)
        :param value: Присваиваемое значение
        :return: Объект с присвоенным значением поля
        """
        if not attrs_dict:
            raise AttributeError("Invalid parameters value.")
        elif len(attrs_dict) == 1:
            obj[attrs_dict[0]] = value
        else:
            key, *keys = attrs_dict
            if isinstance(keys[0], int):
                obj.setdefault(key, [])
                if len(obj[key]) < keys[0]:
                    obj[key].extend([None] * (keys[0] - len(obj[key]) + 1))
            obj[key] = self.set_param(obj[key] if key in obj else {}, keys, value)
        return obj
