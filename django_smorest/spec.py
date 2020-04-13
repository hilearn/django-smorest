from flask import Flask
from flask_smorest import Api
from django.conf import settings
from django.http.response import JsonResponse
from django.urls import path
from django.shortcuts import render_to_response


class OpenAPISpec:
    def __init__(self, name='', url_prefix=''):
        self.spec_urls = []
        self.url_prefix = url_prefix
        self._app = Flask(name)
        self._app.config = settings.OPENAPI_SETTINGS
        self._app.config['DEBUG'] = True
        self._api = Api(app=self._app)
        self._init_spec_urls()

    def register_blueprint(self, blp, **kwargs):
        if 'url_prefix' in kwargs:
            del kwargs['url_prefix']

        self._api.register_blueprint(
            blp, url_prefix=f'{self.url_prefix}{blp.url_prefix}',
            **kwargs)

    def _init_spec_urls(self):
        self.openapi_url = self._app.config.get('OPENAPI_URL_PREFIX', None)
        if self.openapi_url is not None:
            json_path = self._app.config.get(
                'OPENAPI_JSON_PATH', 'openapi.json')
            self.openapi_json_url = f'{self.openapi_url}/{json_path}'
            self.spec_urls.append(path(self.openapi_json_url,
                                       self._openapi_json,
                                       name='openapi-json'))

            self._register_redoc_url()
            self._register_swagger_ui_url()

    def _register_redoc_url(self):
        redoc_path = self._app.config.get('OPENAPI_REDOC_PATH')
        if redoc_path is not None:
            redoc_url = self._app.config.get('OPENAPI_REDOC_URL')
            if redoc_url is not None:
                self._redoc_url = redoc_url
                self.spec_urls.append(
                    path(f'{self.openapi_url}/{redoc_path}',
                         self._redoc_ui))

    def _register_swagger_ui_url(self):
        swagger_ui_path = self._app.config.get('OPENAPI_SWAGGER_UI_PATH')
        if swagger_ui_path is not None:
            swagger_ui_url = self._app.config.get('OPENAPI_SWAGGER_UI_URL')
            if swagger_ui_url is not None:
                self._swagger_ui_url = swagger_ui_url
                self.spec_urls.append(
                    path(f'{self.openapi_url}/{swagger_ui_path}',
                         self._swagger_ui))

    def _openapi_json(self, *args, **kwargs):
        spec_dict = self._api.spec.to_dict()
        if ('components' in spec_dict
                and 'securitySchemes' in spec_dict['components']):
            spec_dict['security'] = []
            for security in spec_dict['components']['securitySchemes'].keys():
                spec_dict['security'].append({security: []})

        return JsonResponse(spec_dict,
                            safe=False)

    def _redoc_ui(self, *args, **kwargs):
        return render_to_response(
            'redoc.html',
            {'title': self._app.name,
             'open_api_url': f'{self.url_prefix}/{self.openapi_json_url}',
             'redoc_url': self._redoc_url})

    def _swagger_ui(self, *args, **kwargs):
        return render_to_response(
            'swagger_ui.html',
            {'title': self._app.name,
             'open_api_url': f'{self.url_prefix}/{self.openapi_json_url}',
             'swagger_ui_url': self._swagger_ui_url})

    def to_dict(self):
        return self._api.spec.to_dict()

    def add_jwt_auth(self):
        jwt_scheme = {"type": "http", "scheme": "bearer",
                      "bearerFormat": "JWT"}

        self._api.spec.components.security_scheme("jwt", jwt_scheme)
