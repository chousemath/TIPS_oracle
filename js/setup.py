from typing import List
from distutils.core import setup
from Cython.Build import cythonize

mods: List[str] = [
    'cparse_pages_list.pyx',
    'cparse_pages_list_mpark.pyx',
    'cparse_pages_list_aj.pyx',
    'cparse_pages_list_encar_domestic.pyx',
    'cparse_pages_list_autoinside.pyx',
    'cparse_pages_detail_autoinside.pyx',
    'cdecompose.pyx',
]
for mod in mods:
    setup(ext_modules=cythonize(
        mod, compiler_directives={'language_level': '3'}))
