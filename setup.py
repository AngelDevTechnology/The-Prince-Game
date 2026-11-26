# ============================================================
# IMPORTS
# ============================================================

from Cython.Build import cythonize
from setuptools import Extension, setup

# ============================================================
# EXTENSION CONFIGURATION
# ============================================================

extensions = [
    Extension(
        name="engine.medieval_court.renderer._obj_parser",
        sources=["engine/medieval_court/renderer/_obj_parser.pyx"],
    )
]


# ============================================================
# PACKAGE BUILD CONFIGURATION
# ============================================================

setup(
    name="the-prince-game",

    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": 3,
        },
        annotate=False,
    ),
)
