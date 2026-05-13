from backend.engine.entity.EntityRegistry import EntityRegistry
from backend.engine.form.FormRegistry import form_registry
from backend.engine.list.ListRegistry import list_registry


class AppRegistry:

    def register(self, *, entity, list=None, form=None):

        # -------------------------
        # ENTITY
        # -------------------------
        entity_instance = EntityRegistry.register(entity)

        code = entity_instance.entity

        # -------------------------
        # LIST (override only)
        # -------------------------
        if list is not None:
            list_registry.register(list)

        # иначе ничего не делаем
        # list_registry сам создаст AutoEntityList при первом get

        # -------------------------
        # FORM (override only)
        # -------------------------
        if form is not None:
            form_registry.register(form)

        # иначе fallback произойдёт в registry