# *-* coding: utf-8 *-*

import inspect
import functools
import logging

import webob
import webob.exc as exc
import webob.dec as dec
from wheezy.routing import PathRouter as Router


_logger = logging.getLogger('Lulu')
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())


class _EndPoint(object):

    __aliased = {}

    def __init__(self, methods, alias):
        if(not any(w in App.HTTP_VERBS for w in methods.keys())):
            raise Exception(
                u'This endpoint needs at least one HTTP verb associated')
        self.methods = methods
        _EndPoint.__aliased[alias] = self

    @staticmethod
    def get_alias(alias):
        return _EndPoint.__aliased[alias] if \
            alias in _EndPoint.__aliased.keys() \
            else None

    def __call__(self, method):
        if method.upper() not in self.methods.keys():
            raise exc.HTTPMethodNotAllowed()
        else:
            return self.methods[method]

""" The Application class. Used to define routes when objects are built. """


class App(object):

    HTTP_VERBS = frozenset([u'GET', u'POST', u'PUT', u'PATCH', u'DELETE'])
    __routes = Router()

    logger = _logger
    session = Session()

    def __init__(self, route, alias):
        if not isinstance(route, unicode):
            raise TypeError(
                u'Route endpoint must be an unicode string'
            )
        if _EndPoint.get_alias(alias) is not None:
            raise Exception(
                u'Route alias already defined'
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
        endpoint = _EndPoint(methods, self.alias)
        App.__routes.add_route(self.route, endpoint, name=self.alias)

    @classmethod
    def _respond(cls, request):
        response = webob.Response()
        try:
            response.headers.add('X-Powered-By', 'Lulu')
            path_response = cls.__routes.match(request.path_info)
            endpoint = path_response[0]
            route_params = path_response[1]

            if endpoint is None:
                raise exc.HTTPNotFound()

            request.route_params = route_params
            request.path_for = cls.__routes.path_for
            try:
                result = endpoint(request.method)(request)
            except:
                raise exc.HTTPServerError()

            if isinstance(result, basestring):
                response.text = result
                response.charset = 'utf8'
            elif type(result) is dict:
                response.content_type = result['content_type'] if \
                    'content_type' in result.keys() else 'text/html'
                response.body = result['body']

        except exc.HTTPError as e:
            response = e
        finally:
            return response

    @staticmethod
    @dec.wsgify
    def serve(request):
        return App._respond(request)

    @classmethod
    def start(cls, host='', port=1500):

        welcome_messages = [
            u'Up we go!',
            u'Zippy!',
            u'Vroom vroom!',
            u'Delightify!'
        ]

        from wsgiref.simple_server import make_server
        from random import choice
        try:
            host = '127.0.0.1' if host == '' else host
            cls.logger.info('%s Lulu is supporting in %s:%d',
                            choice(welcome_messages), host, port)
            make_server(host, port, cls.serve).serve_forever()
        except KeyboardInterrupt:
            cls.logger.info('Lulu stopped supporting')
