from rest_framework.views import APIView
from flask.views import MethodView


class View(APIView, MethodView):
    @classmethod
    def as_view(cls, *args, **kwargs):
        return super().as_view()
