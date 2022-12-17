#! /usr/bin/env python3

# Semi Auto-generated file ; Don't edit ; Learn more at docs/depg.md

CppSource(
    name = "f1",
    hdrs = [ "f1.hpp" ],
    srcs = [ "f1.cpp" ],
    private_cc_flags = [ "-DPRIVATE_F1_FLAG=8" ],
    public_cc_flags = [ "-DPUBLIC_F1_FLAG=5" ])

CppSource(
    name = "f2",
    hdrs = [ "f2.hpp" ],
    srcs = [ "f2.cpp" ],
    private_deps = [ ":f1" ],
    private_cc_flags = [ "-DPRIVATE_F2_FLAG=18" ],
    public_cc_flags = [ "-DPUBLIC_F2_FLAG=17" ])

CppExecutable(
    name = "main1",
    srcs = [ "main1.cpp" ],
    private_deps = [ ":f1",
                     ":f2" ],
    private_cc_flags = [ "-DPRIVATE_MAIN_FLAG=28" ],
    public_cc_flags = [ "-DPUBLIC_MAIN_FLAG=27" ])

