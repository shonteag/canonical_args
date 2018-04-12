"""
Provides decorators and utilities for interfacing
``canonical_args`` with python methods.
"""
from __future__ import absolute_import

import functools

from . import structure



def arg_spec(spec):
	"""
	Decorates a method, and checks args against
	registry.

	:param spec: the structure to use when checking args. if
		of type ``str``, will assume it is a file, and load it.
	:type spec: ``dict`` or ``str``
	"""
	if isinstance(spec, str) or isinstance(spec, unicode):
		with open(spec) as f:
			spec = json.load(f)

	def inner(func):
		@functools.wraps(func)
		def _inner(*args, **kwargs):
			structure.check_args(spec, args, kwargs)
			return func(*args, **kwargs)
		return _inner
	return inner
