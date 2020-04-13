from flask_smorest.blueprint import Blueprint
from .arguments import DjangoArgumentsMixin
from .response import DjangoResponseMixin


class DjangoBlueprint(DjangoArgumentsMixin, DjangoResponseMixin, Blueprint):
    pass
