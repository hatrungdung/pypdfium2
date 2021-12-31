#! /usr/bin/env python3
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

import os
import platform
import build_pdfium
from setup_base import *


class bdist (BDistBase):
    def finalize_options(self):
        BDistBase.finalize_options(self)
        plat_name = f"{platform.system()}_{platform.machine()}".lower()
        plat_name = plat_name.replace('-','_').replace('.','_')
        self.plat_name = plat_name


def lib_setup(libname):
    setuptools.setup(
        cmdclass = {'bdist_wheel': bdist},
        package_data = {'': [libname]},
    )


def get_binary():
    libpath = build_pdfium.find_lib(build_pdfium.OutputDir)
    return os.path.basename(libpath)


def main():
    libname = get_binary()
    build(lambda: lib_setup(libname), build_pdfium.OutputDir)
    binary_path = join(SourceTree, 'src', 'pypdfium2', libname)
    os.remove(binary_path)


if __name__ == '__main__':
    main()
