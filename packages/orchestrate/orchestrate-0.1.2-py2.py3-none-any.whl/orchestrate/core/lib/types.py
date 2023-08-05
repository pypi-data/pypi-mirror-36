import collections as _collections


def is_sequence(val):
  """
  Returns True iff this is a "list-like" type. Avoids the common error that strings
  are iterable, and handles numpy and protobufs correctly
  """
  return (isinstance(val, _collections.Sequence) and not isinstance(val, str))

def is_mapping(val):
  """
  Returns True iff this is a "dict-like" type
  """
  return isinstance(val, _collections.Mapping)


def is_set(val):
  """
  Returns True iff this is a "set-like" type
  """
  return isinstance(val, (frozenset, set))


def is_string(val):
  """
  Return True iff this is a string
  """
  return isinstance(val, str)

def is_integer(val):
  """
  Return True iff this is an integer
  """
  return (val is not True) and (val is not False) and isinstance(val, int)
