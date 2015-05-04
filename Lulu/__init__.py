# *-* coding: utf-8 *-*

import inspect
import functools
import logging

import webob
import webob.exc as exc
import webob.dec as dec
from wheezy.routing import PathRouter as Router
from beaker.session import SessionObject


"""Lulu current version string"""
_VERSION = '0.0.1'

_logger = logging.getLogger('Lulu')
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler())


_default_configuration = {
    'debug': False,
    'session.encrypt_key': None,
    'session.cookie_expires': True,
    'session.cookie_domain': None,
    'session.cookie_path': '/',
    'session.httponly': False,
    'session.key': 'lulu.session',
    'session.data_dir': None,
    'session.invalidate_corrupt': False,
    'session.secure': None,
    'session.secret': None,
    'session.timeout': None,
    'session.type': None,
    'session.validate_key': None,
    'show_x_powered_by': True,
}


class _EndPoint(object):

    __aliased = {}

    def __init__(self, methods, alias):
        if(not any(w in App.HTTP_VERBS for w in methods.keys())):
            raise KeyError(
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


class _Request(object):

    def __init__(self, **kwargs):
        self.session = kwargs['session']
        self.route_params = kwargs['route_params']
        self.path_for = kwargs['path_for']
        self.raw = kwargs['raw']

    def __set__(self, name, value):
        raise Exception('Request data cannot be changed')


class App(object):

    HTTP_VERBS = frozenset([u'GET', u'POST', u'PUT', u'PATCH', u'DELETE'])
    __routes = Router()

    __config = _default_configuration.copy()
    __session_config = None

    def __init__(self, route, alias):
        if not isinstance(route, unicode):
            raise TypeError(
                u'Route endpoint must be an unicode string'
            )
        if _EndPoint.get_alias(alias) is not None:
            raise RuntimeError(
                u'Route alias {0} already defined'.format(alias)
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
    def config(cls, kwargs):
        for key, value in kwargs.iteritems():
            if key in cls.__config:
                cls.__config[key] = value
            else:
                raise Exception('Custom configuration cannot be added')

    @classmethod
    def __get_session_config(cls):
        if cls.__session_config is None:
            cls.__session_config = {k.replace(u'session.', ''): v for (k, v) in
                                    cls.__config.iteritems() if
                                    k.startswith('session.')}
        return cls.__session_config

    @classmethod
    def _respond(cls, request):
        try:
            path_response = cls.__routes.match(request.path_info)
            if path_response[0] is None:
                raise exc.HTTPNotFound()

            endpoint = path_response[0]
            session = SessionObject(
                request.environ, **cls.__get_session_config())

            try:
                method = endpoint(request.method)
                result = method(
                    _Request(
                        session=session,
                        route_params=path_response[1],
                        path_for=cls.__routes.path_for,
                        raw=request
                    )
                )

            except Exception as e:
                raise exc.HTTPServerError()

            response = webob.Response()

            if session.accessed():
                if not session.dirty():
                    session.save()
                session.persist()
                cookie = session.__dict__['_headers']['cookie_out'] if \
                    session.__dict__['_headers']['set_cookie'] else None
                if cookie:
                    response.headers.add('Set-Cookie', cookie)

            if cls.__config['show_x_powered_by']:
                response.headers.add(
                    'X-Powered-By', 'Lulu version %s' % _VERSION)

            if isinstance(result, basestring):
                response.text = result
                response.charset = 'utf8'
            elif type(result) is dict:
                response.content_type = result['content_type'] if \
                    'content_type' in result.keys() else 'text/html'
                response.body = result['body']

            return response
        except exc.HTTPError as e:
            return e

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
