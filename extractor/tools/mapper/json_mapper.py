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
        for rule in self.rules:
            if "name" in rule:
                operations[rule["name"]](**rule).run(target=self.target, source=self.source)
            if "bool_operation" in rule:
                Condition(**rule).run(target=self.target, source=self.source)
