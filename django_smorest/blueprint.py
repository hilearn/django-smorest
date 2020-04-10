from flask_smorest.blueprint import Blueprint
from .arguments import DjangoArgumentsMixin


class DjangoBlueprint(DjangoArgumentsMixin, Blueprint):
    pass
