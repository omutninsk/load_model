from .copy_plugin import Copy
from .set_plugin import Set
from .condition_plugin import Condition
from .condition_in_plugin import ConditionIn
from .condition_and_plugin import ConditionAnd
from .condition_exists_plugin import ConditionExists


operations = {
    "copy": Copy,
    "set": Set}
bool_operations = {
    "in": ConditionIn,
    "and": ConditionAnd,
    "exists": ConditionExists}