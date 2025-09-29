import subprocess

from setuptools import setup, Extension

try:
    pandoc = subprocess.Popen(['pandoc', 'README.md', '--to', 'rst'],
                              stdout=subprocess.PIPE)
    readme = pandoc.communicate()[0].decode()

except OSError:
    with open('README.md') as f:
        readme = f.read()

cmdclass = {}

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'

try:
    import numpy
except ImportError:
    exit('Install numpy before installing pharminv.')

extensions = [Extension('harminv.charminv',
                        ["harminv/charminv" + ext],
                        include_dirs=[numpy.get_include(), "."],
                        libraries=['harminv'],
                        )]

if USE_CYTHON:
    extensions = cythonize(extensions, include_path=["harminv"])
    from Cython.Distutils import build_ext
    cmdclass.update(build_ext=build_ext)

setup(
    packages=['harminv'],
    cmdclass=cmdclass,
    ext_modules=extensions
)
