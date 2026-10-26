"""Persistent shared JSON cache for public demonstration profiles."""
from app.config import CACHE_PATH,CACHE_TTL
def get_or_load(key, loader, now=None):
    raise NotImplementedError('implement shared cache with reuse and expiry')
