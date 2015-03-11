# *-* coding: utf-8 *-*

import inspect
import functools
import webob
import webob.exc as HTTPErrors
import logging
from wheezy.routing import PathRouter as Router


""" The Application class. Used to define routes when objects are built. """


class App(object):

    HTTP_VERBS = frozenset([u'GET', u'POST', u'PUT', u'PATCH', u'DELETE'])
    __routes = Router()

    logger = logging.getLogger('Lulu')

    class EndPoint(object):

        __aliased = {}

        def __init__(self, methods, alias):
            if(not any(w in App.HTTP_VERBS for w in methods.keys())):
                raise Exception(
                    u'This endpoint needs at least one HTTP verb associated')
            self.methods = methods
            App.EndPoint.__aliased[alias] = self

        @staticmethod
        def get_alias(alias):
            return App.EndPoint.__aliased[alias] if alias in \
                App.EndPoint.__aliased.keys() else None

        def __call__(self, method):
            if method.upper() not in self.methods.keys():
                raise HTTPErrors.HTTPMethodNotAllowed()
            else:
                return self.methods[method]

    def __init__(self, route, alias):
        if not isinstance(route, unicode):
            raise TypeError(
                u'Router must be an Unicode string'
            )
        if App.EndPoint.get_alias(alias) is not None:
            raise Exception(
                u'URL alias already defined'
            )

        self.alias = alias
        self.route = route

    def __enter__(self):
        self.__previous_frame = {k.upper(): v for (k, v) in
                                 inspect.currentframe(1).f_locals.iteritems()
                                 if k.upper() in App.HTTP_VERBS}

    def __exit__(self, exc_type, exc_value, traceback):
        methods = {k.upper(): v for (k, v) in
                   inspect.currentframe(1).f_locals.iteritems()
                   if k.upper() in App.HTTP_VERBS
                   and v not in self.__previous_frame.values()}
        endpoint = App.EndPoint(methods, self.alias)
        App.__routes.add_route(self.route, endpoint)

    @staticmethod
    def _respond(request):
        response = webob.Response()
        App.logger.info(request)
        endpoint = App.__routes.match(request.path_info)[0]
        App.logger.info(endpoint)
        if(endpoint is None):
            raise HTTPErrors.HTTPNotFound

        after_process = endpoint(request.method)(request)

        response.content_type = 'text/plain'
        response.text = after_process
        response.headers.add('X-Powered-By', 'Lulu')
        return response

    @staticmethod
    def serve(environ, start_response):
        return App._respond(webob.Request(environ))(environ, start_response)

    @staticmethod
    def start():
        App.logger.setLevel(logging.INFO)
        App.logger.addHandler(logging.StreamHandler())
        from wsgiref.simple_server import make_server
        try:
            App.logger.info('Lulu is supporting in localhost:1500')
            make_server('', 1500, App.serve).serve_forever()
        except KeyboardInterrupt:
            App.logger.info('Lulu stopped supporting')