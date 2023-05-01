import re
from .base import BasePlugin


class ExtractRegexp(BasePlugin):

    name = "extract_regexp"

    def __init__(self, source: str, regexp: str, name=None, target=None, default=None):
        if target:
            self.target_field = self.get_fields(target)
        else:
            self.target_field = None
        self.source_field = self.get_fields(source)
        self.regexp = regexp
        self.default = default

    def run(self, target, source):
        value = self.get_param(obj=source, attrs_dict=self.source_field, default=self.default)
        if not isinstance(value, list):
            pattern = r"(\w+)=([\w\d]+)"
            params = {}
            for match in re.finditer(pattern, value):
                name = match.group(1)
                value = match.group(2)
                params[name] = value
            if self.target_field:
                self.set_param(obj=target, attrs_dict=self.target_field, value=params)
            else:
                for item in params:
                    self.set_param(obj=target, attrs_dict=[item], value=params[item])