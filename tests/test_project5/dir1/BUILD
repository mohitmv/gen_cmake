#! /usr/bin/env python3

# Semi Auto-generated file ; Don't edit ; Learn more at docs/depg.md

CppSource(
    name = "f2",
    hdrs = [ "f2.hpp" ],
    srcs = [ "f2.cpp" ],
    private_deps = [ ":f1",
                     ":version" ])

CppSource(
    name = "f1",
    hdrs = [ "f1.hpp" ],
    srcs = [ "f1.cpp" ])

CustomTarget(
    name = "version",
    output_files = [ "version.hpp" ],
    always_rebuild = True,
    command = "python3 /tmp/test_project5/gen_version.py")

CppExecutable(
    name = "main2",
    srcs = [ "main2.cpp" ],
    private_deps = [ ":generated_source" ])

CppSource(
    name = "generated_source",
    srcs = [ "generated_source.cpp" ],
    private_deps = [":gen_source"])

CustomTarget(
    name = "gen_source",
    output_files = [ "generated_source.cpp" ],
    input_files = [ "source_template.txt" ],
    command = "python3 /tmp/test_project5/gen_source.py")

CppExecutable(
    name = "main1",
    srcs = [ "main1.cpp" ],
    private_deps = [ ":f1",
                     ":f2" ])

