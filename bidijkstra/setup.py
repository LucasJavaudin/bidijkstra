from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "bidijkstra_py_compiled",
        ["bidijkstra_py_compiled.py"],
    ),
    Extension(
        "bidijkstra_cython",
        ["bidijkstra_cython.pyx"],
    ),
    Extension(
        "bidijkstra_fibonacci",
        ["bidijkstra_fibonacci.pyx"],
    ),
    Extension(
        "bidijktra_openmp",
        ["bidijktra_openmp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    ),
]

setup(
    name='bidijkstra',
    ext_modules=cythonize(ext_modules, annotate=False),
)
