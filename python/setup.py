#!/usr/bin/env python

"""
setup.py file for MOODS
"""
from pathlib import Path
from setuptools import setup, Extension
import sys

# repo_root/core relative to this file
CORE_DIR = Path(__file__).resolve().parents[1] / "core"
if not CORE_DIR.exists():
    raise RuntimeError(f"Missing core dir: {CORE_DIR}")

# compiler flags
if sys.platform == "win32":
    cflags = ["/O2", "/EHsc"]                  # MSVC
else:
    cflags = ["-O3", "-std=c++11", "-fPIC"]    # GCC/Clang

common = dict(
    include_dirs=[str(CORE_DIR)],
    extra_compile_args=cflags,
    language="c++",
    swig_opts=["-c++", f"-I{CORE_DIR}", "-outdir", "MOODS"],
)

def ext(name, iface, extra_cpp):
    return Extension(
        name,
        sources=[str(CORE_DIR / iface)] + [str(CORE_DIR / s) for s in extra_cpp],
        **common,
    )

tools_mod = ext(
    "MOODS._tools",
    "tools.i",
    ["moods_tools.cpp", "moods_misc.cpp", "match_types.cpp"],
)

scan_mod = ext(
    "MOODS._scan",
    "scan.i",
    [
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
    "parsers.i",
    ["moods_parsers.cpp", "moods_misc.cpp", "moods_tools.cpp", "match_types.cpp"],
)

readme = Path(__file__).parent / "readme.MD"
long_desc = readme.read_text(encoding="utf-8") if readme.exists() else ""

setup(
    name="MOODS-python",
    version="1.9.4.1",
    description="MOODS: Motif Occurrence Detection Suite",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=["MOODS"],
    ext_modules=[tools_mod, scan_mod, parsers_mod],
    scripts=["scripts/moods-dna.py"],
    classifiers=["Topic :: Scientific/Engineering :: Bio-Informatics"],
    keywords="PWM, PSSM, motif scan",
    zip_safe=False,
)
