import chalk
import os
import sys


PID_DIR = os.path.dirname(os.path.abspath(__file__))

SHARE_PATH = os.path.join(
    os.path.dirname(sys.executable),
    'share/neji'
)


def getPidPath(options):
    """returns The default location of the pid file for process management"""
    return '%s/%s_%s.pid' % (
        PID_DIR, options['port'], options['app'].replace('.', '_')
    )


def responseInColor(request, prefix='Response', opts=None):
    "Prints the response info in color"
    message = '%s [%s] => Request %s %s %s on pid %d' % (
        prefix,
        request.code,
        str(request.host),
        request.method,
        request.path,
        os.getpid()
    )
    signal = int(request.code)/100
    if signal == 2:
        chalk.green(message, opts=opts)
    elif signal == 3:
        chalk.blue(message, opts=opts)
    else:
        chalk.red(message, opts=opts)
