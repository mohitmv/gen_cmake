#! /usr/bin/env python3

# Semi Auto-generated file ; Don't edit ; Learn more at docs/depg.md

CppSource(
    name = "f1",
    hdrs = [ "f1.hpp" ],
    srcs = [ "f1.cpp" ],
    private_deps = [ "dir1:f1" ])

CppSource(
    name = "f2",
    hdrs = [ "f2.hpp" ],
    srcs = [ "f2.cpp" ],
    private_deps = [ ":f1" ])

CppSharedLib(
    name = "shared_lib",
    hdrs = [ "shared_lib.hpp" ],
    srcs = [ "shared_lib.cpp" ],
    private_deps = [ ":f1",
                     ":f2",
                     "common:common_stuff" ])

