import abc
import copy
import logging
import pathlib
import sys
from typing import AnyStr, List  # NOQA

import jinja2
import six
import yaml
from openapi_spec_validator.exceptions import OpenAPIValidationError
from six.moves.urllib.parse import urlsplit

from ..exceptions import InvalidSpecification, ResolverError
from ..json_schema import resolve_refs
from ..operations import OpenAPIOperation, Swagger2Operation
from ..options import ConnexionOptions
from ..resolver import Resolver
from ..utils import Jsonifier

MODULE_PATH = pathlib.Path(__file__).absolute().parent.parent
SWAGGER_UI_URL = 'ui'
NO_SPEC_VERSION_ERR_MSG = """Unable to get the spec version.
You are missing either '"swagger": "2.0"' or '"openapi": "3.0.0"'
from the top level of your spec."""

logger = logging.getLogger('connexion.apis.abstract')


def _get_spec_version(spec):
    try:
        version_string = spec.get('openapi') or spec.get('swagger')
    except AttributeError:
        raise InvalidSpecification(NO_SPEC_VERSION_ERR_MSG)
    if version_string is None:
        raise InvalidSpecification(NO_SPEC_VERSION_ERR_MSG)
    try:
        version_tuple = tuple(map(int, version_string.split(".")))
    except TypeError:
        err = ('Unable to convert version string to semantic version tuple: '
               '{version_string}.')
        err = err.format(version_string=version_string)
        raise InvalidSpecification(err)
    return version_tuple


class AbstractAPIMeta(abc.ABCMeta):

    def __init__(cls, name, bases, attrs):
        abc.ABCMeta.__init__(cls, name, bases, attrs)
        cls._set_jsonifier()


@six.add_metaclass(AbstractAPIMeta)
class AbstractAPI(object):
    """
    Defines an abstract interface for a Swagger API
    """

    def __init__(self, specification, base_path=None, arguments=None,
                 validate_responses=False, strict_validation=False, resolver=None,
                 auth_all_paths=False, debug=False, resolver_error_handler=None,
                 validator_map=None, pythonic_params=False, pass_context_arg_name=None, options=None):
        """
        :type specification: pathlib.Path | dict
        :type base_path: str | None
        :type arguments: dict | None
        :type validate_responses: bool
        :type strict_validation: bool
        :type auth_all_paths: bool
        :type debug: bool
        :param validator_map: Custom validators for the types "parameter", "body" and "response".
        :type validator_map: dict
        :param resolver: Callable that maps operationID to a function
        :param resolver_error_handler: If given, a callable that generates an
            Operation used for handling ResolveErrors
        :type resolver_error_handler: callable | None
        :param pythonic_params: When True CamelCase parameters are converted to snake_case and an underscore is appended
        to any shadowed built-ins
        :type pythonic_params: bool
        :param options: New style options dictionary.
        :type options: dict | None
        :param pass_context_arg_name: If not None URL request handling functions with an argument matching this name
        will be passed the framework's request context.
        :type pass_context_arg_name: str | None
        """
        self.debug = debug
        self.validator_map = validator_map
        self.resolver_error_handler = resolver_error_handler

        logger.debug('Loading specification: %s', specification,
                     extra={'swagger_yaml': specification,
                            'base_path': base_path,
                            'arguments': arguments,
                            'auth_all_paths': auth_all_paths})

        if isinstance(specification, dict):
            self.specification = specification
        else:
            specification_path = pathlib.Path(specification)
            self.specification = self.load_spec_from_file(arguments, specification_path)

        logger.debug('Read specification', extra={'spec': self.specification})

        self.spec_version = _get_spec_version(self.specification)

        self.options = ConnexionOptions(options, oas_version=self.spec_version)

        logger.debug('Options Loaded',
                     extra={'swagger_ui': self.options.openapi_console_ui_available,
                            'swagger_path': self.options.openapi_console_ui_from_dir,
                            'swagger_url': self.options.openapi_console_ui_path})

        # Avoid validator having ability to modify specification
        self.raw_spec = copy.deepcopy(self.specification)
        self._validate_spec(self.specification)
        self.specification = resolve_refs(self.specification)

        # https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md#fixed-fields
        # If base_path is not on provided then we try to read it from the swagger.yaml or use / by default
        self._set_base_path(base_path)

        # A list of MIME types the APIs can produce. This is global to all APIs but can be overridden on specific
        # API calls.
        self.produces = self.specification.get('produces', list())  # type: List[str]

        # A list of MIME types the APIs can consume. This is global to all APIs but can be overridden on specific
        # API calls.
        self.consumes = self.specification.get('consumes', ['application/json'])  # type: List[str]

        self.definitions = self.specification.get('definitions', {})
        self.components = self.specification.get('components', {})

        self.security = self.specification.get('security', dict())
        _security_schemes = self.components.get('securitySchemes', dict())
        self.security_definitions = self.specification.get(
            'securityDefinitions',
            _security_schemes
        )
        logger.debug('Security Definitions: %s', self.security_definitions)

        self.parameter_definitions = self.specification.get('parameters', {})
        self.response_definitions = self.specification.get('responses', {})

        self.resolver = resolver or Resolver()

        logger.debug('Validate Responses: %s', str(validate_responses))
        self.validate_responses = validate_responses

        logger.debug('Strict Request Validation: %s', str(validate_responses))
        self.strict_validation = strict_validation

        logger.debug('Pythonic params: %s', str(pythonic_params))
        self.pythonic_params = pythonic_params

        logger.debug('pass_context_arg_name: %s', pass_context_arg_name)
        self.pass_context_arg_name = pass_context_arg_name

        if self.options.openapi_spec_available:
            self.add_openapi_json()

        if self.options.openapi_console_ui_available:
            self.add_swagger_ui()

        self.add_paths()

        if auth_all_paths:
            self.add_auth_on_not_found(self.security, self.security_definitions)

    def _validate_spec(self, spec):
        if self.spec_version < (3, 0, 0):
            from openapi_spec_validator import validate_v2_spec as validate_spec
        else:
            from openapi_spec_validator import validate_v3_spec as validate_spec
        try:
            validate_spec(spec)
        except OpenAPIValidationError as e:
            raise InvalidSpecification.create_from(e)

    def _set_base_path(self, base_path):
        # type: (AnyStr) -> None
        if self.spec_version < (3, 0, 0):
            if base_path is None:
                base_path = self.specification.get('basePath', '')
                self.base_path = canonical_base_path(base_path)
            else:
                self.base_path = canonical_base_path(base_path)
                self.raw_spec['base_path'] = self.base_path
                self.specification['base_path'] = self.base_path
        else:
            servers = self.specification.get('servers', [])
            if base_path is None:
                # get the base_path from the spec
                try:
                    # assume we're the first server in list
                    server = copy.deepcopy(servers[0])
                    server_vars = server.pop("variables", {})
                    server['url'] = server['url'].format(
                        **{k: v['default'] for k, v
                           in six.iteritems(server_vars)}
                    )
                    base_path = urlsplit(server['url']).path
                except IndexError:
                    base_path = ''
                self.base_path = canonical_base_path(base_path)
            else:
                # overwrite the servers block with the given base_path
                self.base_path = canonical_base_path(base_path)
                user_servers = [{'url': self.base_path}]
                self.raw_spec['servers'] = user_servers
                self.specification['servers'] = user_servers

    @abc.abstractmethod
    def add_openapi_json(self):
        """
        Adds openapi spec to {base_path}/openapi.json
             (or {base_path}/swagger.json for swagger2)
        """

    @abc.abstractmethod
    def add_swagger_ui(self):
        """
        Adds swagger ui to {base_path}/ui/
        """

    @abc.abstractmethod
    def add_auth_on_not_found(self, security, security_definitions):
        """
        Adds a 404 error handler to authenticate and only expose the 404 status if the security validation pass.
        """

    def add_operation(self, method, path, swagger_operation, path_parameters):
        """
        Adds one operation to the api.

        This method uses the OperationID identify the module and function that will handle the operation

        From Swagger Specification:

        **OperationID**

        A friendly name for the operation. The id MUST be unique among all operations described in the API.
        Tools and libraries MAY use the operation id to uniquely identify an operation.

        :type method: str
        :type path: str
        :type swagger_operation: dict
        """

        shared_args = {
            "method": method,
            "path": path,
            "path_parameters": path_parameters,
            "operation": swagger_operation,
            "app_security": self.security,
            "validate_responses": self.validate_responses,
            "validator_map": self.validator_map,
            "strict_validation": self.strict_validation,
            "resolver": self.resolver,
            "pythonic_params": self.pythonic_params,
            "uri_parser_class": self.options.uri_parser_class,
            "pass_context_arg_name": self.pass_context_arg_name
        }

        if self.spec_version < (3, 0, 0):
            operation = Swagger2Operation(self,
                                          app_produces=self.produces,
                                          app_consumes=self.consumes,
                                          security_definitions=self.security_definitions,
                                          definitions=self.definitions,
                                          parameter_definitions=self.parameter_definitions,
                                          response_definitions=self.response_definitions,
                                          **shared_args)
        else:
            operation = OpenAPIOperation(self,
                                         components=self.components,
                                         **shared_args)

        self._add_operation_internal(method, path, operation)

    @abc.abstractmethod
    def _add_operation_internal(self, method, path, operation):
        """
        Adds the operation according to the user framework in use.
        It will be used to register the operation on the user framework router.
        """

    def _add_resolver_error_handler(self, method, path, err):
        """
        Adds a handler for ResolverError for the given method and path.
        """
        operation = self.resolver_error_handler(err,
                                                security=self.security,
                                                security_definitions=self.security_definitions)
        self._add_operation_internal(method, path, operation)

    def add_paths(self, paths=None):
        """
        Adds the paths defined in the specification as endpoints

        :type paths: list
        """
        paths = paths or self.specification.get('paths', dict())
        for path, methods in paths.items():
            logger.debug('Adding %s%s...', self.base_path, path)

            # search for parameters definitions in the path level
            # http://swagger.io/specification/#pathItemObject
            path_parameters = methods.get('parameters', [])

            for method, endpoint in methods.items():
                if method == 'parameters':
                    continue
                try:
                    self.add_operation(method, path, endpoint, path_parameters)
                except ResolverError as err:
                    # If we have an error handler for resolver errors, add it as an operation.
                    # Otherwise treat it as any other error.
                    if self.resolver_error_handler is not None:
                        self._add_resolver_error_handler(method, path, err)
                    else:
                        self._handle_add_operation_error(path, method, err.exc_info)
                except Exception:
                    # All other relevant exceptions should be handled as well.
                    self._handle_add_operation_error(path, method, sys.exc_info())

    def _handle_add_operation_error(self, path, method, exc_info):
        url = '{base_path}{path}'.format(base_path=self.base_path, path=path)
        error_msg = 'Failed to add operation for {method} {url}'.format(
            method=method.upper(),
            url=url)
        if self.debug:
            logger.exception(error_msg)
        else:
            logger.error(error_msg)
            six.reraise(*exc_info)

    def load_spec_from_file(self, arguments, specification):
        from openapi_spec_validator.loaders import ExtendedSafeLoader
        arguments = arguments or {}

        with specification.open(mode='rb') as openapi_yaml:
            contents = openapi_yaml.read()
            try:
                openapi_template = contents.decode()
            except UnicodeDecodeError:
                openapi_template = contents.decode('utf-8', 'replace')

            openapi_string = jinja2.Template(openapi_template).render(**arguments)
            return yaml.load(openapi_string, ExtendedSafeLoader)  # type: dict

    @classmethod
    @abc.abstractmethod
    def get_request(self, *args, **kwargs):
        """
        This method converts the user framework request to a ConnexionRequest.
        """

    @classmethod
    @abc.abstractmethod
    def get_response(self, response, mimetype=None, request=None):
        """
        This method converts the ConnexionResponse to a user framework response.
        :param response: A response to cast.
        :param mimetype: The response mimetype.
        :param request: The request associated with this response (the user framework request).

        :type response: ConnexionResponse
        :type mimetype: str
        """

    @classmethod
    @abc.abstractmethod
    def get_connexion_response(cls, response):
        """
        This method converts the user framework response to a ConnexionResponse.
        :param response: A response to cast.
        """

    def json_loads(self, data):
        return self.jsonifier.loads(data)

    @classmethod
    def _set_jsonifier(cls):
        import json
        cls.jsonifier = Jsonifier(json)


def canonical_base_path(base_path):
    """
    Make given "basePath" a canonical base URL which can be prepended to paths starting with "/".
    """
    return base_path.rstrip('/')
