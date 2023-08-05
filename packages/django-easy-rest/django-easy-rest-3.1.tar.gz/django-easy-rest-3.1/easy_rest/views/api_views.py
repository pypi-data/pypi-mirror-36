import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from django.conf import settings
from .debugger import DebugHandler, DebugCache
import inspect


class RestApiView(APIView):
    """
    this is the main api view of the django easy rest
    """

    # the function filed name in data for instance {"action":"get-user"}
    function_field_name = 'action'

    # the api allowed methods ('actions')
    api_allowed_methods_post = ['__all__']

    # the api allowed methods ('actions')
    api_allowed_methods_get = ['__all__']

    # the data to return on get of the api view
    get_data = {}

    # base_response initial value.
    base_response = None

    debugger = DebugCache()

    @property
    def api_allowed_method(self):
        if self.request.method == "GET":
            return self.api_allowed_methods_get
        elif self.request.method == "POST":
            return self.api_allowed_methods_post
        return []

    def get(self, request):
        """
        the get of the api
        :param request: WSGI request
        :return: (dict): Http Response
        """
        if type(self.get_data) is not dict and type(self.get_data) is not str:
            self.get_data = {}
        if not request.GET:
            return Response(self.get_data)
        else:
            return self.base_factory(base_data=request.GET, api_allowed_methods=self.api_allowed_methods_get)

    def _pythonize(self, name):
        """
        this is a base function to pythonize the fields

        for instance action: "HELLO_WORLD"
        will become a python friendly var by lowering each case
        and the result will be:

        action: "hello_world"

        :param name: the original field name
        :return: python friendly field.
        """
        return name.lower()

    def restifiy(self, data):
        """
        The restifiy method make api calls as the format of the current api view
        for instance restifiying the following data "hello world"
        returns "hello-world" this is used by the decorative keys mixin
        :param data: the data to restifiy
        :return: restified data
        """
        return data

    def post(self, request):
        return self.base_factory(base_data=request.data, api_allowed_methods=self.api_allowed_methods_post)

    def base_factory(self, base_data, api_allowed_methods):
        """
        The easy rest post method handle post requests and make abstractions for the rest mixins
        :param base_data: request base data
        :param api_allowed_methods: allowed methods for the api
        :return: (httpResponse) processed data
        """
        if settings.DEBUG:
            # creating a new debugger
            self.debugger = DebugCache()
            # reset last debug message
            if 'last_debug_error' in self.request.session:
                self.request.session['last_debug_error'] = None
                self.request.session.save()
        # creating the base response
        self.base_response = self.create_base_response(api_allowed_methods)
        try:
            # preparing the data by api abstractions if mixin is on.
            data = self.api_abstractions(base_data)
            # if this is a valid api request
            if self.function_field_name in data:

                # getting the requested action
                action = self._pythonize(data[self.function_field_name])
                try:

                    # if action is not allowed
                    if action not in api_allowed_methods and '__all__' not in api_allowed_methods:
                        # returning not allowed response
                        self.base_response['error'] = '{0} {1} not allowed , allowed {0} {2}'.format(
                            self.function_field_name,
                            action,
                            api_allowed_methods)
                        return self.return_response(data=self.base_response,
                                                    status=http_status.HTTP_403_FORBIDDEN)

                    # if this action is allowed searching for this action
                    _method = getattr(self, action)

                    # getting the output, debug-output, error for the method wrapper
                    # the method wrapper calls the method.
                    output, debug, error = self._method_wrapper(data, _method, action)
                    # updating the base response
                    if settings.DEBUG:
                        self.base_response['debug'].update(debug)
                    self.base_response['data'] = output
                    # if the method call is a success
                    if not error:
                        # returning the response
                        return self.return_response(data=self.base_response, status=http_status.HTTP_200_OK)
                    else:
                        # returning error response
                        return self.return_response(data=self.base_response,
                                                    status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

                # if this method was not found
                except (AttributeError, ImportError) as error:
                    # creating the correct error response
                    self.base_response['error'] = "{} not found".format(self.function_field_name)
                    if settings.DEBUG:
                        self.base_response['debug'].update({"exception": str(error)})
                    # returning the response
                    return self.return_response(data=self.base_response, status=http_status.HTTP_404_NOT_FOUND)
            else:
                # if the is no action in data creating the correct response
                self.base_response['error'] = "no {} in data".format(self.function_field_name)
                # returning the response.
                return self.return_response(data=self.base_response, status=http_status.HTTP_400_BAD_REQUEST)

        except (Exception, json.JSONDecodeError) as error:
            # if there is a general error
            self.base_response["error"] = "general api error"
            if settings.DEBUG:
                self.debug(error, "(Exception, json.JSONDecodeError)")
                self.base_response['debug'].update({self.restifiy('exception type'): str(type(error)),
                                                    self.restifiy('exception args'): error.args})
            # returning general error
            return self.return_response(data=self.base_response, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def rebuild_request_code(self):
        data = self.request.data
        get_url = ""
        if self.request.method == "GET":
            data = self.request.GET
            action = "GetSync"
            parameters_map = ""
            for key, value in data.items():
                parameters_map += "&{0}={1}".format(key, value)
            parameters_map = parameters_map[1:]
            get_url = "{0}{1}".format(self.request.path, parameters_map)
            get_url = "request url = \"{0}\"".format(get_url)
        else:
            action = "SendSync"

        return "\n".join([
            "// the code below is built to debug, and uses SyncRequests, "
            "if your request was Async, the code will generate a sync request",
            "api = new RequestHandler('{}')".format(self.request.path),
            "api.{}({});".format(action, json.dumps(data, indent=1)),
            "{0}".format(get_url)
        ])

    def debug(self, error, handler):
        if settings.DEBUG:
            self.debugger.update(error, handler)

    def return_response(self, data, status):
        request_data = self.request.data if self.request.method == "POST" else self.request.GET
        if status in [
            http_status.HTTP_400_BAD_REQUEST,
            http_status.HTTP_404_NOT_FOUND,
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        ]:
            self.request.session['last_debug_error'] = self.debugger.serialize()
            self.request.session.save()
            data["input"] = {
                "request_data": request_data,
                "request_code": self.rebuild_request_code()
            }
            return DebugHandler(request=self.request, data=data, status=status).handle()
        return Response(data, status)

    def create_base_response(self, api_allowed_methods):
        """
        creates the base response
        :return: base response object
        """
        if settings.DEBUG:
            return {'debug': {
                self.restifiy("api attributes"): {self.restifiy("api allowed methods"): api_allowed_methods}},
                'debug-mode': ["enabled", "to disable go to settings.py and change DEBUG=True to false"]}
        return {}

    def call_method(self, data, method):
        # basic call method in the easy rest
        args = list(inspect.signature(method).parameters)
        if "self" in args:
            args.remove("self")
        if len(args) > 0:
            return method(data)
        return method()

    def _method_wrapper(self, data, method, action):
        """

        wraps the functions call and the base response
        with the call response

        :param data: request.data (dict)
        :param method: method to call inside api (object)
        :param action: action name (str)
        :return: function data, debug, error [type = Bool]
        """
        # data it got from the call
        out = None
        # additional data to append
        additional = None
        # debug data
        debug = {}

        try:
            # calling the method
            out = self.call_method(data=data, method=method)
        except Exception as error:
            # if exception occurred while calling the method
            additional = {'error': "Exception occurred in method check function usage",
                          self.function_field_name: action}
            if settings.DEBUG:
                debug = {'exception-type': str(type(error)), 'exception-args': error.args}
                self.debug(error, "method_wrapper_base")

        if additional:
            return additional, debug, True
        if out:
            return out, debug, False
        if settings.DEBUG:
            return {}, {"error": '{} did not return any data'.format(self.function_field_name)}, True

    def api_abstractions(self, data):
        """
        Implement this method in the complex api mixins
        change base response here according to new data
        :param data:
        :return:
        """
        return data
