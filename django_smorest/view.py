from rest_framework.views import APIView
from flask.views import MethodView


class View(APIView, MethodView):
    @classmethod
    def as_view(cls, *args, **kwargs):
        cls.methods.discard('OPTIONS')
        return super().as_view()
