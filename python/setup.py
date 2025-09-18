#!/usr/bin/env python

"""
setup.py file for MOODS
"""


from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path
import sys
import os

HERE = Path(__file__).resolve().parent
CORE = (HERE / ".." / "core").resolve()

def _unix_like_flags():
    flags = ["-O3", "-std=c++11", "-fPIC"]
    return flags

def _msvc_flags():
    # minimal flags for MSVC: enable optimization and standard exception handling
    return ["/O2", "/EHsc"]

class BuildExt(build_ext):
    def build_extensions(self):
        ctype = self.compiler.compiler_type
        if ctype == "msvc":
            for ext in self.extensions:
                ext.extra_compile_args = _msvc_flags()
        else:
            for ext in self.extensions:
                ext.extra_compile_args = _unix_like_flags()
        for ext in self.extensions:
            ext.language = "c++"
        super().build_extensions()

common_includes = [str(CORE)]

def ext(name, sources):
    return Extension(
        name,
        sources=[str(CORE / s) for s in sources],
        include_dirs=common_includes,
        language="c++",
    )

tools_mod = ext(
    "MOODS._tools",
    [
        "tools_wrap.cxx",
        "moods_tools.cpp",
        "moods_misc.cpp",
        "match_types.cpp",
    ],
)

scan_mod = ext(
    "MOODS._scan",
    [
        "scan_wrap.cxx",
        "moods_scan.cpp",
        "motif_0.cpp",
        "motif_h.cpp",
        "moods_misc.cpp",
        "scanner.cpp",
        "moods_tools.cpp",
        "match_types.cpp",
    ],
)

parsers_mod = ext(
    "MOODS._parsers",
    [
        "parsers_wrap.cxx",
        "moods_parsers.cpp",
        "moods_misc.cpp",
        "moods_tools.cpp",
        "match_types.cpp",
    ],
)

setup(
    name="MOODS-python",
    version="1.9.4.1",
    description="MOODS: Motif Occurrence Detection Suite",
    packages=["MOODS"],
    ext_modules=[tools_mod, scan_mod, parsers_mod],
    scripts=["scripts/moods-dna.py"],
    cmdclass={"build_ext": BuildExt},
)
