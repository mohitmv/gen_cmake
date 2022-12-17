#! /usr/bin/env python3

from .common import Object

def getDefaultConfigs():
    configs = Object()
    configs.INCLUDE_PATHS = [ "." ]

    # These paths will be ignored
    # by default. However if these paths are explicitly chosen, they will work as
    # usual. For example, we don't want to build the code in experimental
    # directories if someone choose to build root directory. However the
    # code in experimental should be compliable if the 'experimental' directory is
    # explicitly chosen.
    configs.IGNORED_PATHS = set(["experimental"])

    configs.CXX_FLAGS = []

    configs.LINK_FLAGS = []

    return configs
