from django.conf import settings
from django.contrib import admin
from axes.decorators import watch_login

_login_view_path = getattr(settings, 'AXES_LOGIN_VIEW',\
                               'django.contrib.auth.views.login')
_module_name = '.'.join(_login_view_path.split('.')[:-1])
_login_view = _login_view_path.split('.')[-1]
_module = __import__(_module_name, globals(), locals(),
                     [_login_view,], -1
                    )
login_view = getattr(_module, _login_view, None)

class FailedLoginMiddleware(object):

    def __init__(self, *args, **kwargs):
        super(FailedLoginMiddleware, self).__init__(*args, **kwargs)

        # watch the admin login page
        admin.site.login = watch_login(admin.site.login)

        # and the regular auth login page
        _module.__dict__[_login_view] = watch_login(login_view)


class FailedAdminLoginMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(FailedAdminLoginMiddleware, self).__init__(*args, **kwargs)

        # watch the admin login page
        admin.site.login = watch_login(admin.site.login)


class FailedAuthLoginMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(FailedAuthLoginMiddleware, self).__init__(*args, **kwargs)

        # watch the regular auth login page
        _module.__dict__[_login_view] = watch_login(login_view)
