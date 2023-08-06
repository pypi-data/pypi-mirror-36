from urllib.parse import urlparse

from clor import resolve


class StorageError(Exception):
  '''Generic storage error'''


class StorageQueryError(StorageError):
  '''The exception indicates invalid storage query input'''


def createStorage(dsn):
  if not dsn:
    raise ValueError('Empty storage DSN')

  cfg = urlparse(dsn)
  scheme = cfg.scheme.split('+', 1)
  driver = scheme[1].title() if scheme[1:] else 'Storage'
  cls = resolve('.'.join(['chronologer', 'storage', scheme[0], driver]))
  return cls(cfg)

