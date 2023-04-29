"""API."""


from .user import user_blueprint
from .source_fields import source_fields_blueprint
from .sources import sources_blueprint
from .index import index_blueprint
from .model import model_blueprint
from tools.common import BlueprintContainer

blueprints = [BlueprintContainer(index_blueprint, "/"),]
blueprints.append(BlueprintContainer(user_blueprint, "/api/user"))
blueprints.append(BlueprintContainer(model_blueprint, "/api/model"))
blueprints.append(BlueprintContainer(sources_blueprint, "/api/sources"))
blueprints.append(BlueprintContainer(source_fields_blueprint, "/api/source_fields"))
