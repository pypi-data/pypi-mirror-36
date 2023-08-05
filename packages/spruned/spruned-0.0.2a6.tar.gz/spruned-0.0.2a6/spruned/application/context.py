from argparse import Namespace
import threading
from pathlib import Path
from typing import Dict
from spruned.application import networks


class Context(dict):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.configfile = kw.get('configfile', 'spruned.conf')
        self.update(
            {
                'configfile': {},
                'args': {},
                'default': {
                    'daemonize': False,
                    'datadir': str(Path.home()) + '/.spruned',
                    'rpcbind': '127.0.0.1',
                    'rpcport': None,
                    'rpcuser': 'rpcuser',
                    'rpcpassword': 'rpcpassword',
                    'network': 'bitcoin.mainnet',
                    'debug': False,
                    'cache_size': 50,
                    'keep_blocks': 200,
                    'proxy': None,
                    'tor': False,
                    'no_dns_seed': False,
                    'max_p2p_connections': None,
                    'add_p2p_peer': [],
                    'no_electrum_peer_discovery': False,
                    'max_electrum_connections': None,
                    'add_electrum_server': [],
                }
            }
        )
        self.load_config()

    def load_config(self):
        values = {
            'i': ['cache_size', 'keep_blocks', 'rpcport'],
            'b': ['daemonize', 'debug']
        }
        import os
        filename = self.datadir + '/' + self.configfile
        if not os.path.exists(filename):
            return
        with open(filename, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.strip().replace(' ', '')
            if not line:
                continue
            k, v = line.split('=')
            if k not in self['default']:
                raise ValueError('Configuration file error: parameter not admitted: %s (%s:%s)' % (line, filename, i))
            if k in values['i']:
                self['configfile'][k] = int(v)
            elif k in values['b']:
                self['configfile'][k] = bool(v)
            else:
                self['configfile'][k] = v

    @property
    def datadir(self):
        if self._get_param('network') != 'bitcoin.mainnet':
            return self._get_param('datadir') + '/' + self._get_param('network')
        return self._get_param('datadir')

    @property
    def max_electrum_connections(self):
        """
        pass network default if is not set
        """
        exists = self._get_param('max_electrum_connections')
        return int(exists if exists is not None else self.get_network()['electrum_concurrency'])

    @property
    def debug(self):
        return self._get_param('debug')

    @property
    def keep_blocks(self):
        return int(self._get_param('keep_blocks'))

    @property
    def network(self):
        return self._get_param('network')

    @property
    def rpcbind(self):
        return self._get_param('rpcbind')

    @property
    def rpcport(self):
        return self._get_param('rpcport') or self.get_network().get('rpc_port')

    @property
    def rpcuser(self):
        return self._get_param('rpcuser')

    @property
    def rpcpassword(self):
        return self._get_param('rpcpassword')

    @property
    def daemonize(self):
        return self._get_param('daemonize')

    @property
    def proxy(self):
        return self._get_param('daemonize')

    @property
    def tor(self):
        return self._get_param('daemonize')

    @property
    def cache_size(self):
        return int(self._get_param('cache_size'))

    def load_args(self, args: Namespace):
        self['args'] = {
            'daemonize': args.daemonize,
            'datadir': args.datadir,
            'rpcbind': args.rpcbind,
            'rpcpassword': args.rpcpassword,
            'rpcport': args.rpcport,
            'rpcuser': args.rpcuser,
            'network': args.network,
            'debug': args.debug,
            'cache_size': int(args.cache_size),
            'keep_blocks': int(args.keep_blocks),
            'proxy': args.proxy,
            'tor': args.tor,
            'no_dns_seed': args.no_dns_seed,
            'max_p2p_connections': args.max_p2p_connections,
            'add_p2p_peer': args.add_p2p_peer,
            'no_electrum_peer_discovery': args.no_electrum_peer_discovery,
            'max_electrum_connections': args.max_electrum_connections,
            'add_electrum_server': args.electrum_server

        }
        self.apply_context()

    def _get_param(self, key):
        return self['args'].get(key, None) or \
               self['configfile'].get(key, None) or \
               self['default'].get(key, None)

    def apply_context(self):
        pass

    def get_network(self) -> Dict:
        net, work = self._get_param('network').split('.')
        module = getattr(networks, net)
        return getattr(module, work)


_local = threading.local()
_local.ctx = ctx = Context()
