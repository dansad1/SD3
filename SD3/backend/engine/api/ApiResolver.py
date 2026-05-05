# core/api/engine/api/ApiResolver.py
from core.api.engine.Resource.ResourceRegistry import resource_registry
from core.api.engine.form.FormRegistry import form_registry
from core.api.engine.list.ListRegistry import list_registry
from core.api.engine.action.ActionRegistry import actions
from core.api.engine.matrix.MatrixRegistry import matrix_registry


class ApiResolver:

    def resolve(self, code: str):

        # form
        if code.endswith(".form"):
            return form_registry.get(code)

        # list
        if code.endswith(".list"):
            return list_registry.get(code)

        # matrix
        try:
            return matrix_registry.get(code)
        except KeyError:
            pass

        # action
        try:
            return actions.get(code)
        except KeyError:
            pass

        # resource
        try:
            return resource_registry.get(code)
        except KeyError:
            pass

        raise KeyError(f"Unknown API code: {code}")


api_resolver = ApiResolver()