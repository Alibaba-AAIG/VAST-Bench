"""Package network defaults and boundary for the RetinaPy task interpreter.

Installed only into /opt/retinapy-venv, never the scaffold's system Python.
The local package API examples need no network except this fixed wheel index.
This is inspectable process configuration, not a tamper-proof security sandbox
or whole-container network isolation.
"""
import os
import socket

INDEX_PORT = 18083
LOCAL_NAMES = {'127.0.0.1', 'localhost', 'pypi.org'}

# Ignore inherited pip configuration and proxy settings in this task venv.
for key in list(os.environ):
    if key.upper().endswith('_PROXY') or key.upper().startswith('PIP_'):
        os.environ.pop(key, None)
os.environ.update({
    'PIP_CONFIG_FILE': os.devnull,
    'PIP_INDEX_URL': 'http://pypi.org:18083/simple',
    'PIP_TRUSTED_HOST': '127.0.0.1 pypi.org localhost',
    'PIP_DISABLE_PIP_VERSION_CHECK': '1',
    'PIP_ONLY_BINARY': ':all:',
})

_getaddrinfo = socket.getaddrinfo
_connect = socket.socket.connect
_connect_ex = socket.socket.connect_ex
_sendto = socket.socket.sendto


def local_address(host, port):
    if isinstance(host, bytes):
        host = host.decode('ascii')
    try:
        valid = host in LOCAL_NAMES and int(port) == INDEX_PORT
    except (ValueError, TypeError):
        valid = False
    if not valid:
        raise OSError('RetinaPy task Python permits network connections only to its local wheel index at 127.0.0.1:18083')
    return '127.0.0.1', INDEX_PORT


def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    host, port = local_address(host, port)
    return _getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


def connect(self, address):
    if self.family in (socket.AF_INET, socket.AF_INET6):
        address = local_address(*address[:2])
    return _connect(self, address)


def connect_ex(self, address):
    if self.family in (socket.AF_INET, socket.AF_INET6):
        address = local_address(*address[:2])
    return _connect_ex(self, address)


def sendto(self, data, *args):
    if self.family in (socket.AF_INET, socket.AF_INET6):
        args = (*args[:-1], local_address(*args[-1][:2]))
    return _sendto(self, data, *args)


socket.getaddrinfo = getaddrinfo
socket.socket.connect = connect
socket.socket.connect_ex = connect_ex
socket.socket.sendto = sendto
