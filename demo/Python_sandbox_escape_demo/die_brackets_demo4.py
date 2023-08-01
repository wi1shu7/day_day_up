import enum
from os import system

enum.EnumMeta.__getitem__ = system
enum.Enum['whoami']

import reprlib

reprlib.Repr.__getitem__ = system
reprlib.aRepr['chcp 65001']
reprlib.aRepr['dir']