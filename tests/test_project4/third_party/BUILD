#! /usr/bin/env python3

# DO_NOT_AUTO_GENERATE_THIS_BUILD_FILE

toolchain_root = "/tmp/toolchain/depg_test_project4"
toolchain_local = toolchain_root + '/local'
toolchain_lib = toolchain_local + '/lib'

########### Declaration of C++ Third Party Library Starts Here ###############

CppSource(
    name = 'libA',
    header_prefix = ['libA/'],
    public_include_paths = [ f'{toolchain_root}/libA/include' ],
    library = [ f'{toolchain_root}/libA/lib64/libA.o' ])


CppSource(
    name = 'libB',
    header_prefix = ['libB/'],
    public_include_paths = [ f'{toolchain_root}/libB/include' ],
    library = [ f'{toolchain_root}/libB/lib64/libB.o' ],
    public_deps = [ ':libA' ])

