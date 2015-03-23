#Lulu
Another web microframework for Python.

[![The Fae Sorceress, by adrusaurio (http://adrusaurio.tumblr.com/)](http://41.media.tumblr.com/412f6889177a7e9b0f213868947e418f/tumblr_mor56i6Ta21rs016xo1_320.png)](http://adrusaurio.tumblr.com/post/53525045449/lulu-the-fae-sorceress-definitely-my-fave-lol)

##Description
Lulu is a Python web microframework inspired by [Cuba](http://github.com/soveran/cuba), a microframework for Ruby.

##Not for using (yet)
Lulu is still a very immature project. So, it's not ready for application development. It will be available on PyPI _when it's done_.

##Still, how can I install Lulu?
Just download the latest master, copy the Lulu folder and install it's dependencies using `pip install -r requirements.txt`.

##Another framework?
_(or how Lulu tries to be different from the rest)_

Almost all web microframeworks in Python use function decorators to set endpoints. A few ones use class inheritance.

Lulu makes use of the `with` statement to set your application endpoints, and accepted HTTP methods are just properly named functions inside the `with` block.

The idea of using `with` as a way to write closures (which Cuba heavily relies on) came from [this article](http://billmill.org/multi_line_lambdas.html) from the near past (2009).

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
    Lulu.start()

```

On script execution (`python example.py`). Lulu will spawn a WSGIref server for development, listening to 0.0.0.0:1337. The default values for host and port are localhost:1500.

Declaring functions with names other than HTTP methods (GET, POST, PUT, etc) inside the endpoint block will be ignored.

If you want to serve applications using a WSGI server, for example Gunicorn, you need to point to the Lulu.serve method.

_Example_: `gunicorn example:Lulu.serve`

##Dependencies
The only two dependencies (for now) are `webob` and `wheezy.routing`. Got really confused trying to understand WSGI and too lazy to write a router.

##Is it compatible with Python 3?
Short answer: No.

Long answer: Tries to be compatible with Python 3, but it's not assured to work with.

##TODO
* Proper routing.
* Middleware support.
* Session handling.
* Cookie handling.
* Automated testing.
* `with` nesting for clearer URLs.

##License
The source code of Lulu is released under the [MIT license](http://choosealicense.com/licenses/mit/).
