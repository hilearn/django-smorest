from copy import deepcopy
from functools import wraps

from flask_smorest.arguments import ArgumentsMixin
from webargs.djangoparser import DjangoParser


class DjangoArgumentsMixin(ArgumentsMixin):
    ARGUMENTS_PARSER = DjangoParser()

    def arguments(
            self, schema, *, location='json', content_type=None, required=True,
            description=None, example=None, examples=None, **kwargs
    ):
        parameters = {
            'in': location,
            'required': required,
            'schema': schema,
        }
        if content_type is not None:
            parameters['content_type'] = content_type
        if example is not None:
            parameters['example'] = example
        if examples is not None:
            parameters['examples'] = examples
        if description is not None:
            parameters['description'] = description

        def decorator(func):

            @wraps(func)
            def wrapper(*f_args, **f_kwargs):
                return func(*f_args, **f_kwargs)

            # Add parameter to parameters list in doc info in function object
            # The deepcopy avoids modifying the wrapped function doc
            wrapper._apidoc = deepcopy(getattr(wrapper, '_apidoc', {}))
            docs = wrapper._apidoc.setdefault('arguments', {})
            docs.setdefault('parameters', []).append(parameters)

            # Call use_args (from webargs) to inject params in function
            return self.ARGUMENTS_PARSER.use_args(
                schema, location=location, **kwargs)(wrapper)

        return decorator
