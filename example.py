# *-* coding: utf-8 *-*

from Lulu import App as Lulu


with Lulu(u'/', u'index'):
    def get(request):
        Lulu.logger.info('Route Name is %s', request.route_params['route_name'])
        if not 'times' in request.session:
            request.session['times'] = 1
        else:
            request.session['times'] += 1
        Lulu.logger.info('Accesed %d times' % request.session['times'])
        return u'Yup, that tasted purple.'

with Lulu(u'/{name:word}', 'name'):
    def get(request):
        Lulu.logger.info('Route Name is %s', request.route_params['route_name'])
        return u'Hi, %s' % request.route_params['name']

if __name__ == '__main__':
    Lulu.start()
