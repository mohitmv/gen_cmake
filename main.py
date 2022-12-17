#! /usr/bin/env python3

# Author: Mohit Saini (mohitsaini1196@gmail.com)

"""
Usage:
./tools/depg/main.py a/b/c.cpp z/g.hpp
This will update the targets in a/b/BUILD and z/BUILD as per changed files.

Read `tools/depg/README.md` and
     `tools/depg/implementation_details_README.md` to know more about depg.
"""

# pylint: disable=missing-function-docstring,invalid-name,no-else-return
# pylint: disable=unused-import

import argparse
import os

import merge_build_file
import gen_cmake

def getArgs():
    """Return the object with parsed command line arguments."""
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        'paths', nargs='*',
        help="List of changed files/directories in this repo. If a directory "
             "is specified then all files will be considered recursively.")
    parser.add_argument(
        "--output_directory",
        default=".",
        help="Directory where generated BUILD files will be written. "
             "Default: Current directory. A custom directory like '/tmp/abc' "
             "can be used here to only dump the generated BUILD files without "
             "overwriting the existing BUILD files.")
    parser.add_argument("--dont_gen_build", action='store_true', default=False)
    parser.add_argument("--gen_cmake", action='store_true', default=False)
    parser.add_argument("--cmake_build_dir", default="build")
    return parser.parse_args()

def main():
    os.chdir("../ms/ctwik_experimental")
    args = getArgs()
    if not args.dont_gen_build:
        merge_build_file.regenerateBuildFiles(args.paths, args.output_directory)
    if args.gen_cmake:
        gen_cmake.genCmake(args.paths, args.cmake_build_dir)

if __name__ == "__main__":
    main()
