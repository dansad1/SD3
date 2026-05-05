# core/api/engine/resource/BaseResource.py

class BaseResource:
    code: str = ""

    def check_permission(self, request):
        pass

    def get(self, request, **params):
        raise NotImplementedError