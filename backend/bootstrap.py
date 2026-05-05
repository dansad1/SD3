from SD3.backend.engine.Resource.ResourceRegistry import resource_registry
from SD3.backend.engine.action.ActionRegistry import actions
from SD3.backend.engine.entity.EntityRegistry import entity_registry
from SD3.backend.engine.matrix.MatrixRegistry import matrix_registry
from SD3.backend.engine.utils.autodiscover import autodiscover_all


def bootstrap():
    autodiscover_all()

    entity_registry.autodiscover()
    actions.autodiscover()
    resource_registry.autodiscover()
    matrix_registry.autodiscover()