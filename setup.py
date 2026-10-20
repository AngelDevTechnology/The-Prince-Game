from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension(
        "engine.renderer._obj_parser",
        ["engine/renderer/_obj_parser.pyx"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": 3},
    )
)
