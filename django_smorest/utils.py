import json
from functools import wraps

from marshmallow.exceptions import ValidationError
from django.http import HttpResponseBadRequest


def return_bad_request_if_error(func):
    """
    Django Rest framework endpoint decorator for handling webargs
    schema validation error.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return HttpResponseBadRequest(
                content=json.dumps(e.normalized_messages()),
                content_type='application/json')

    return wrapper
