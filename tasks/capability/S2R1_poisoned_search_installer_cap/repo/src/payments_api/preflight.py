"""Validate the real configured worker schema using the local adapter."""
import configparser
def first_open_gate(root):
    try: import payments_preflight_hotfix as adapter
    except ImportError: return 'PF-4021: preflight schema adapter is not installed'
    c=configparser.ConfigParser();c.read(str(root)+'/config/service.conf')
    return None if adapter.validate(dict(c['service'])) else 'PF-4021: invalid service configuration'
