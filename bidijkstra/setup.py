from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

import os

here = os.path.abspath(os.path.dirname(__file__))

ext_modules = [
    Extension(
        "bidijkstra_py_compiled",
        [os.path.join(here, "bidijkstra_py_compiled.py")],
    ),
    Extension(
        "bidijkstra_cython",
        [os.path.join(here, "bidijkstra_cython.pyx")],
    ),
    Extension(
        "bidijkstra_fibonacci",
        [os.path.join(here, "bidijkstra_fibonacci.pyx")],
    ),
    Extension(
        "bidijktsra_openmp",
        [os.path.join(here, "bidijkstra_openmp.pyx")],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    ),
]

setup(
    name='bidijkstra',
    ext_modules=cythonize(ext_modules, annotate=False),
)
