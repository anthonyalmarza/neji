from optparse import make_option, OptionParser
import os

HTTP_PORT = 8000

OPTION_LIST = (
    make_option(
        '--log',
        dest='log',
        type=str,
        default=os.path.join(os.path.dirname(__file__), 'neji.log'),
        help=(
            'file path to where the log files should live '
            '[default: $PYTHON_PATH/lib/.../neji/neji.log]'
        )
    ),
    make_option(
        '--pythonpath',
        help=(
            'A directory to add to the Python path, e.g. '
            '"/home/myproject/path".'
        )
    ),
    make_option(
        '-p', '--port',
        type=int,
        dest='port',
        default=HTTP_PORT,
        help='Enter a port number for the server to serve content.'
    ),
    make_option(
        '-w', '--workers',
        type=int,
        dest='workers',
        default=0,
        help='Number of processes to run'
    ),
    make_option(
        '--fd',
        type=str,
        dest='fd',
        default=None,
        help='DO NOT SET THIS'
    ),
    make_option(
        '--dev',
        dest='dev',
        action='store_true',
        default=False,
        help=(
            'Runs in development mode. Listens for changes in python files in '
            'your python path. Not recommended for use in production.'
        )
    ),
    make_option(
        '--app',
        dest='app',
        type=str,
        default='app',
        help=(
            'absolute dot path import path to your app module containing '
            'the "root" resource. e.g. --app myproject.pkg.myapp - where myapp'
            '.py contains ... root = Resource() ... By default ng will look '
            'for the module "app.py" in your current working directory.'
        )
    ),
)


NejiOptionParser = OptionParser(
    description=(
        'ng is the interface to deploy a neji app. You must provide an action '
        'i.e. either start or stop and can set a number of options (below)'
    ),
    usage='ng start|stop [options]',
    option_list=OPTION_LIST
)


DEFAULT_OPTIONS = vars(NejiOptionParser.parse_args([])[0])
