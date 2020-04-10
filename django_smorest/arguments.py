from flask_smorest.arguments import ArgumentsMixin
from webargs.djangoparser import DjangoParser


class DjangoArgumentsMixin(ArgumentsMixin):
    ARGUMENTS_PARSER = DjangoParser()
