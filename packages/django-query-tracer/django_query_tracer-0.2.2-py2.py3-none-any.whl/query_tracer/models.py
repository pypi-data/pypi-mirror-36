import django
from django.core import exceptions
from django.core.exceptions import ImproperlyConfigured

from query_tracer.logger import GenericLogger
from query_tracer.logger import EnhancedLogger
from query_tracer.logger import TimeLogger

import logging


MODULES = []


# def check_installed_apps_configuration():
#     """
#     Check the app is put in correct order in INSTALLED_APPS

#     django.contrib.staticfiles runserver command is likely to
#     override query_tracer management command if put in wrong order.

#     Django had reversed order of management commands collection prior to 1.7
#     https://code.djangoproject.com/ticket/16599
#     """
#     from django.conf import settings
#     try:
#         staticfiles_index = settings.INSTALLED_APPS.index('django.contrib.staticfiles')
#         devserver_index = settings.INSTALLED_APPS.index('query_tracer')
#     except ValueError:
#         pass
#     else:
#         latest_app_overrides = django.VERSION < (1, 7)
#         if devserver_index < staticfiles_index and latest_app_overrides:
#             logging.error(
#                 'Put "query_tracer" below "django.contrib.staticfiles" in INSTALLED_APPS to make it work')
#         elif devserver_index > staticfiles_index and not latest_app_overrides:
#             logging.error(
#                 'Put "query_tracer" above "django.contrib.staticfiles" in INSTALLED_APPS to make it work')


def load_modules():
    global MODULES

    MODULES = []

    from query_tracer import settings

    for path in settings.QUERYTRACER_MODULES:
        try:
            name, class_name = path.rsplit('.', 1)
        except ValueError:
            raise exceptions.ImproperlyConfigured('%s isn\'t a query_tracer module' % path)

        try:
            module = __import__(name, {}, {}, [''])
        except ImportError as e:
            raise exceptions.ImproperlyConfigured('Error importing query_tracer module %s: "%s"' % (name, e))

        try:
            cls = getattr(module, class_name)
        except AttributeError:
            raise exceptions.ImproperlyConfigured('Error importing query_tracer module "%s" does not define a "%s" class' % (name, class_name))

        try:
            if class_name in ['SQLSummaryModule', ]:
                instance = cls(EnhancedLogger(cls))
            elif class_name in ['TimeModule', ]:
                instance = cls(TimeLogger(cls))
            else:
                instance = cls(GenericLogger(cls))
        except:
            raise  # Bubble up problem loading panel

        MODULES.append(instance)

if not MODULES:
    #check_installed_apps_configuration()
    load_modules()
