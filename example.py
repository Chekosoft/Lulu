# *-* coding: utf-8 *-*

from Lulu import App as Lulu


with Lulu(u'/', u'index'):
  def get(request):
    return u'Yup, that tasted purple.'


if __name__ == '__main__':
    Lulu.start()
