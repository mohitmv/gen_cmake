#! /usr/bin/env python3

# Semi Auto-generated file ; Don't edit ; Learn more at docs/depg.md

CppSource(
    name = "f1",
    hdrs = [ "f1.hpp" ],
    srcs = [ "f1.cpp" ],
    private_deps = [ "third_party:libB" ])

CppSource(
    name = "f2",
    hdrs = [ "f2.hpp" ],
    srcs = [ "f2.cpp" ],
    private_deps = [ ":f1" ])

CppExecutable(
    name = "main1",
    srcs = [ "main1.cpp" ],
    private_deps = [ ":f1",
                     ":f2" ])

