#! /usr/bin/env bash
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

rm -r dist
rm -r data/*
touch data/.gitkeep
rm -r src/pypdfium2.egg-info/
rm -r __pycache__
rm -r src/pypdfium2/__pycache__