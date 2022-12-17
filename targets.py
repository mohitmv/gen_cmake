#! /usr/bin/env python3

# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=missing-class-docstring

import os
from enum import IntEnum

class TargetType(IntEnum):
    CPP_SOURCE = 1 # Any x.cpp file.
    CPP_EXECUTABLE = 2 # One of the deps or source must include `int main(...)`
    CPP_TEST = 3
    CPP_SHARED_LIB = 4
    CPP_STATIC_LIB = 5
    NOP_TARGET = 7
    PROTO_LIBRARY = 8
    GRPC_LIBRARY = 9
    CUSTOM = 10
    def funcName(self):
        return self.name.title().replace("_", "")
