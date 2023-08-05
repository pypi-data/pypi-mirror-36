from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules = [
    Extension("sha256prng", ["sha256prng.pyx"],
    include_dirs=[numpy.get_include()])
]

setup(
  name = 'SHA-256 PRNG',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
  include_dirs=[numpy.get_include()]
)