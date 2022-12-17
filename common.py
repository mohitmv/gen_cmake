#! /usr/bin/env python3

# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=invalid-name

import os
import hashlib

def toRelativePaths(paths):
    for path in paths:
        yield os.path.relpath(path)

def assertRelativePaths(paths):
    for path in paths:
        assert os.path.relpath(path) == path, "Path %s is not relative" % path

def trimExtensions(value, extensions):
    assert isinstance(extensions, tuple)
    for x in extensions:
        if value.endswith(x):
            return value[:-len(x)]
    assert False, value + " doesn't match with extensions: " + str(extensions)
    return None

def trimExtension(value, extension):
    assert value.endswith(extension)
    return value[:-len(extension)]

def hasExtensions(value, extensions):
    assert isinstance(extensions, tuple)
    for x in extensions:
        if value.endswith(x):
            return True
    return False

def assertFileExists(file, configs, msg=''):
    if file in configs.IGNORE_EXISTANCE:
        return
    assert os.path.isfile(file), msg

def readFile(file):
    with open(file, encoding="utf-8", errors="ignore") as fd:
        return fd.read()

def writeFile(file, data, mode='w'):
    with open(file, mode, encoding="utf-8") as fd:
        return fd.write(data)

def getFileCheckSum(file):
    assert (os.path.isfile(file)), ("File %s doesn't exists." % file)
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
