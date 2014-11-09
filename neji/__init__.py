try:
    import cPickle as pickle
except ImportError:
    import pickle

from .service import Service
from .options import DEFAULT_OPTIONS
from .utils import getPidPath

from os import environ
from socket import AF_INET
from twisted.application.internet import TCPServer, SSLServer
from twisted.internet import reactor

import chalk
import os
import time


__version__ = "0.0.0"
__all__ = ['start', 'stop', 'restart']


def start(resource, options):
    "sets up the desired services and runs the requested action"
    neji = Neji(resource, options=options)
    neji.spinUp(options['fd'])
    chalk.blue(
        'Ready and Listening on port %d...' % options.get('port')
    )
    neji.reactor.run()


def stop(resource, options, sig=9):
    neji = Neji(resource, options=options)
    with open(neji.pid) as pid_file:
        pids = pid_file.readlines()
        for pid in pids:
            try:
                os.kill(int(pid), sig)
            except OSError:
                # OSError raised when it trys to kill the child processes
                pass
    os.remove(neji.pid)


def restart(resource, options, fd=None):
    stop(resource, options)
    time.sleep(1)  # wait a second to ensure the port is closed
    start(resource, options, fd)


class Neji(object):
    """
    HendrixDeploy encapsulates the necessary information needed to deploy
    the HendrixService on a single or multiple processes.
    """

    def __init__(self, resource, options={}, reactor=reactor):
        self.options = DEFAULT_OPTIONS
        self.options.update(options)
        self.reactor = reactor
        self.service = Service(resource, self.options['port'])

        self.servers = []
        for service in self.service.services:
            if isinstance(service, (TCPServer, SSLServer)):
                self.servers.append(service.name)
        # self.is_secure = self.options['key'] and self.options['cert']

    @property
    def pid(self):
        "The default location of the pid file for process management"
        return getPidPath(self.options)

    def getSpawnArgs(self):
        _args = [
            'ng',
            'start',  # action
            '--port', str(self.options['port']),
            '--workers', '0',
            '--fd', pickle.dumps(self.fds),
        ]

        # args/signals
        if self.options['dev']:
            _args.append('--dev')
        return _args

    def spinUp(self, fd=None):
        if fd is None:
            # anything in this block is only run once
            self.service.startService()
            self.launchWorkers()
        else:
            fds = pickle.loads(fd)
            factories = {}
            for name in self.servers:
                factory = self.disownService(name)
                factories[name] = factory
            self.service.startService()
            for name, factory in factories.iteritems():
                self.addSubprocesses(fds, name, factory)

    def launchWorkers(self):
        pids = [str(os.getpid())]  # script pid
        if self.options['workers']:
            # Create a new listening port and several other processes to
            # help out.
            childFDs = {0: 0, 1: 1, 2: 2}
            self.fds = {}
            for name in self.servers:
                port = self.service.getPort(name)
                fd = port.fileno()
                childFDs[fd] = fd
                self.fds[name] = fd
            args = self.getSpawnArgs()
            transports = []
            for i in range(self.options['workers']):
                transport = self.reactor.spawnProcess(
                    None, 'ng', args, childFDs=childFDs, env=environ
                )
                transports.append(transport)
                pids.append(str(transport.pid))
        with open(self.pid, 'w') as pid_file:
            pid_file.write('\n'.join(pids))

    def addSubprocesses(self, fds, name, factory):
        self.reactor.adoptStreamPort(  # outputs port
            fds[name], AF_INET, factory
        )

    def disownService(self, name):
        """
        disowns a service on hendirix by name
        returns a factory for use in the adoptStreamPort part of setting up
        multiple processes
        """
        _service = self.service.getServiceNamed(name)
        _service.disownServiceParent()
        return _service.factory
