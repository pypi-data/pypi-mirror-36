from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

# import numpy as np
import os
from glob import glob
from os.path import join

from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

# # This can be loosen probably, though it's fine I think
# min_cython_ver = '0.24.0'
# try:
#     import Cython
#     ver = Cython.__version__
#     _CYTHON_INSTALLED = ver >= LooseVersion(min_cython_ver)
# except ImportError:
#     _CYTHON_INSTALLED = False

# try:
#     if not _CYTHON_INSTALLED:
#         raise ImportError('No supported version of Cython installed.')
#     from Cython.Distutils import build_ext
#     cython = True
# except ImportError:
#     cython = False

# if cython:
#     ext = '.pyx'
#     cmdclass = {'build_ext': build_ext}
# else:
#     ext = '.cpp'
#     cmdclass = {}
#     if not os.path.exists(join("pyworld", "pyworld" + ext)):
#         raise RuntimeError("Cython is required to generate C++ wrapper")


world_src_top = join("lib", "World", "src")
world_sources = glob(join(world_src_top, "*.cpp"))

ext_modules = [
    Extension(
        name="pyworld.pyworld",
        # include_dirs=[np.get_include(), world_src_top],
        include_dirs=[world_src_top],
        sources=[join("pyworld", "pyworld.pyx")] + world_sources,
        language="c++")]

setup(
    name="pyworld",
    ext_modules=ext_modules,
    # cmdclass=cmdclass,
    cmdclass={'build_ext': build_ext},
    version='0.2.5',
    packages=find_packages(),
    setup_requires=[
        'numpy',
    #     'cython>=0.24.0',
    ],
    install_requires=[
        'numpy',
        'cython>=0.24.0',
    ],
    extras_require={
        'test': ['nose'],
        # 'develop': ['cython >= ' + min_cython_ver],
        'sdist': ['numpy', 'cython'],
    },
    author="Pyworld Contributors",
    author_email="jeremycchsu@gmail.com",
    url="https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder",
    description="a Python wrapper for the WORLD vocoder",
    keywords=['vocoder'],
    classifiers=[],
)
