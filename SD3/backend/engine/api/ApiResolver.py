from SD3.backend.engine.Resource.ResourceRegistry import resource_registry
from SD3.backend.engine.action.ActionRegistry import actions
from SD3.backend.engine.form.FormRegistry import form_registry
from SD3.backend.engine.list.ListRegistry import list_registry
from SD3.backend.engine.matrix.MatrixRegistry import matrix_registry


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