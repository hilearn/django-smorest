from copy import deepcopy
from functools import wraps

from flask_smorest.compat import MARSHMALLOW_VERSION_MAJOR
from flask_smorest.utils import deepupdate


class DjangoResponseMixin:
    def response(
            self, schema=None, *, code=200, description=None,
            example=None, examples=None, headers=None
    ):
        if isinstance(schema, type):
            schema = schema()

        resp_doc = {}
        doc_schema = self._make_doc_response_schema(schema)
        if doc_schema is not None:
            resp_doc['schema'] = doc_schema
        if description is not None:
            resp_doc['description'] = description
        if example is not None:
            resp_doc['example'] = example
        if examples is not None:
            resp_doc['examples'] = examples
        if headers is not None:
            resp_doc['headers'] = headers
        doc = {'responses': {code: resp_doc}}

        def decorator(func):

            @wraps(func)
            def wrapper(*args, **kwargs):

                # Execute decorated function
                result = func(*args, **kwargs)
                result_raw = result.content

                # Dump result with schema if specified
                if schema is None:
                    result_dump = result_raw
                else:
                    result_dump = schema.dump(result_raw)
                    if MARSHMALLOW_VERSION_MAJOR < 3:
                        result_dump = result_dump.data
                result.content = result_dump
                return result

            # Store doc in wrapper function
            # The deepcopy avoids modifying the wrapped function doc
            wrapper._apidoc = deepupdate(
                deepcopy(getattr(wrapper, '_apidoc', {})), doc)
            return wrapper

        return decorator
