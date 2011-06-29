import logging
import os

LOGGER = ""
try:
    from django.conf import settings
    LOGGER = getattr(settings, 'AXES_LOGGER', 'axes.watch_login')
except ImportError:
    pass

VERSION = (1, 2, 4, 'rc2')


def get_version():
    return '%s.%s.%s-%s' % VERSION

try:
    LOGFILE = os.path.join(settings.DIRNAME, 'axes.log')
except (ImportError, AttributeError):
    # if we have any problems, we most likely don't have a settings module
    # loaded
    pass
else:
    log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=LOGFILE,
                        filemode='w')

    fileLog = logging.FileHandler(LOGFILE, 'w')
    fileLog.setLevel(logging.DEBUG)

    # set a format which is simpler for console use
    console_format = '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s'
    formatter = logging.Formatter(console_format)

    # tell the handler to use this format
    fileLog.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger(LOGGER).addHandler(fileLog)
