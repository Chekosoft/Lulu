#Lulu
Another web microframework for Python.

[![The Fae Sorceress, by adrusaurio (http://adrusaurio.tumblr.com/)](http://41.media.tumblr.com/412f6889177a7e9b0f213868947e418f/tumblr_mor56i6Ta21rs016xo1_320.png)](http://adrusaurio.tumblr.com/post/53525045449/lulu-the-fae-sorceress-definitely-my-fave-lol)

##Description
Lulu is a Python web microframework inspired by [Cuba](http://github.com/soveran/cuba), a microframework for Ruby.

##Still in development
Lulu is still a very immature project. So, it's not a great idea to develop applications with. It will be ready when it's listed on PyPI.

##Still, how can I install Lulu?
Just download and extract the latest master and install using `pip install -e /folder/to/Lulu`.

##Another framework?
_(or how Lulu tries to be different from the rest)_

Almost all web microframeworks in Python use function decorators to set endpoints. A few ones use objects.

Lulu makes use of the `with` statement to define proper routes. Then, it checks if there are properly named functions inside the
`with` blocks and assigns them depending the HTTP verb declared in the name of the function.

The idea of using `with` as a way to write closures (which Cuba heavily relies on) came from [this article](http://billmill.org/multi_line_lambdas.html).

##A small example
```python
# *-* coding: utf-8 *-*

from Lulu import App as Lulu


with Lulu(u'/', u'index'):
    def get(request):
        Lulu.logger.info('Route Name is %s', request.route_params['route_name'])
        return u'Yup, that tasted purple.'

#How Lulu handles named parameters
with Lulu(u'/{name:word}', u'name'):
    def get(request):
        Lulu.logger.info('Route Name is %s', request.route_params['route_name'])
        return u'Hi, %s' % request.route_params['name']

if __name__ == '__main__':
    Lulu.start(host='0.0.0.0', port=1337)

```

On script execution (`python example.py`). Lulu will spawn a WSGIref server for development, listening to 0.0.0.0:1337. The default values for host and port are localhost:1500.

Declaring functions with names other than HTTP methods (GET, POST, PUT, etc) inside the endpoint block will be ignored.

If you want to serve applications using a WSGI server, you need to point to the Lulu.serve method.

##Dependencies
* `webob` to handle web requests and responses.
* `wheezy.routing` for routing
* `beaker` for session handling.


##Is it compatible with Python 3?
For the moment, no.

##TODO
* Middleware support.
* Automated testing.
* Default error pages.
* `with` nesting for clearer URLs.

##License
The source code of Lulu is released under the [MIT license](http://choosealicense.com/licenses/mit/).
