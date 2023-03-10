#! /usr/bin/env python3

# Author: Mohit Saini (mohitsaini1196@gmail.com)

"""
Usage:
./tools/gen_cmake_main.py a/b c --out build
This will create build/CMakeLists.txt file to build given targets.
"""

import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../../.."))

import gen_cmake.gen_cmake_lib_main as gen_cmake_lib_main

def getConfigs():
    configs = gen_cmake_lib_main.getDefaultConfigs()
    configs.TOP_DIRECTORY_LIST = ["dir1"]
    return configs

def getArgs():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        'target_and_dirs', nargs='*', help="List of targets or directories.")
    parser.add_argument("--out", '-o', required=True, dest='output_directory', help="Output  directory. Try using --out=build ")
    return parser.parse_args()

def main():
    source_directory = os.path.abspath(os.path.dirname(__file__) + "/..")
    os.chdir(source_directory)
    args = getArgs()
    configs = getConfigs()
    if len(args.target_and_dirs) == 0:
        args.target_and_dirs.append(".")
    gen_cmake_lib_main.genCmake(source_directory, configs, args.target_and_dirs, args.output_directory)

if __name__ == "__main__":
    main()
