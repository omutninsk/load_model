from .plugins import operations, Condition


class JsonMapper:
    source = None
    target = None
    rules = None

    def __init__(self, source, target, rules):
        self.source = source
        self.target = target
        self.rules = rules

    def run(self):
        target = self.target
        source = self.source
        for rule in self.rules:
            if "name" in rule:
                target = {}
                operations[rule["name"]](**rule).run(target=target, source=source)
                source = target
            if "bool_operation" in rule:
                Condition(**rule).run(target=target, source=self)
        return target