import binascii
import sys
import os
import threading

from cffi import FFI
from cffi.verifier import Verifier


def _create_modulename(cdef_sources, source, sys_version):
    """
    This is the same as CFFI's create modulename except we don't include the
    CFFI version.
    """
    key = '\x00'.join([sys_version[:3], source, cdef_sources])
    key = key.encode('utf-8')
    k1 = hex(binascii.crc32(key[0::2]) & 0xffffffff)
    k1 = k1.lstrip('0x').rstrip('L')
    k2 = hex(binascii.crc32(key[1::2]) & 0xffffffff)
    k2 = k2.lstrip('0').rstrip('L')
    return '_xprintidle_cffi_{0}{1}'.format(k1, k2)

source_file = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'src', "xprintidle.c")

f = open(source_file)
SOURCE = f.read()
CDEF = """
unsigned long idle_time();
"""

ffi = FFI()
ffi.cdef(CDEF)
ffi.verifier = Verifier(
    ffi, SOURCE,
    libraries=['X11', 'Xss'],
    modulename=_create_modulename(CDEF, SOURCE, sys.version),
)


class LazyLibrary(object):
    def __init__(self, ffi):
        self._ffi = ffi
        self._lib = None
        self._lock = threading.Lock()

    def __getattr__(self, name):
        if self._lib is None:
            with self._lock:
                if self._lib is None:
                    self._lib = self._ffi.verifier.load_library()

        return getattr(self._lib, name)


_xprintidle = LazyLibrary(ffi)


def idle_time():
    return _xprintidle.idle_time()
