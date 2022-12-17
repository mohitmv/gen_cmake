#! /usr/bin/env python3

import unittest
import subprocess
import os
import shutil


PROJECT1_MAIN1_OUTPUT = """\
START dir1_main
dir1_f1
START dir1_f2
dir1_f1
END dir1_f2
END dir1_main
"""

PROJECT2_MAIN1_OUTPUT = """\
START dir1_f2
dir1_f1
END dir1_f2
START dir1_f3
START dir1_f2
dir1_f1
END dir1_f2
END dir1_f3
"""

PROJECT2_MAIN2_OUTPUT = """\
START dir1_f2
dir1_f1
END dir1_f2
START dir2_shared_lib
common_stuff
START dir2_f1
dir1_f1
END dir2_f1
dir2_f2
END dir2_shared_lib
"""

PROJECT3_MAIN1_OUTPUT = """\
START dir1_main
dir1_f1: PUBLIC_F1_FLAG = 5
dir1_f1: PRIVATE_F1_FLAG = 8
START dir1_f2
dir1_f1: PUBLIC_F1_FLAG = 5
dir1_f1: PRIVATE_F1_FLAG = 8
dir1_f2: PUBLIC_F1_FLAG = 5
dir1_f2: PRIVATE_F1_FLAG not defined 
dir1_f2: PUBLIC_F2_FLAG = 17
dir1_f2: PRIVATE_F2_FLAG = 18
END dir1_f2
dir1_main1: PUBLIC_F1_FLAG = 5
dir1_main1: PRIVATE_F1_FLAG not defined 
dir1_main1: PUBLIC_F2_FLAG = 17
dir1_main1: PRIVATE_F2_FLAG not defined 
dir1_main1: PUBLIC_MAIN_FLAG = 27
dir1_main1: PRIVATE_MAIN_FLAG = 28
END dir1_main
"""

PROJECT4_MAIN1_OUTPUT = """\
START dir1_main
dir1_f1: libA() = libA
dir1_f1: libB() = libB
START dir1_f2
dir1_f1: libA() = libA
dir1_f1: libB() = libB
END dir1_f2
END dir1_main
"""

def cmdOutput(cmd):
  return subprocess.check_output(cmd, shell=True).decode("utf-8")

def readFile(fn):
  with open(fn) as fd:
    return fd.read()

def writeFile(fn, content):
  with open(fn, 'w') as fd:
    return fd.write(content)

def replaceTargetType(content, target_name, old_type, new_type):
    tmp = content.split(f'"{target_name}"', 1)
    assert len(tmp) == 2
    tmp0 = new_type.join(tmp[0].rsplit(old_type, 1))
    return tmp0 + f'"{target_name}"' + tmp[1]

class TestProject1(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project1")

    def assertClean(self):
        self.assertFalse(os.path.exists(f"{self.PROJECT_DIR}/build"))

    def clean(self):
        if os.path.isdir(f"{self.PROJECT_DIR}/build"):
            shutil.rmtree(f"{self.PROJECT_DIR}/build")

    def setUp(self):
        self.clean()

    def tearDown(self):
        self.clean()
        return

    def test_main(self):
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir1_main1"), PROJECT1_MAIN1_OUTPUT)


class TestProject2(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project2")
    build_files = ["dir1/BUILD", "dir2/BUILD", "dir_main/BUILD", "common/BUILD"]

    def assertClean(self):
        for build_file in self.build_files:
            self.assertFalse(os.path.exists(f"{self.PROJECT_DIR}/{build_file}"))
        self.assertFalse(os.path.exists(f"{self.PROJECT_DIR}/build"))

    def assertExists(self):
        for build_file in self.build_files:
            self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/{build_file}"))

    def clean(self):
        for build_file in self.build_files:
            if os.path.isfile(f"{self.PROJECT_DIR}/{build_file}"):
                os.remove(f"{self.PROJECT_DIR}/{build_file}")
        if os.path.isdir(f"{self.PROJECT_DIR}/build"):
            shutil.rmtree(f"{self.PROJECT_DIR}/build")

    def setUp(self):
        self.clean()
        return

    def tearDown(self):
        self.clean()
        return

    def test_main(self):
        self.assertClean()
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        self.assertExists()
        content1 = readFile(f"{self.PROJECT_DIR}/dir_main/BUILD").replace("CppSource", "CppExecutable")
        content2 = readFile(f"{self.PROJECT_DIR}/dir2/BUILD")
        content2 = replaceTargetType(content2, "shared_lib", "CppSource", "CppSharedLib")
        writeFile(f"{self.PROJECT_DIR}/dir_main/BUILD", content1)
        writeFile(f"{self.PROJECT_DIR}/dir2/BUILD", content2)
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        self.assertEqual(readFile(f"{self.PROJECT_DIR}/dir_main/BUILD"), content1)
        self.assertEqual(readFile(f"{self.PROJECT_DIR}/dir2/BUILD"), content2)
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py . --gen_cmake") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir_main_main1"), PROJECT2_MAIN1_OUTPUT)
        self.assertEqual(cmdOutput("./dir_main_main2"), PROJECT2_MAIN2_OUTPUT)


class TestProject3(unittest.TestCase):
    build_files = ["dir1/BUILD"]
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project3")

    def assertClean(self):
        self.assertFalse(os.path.exists(f"{self.PROJECT_DIR}/build"))

    def assertExists(self):
        for build_file in self.build_files:
            self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/{build_file}"))

    def clean(self):
        if os.path.isdir(f"{self.PROJECT_DIR}/build"):
            shutil.rmtree(f"{self.PROJECT_DIR}/build")

    def setUp(self):
        self.clean()
        return

    def tearDown(self):
        self.clean()
        return

    def test_main(self):
        self.assertClean()
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        self.assertExists()
        content2 = readFile(f"{self.PROJECT_DIR}/dir1/BUILD")
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        self.assertEqual(readFile(f"{self.PROJECT_DIR}/dir1/BUILD"), content2)
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py . --gen_cmake") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir1_main1"), PROJECT3_MAIN1_OUTPUT)

def makeToolchain(path, libs_map):
    for lib, (hdr, src) in libs_map.items():
        lib_path = f"{path}/{lib}"
        os.makedirs(f"{lib_path}/include/{lib}", exist_ok=True)
        os.makedirs(f"{lib_path}/lib64/", exist_ok=True)
        writeFile(f"{lib_path}/include/{lib}/{lib}.hpp", hdr)
        writeFile(f"{lib_path}/lib64/main.cpp", src)
        os.system(f"g++ -c {lib_path}/lib64/main.cpp -o {lib_path}/lib64/{lib}.o")

class TestProject4(unittest.TestCase):
    build_files = ["dir1/BUILD"]
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project4")
    TOOLCHAIN_PATH = "/tmp/toolchain/depg_test_project4"

    def assertClean(self):
        self.assertFalse(os.path.exists(f"{self.PROJECT_DIR}/build"))

    def assertExists(self):
        for build_file in self.build_files:
            self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/{build_file}"))

    def clean(self):
        if os.path.isdir(f"{self.PROJECT_DIR}/build"):
            shutil.rmtree(f"{self.PROJECT_DIR}/build")
        if os.path.isdir(self.TOOLCHAIN_PATH):
            shutil.rmtree(self.TOOLCHAIN_PATH)

    def setUp(self):
        self.clean()
        return

    def tearDown(self):
        return
        self.clean()

    def test_main(self):
        self.assertClean()
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        makeToolchain(self.TOOLCHAIN_PATH, {
            "libA": ("const char* libA();",
                     'const char* libA() { return "libA";}'),
            "libB": ('#include "libA/libA.hpp"\nconst char* libB();',
                     'const char* libB() { return "libB";}'),
            })
        self.assertExists()
        content2 = readFile(f"{self.PROJECT_DIR}/dir1/BUILD")
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py .") == 0)
        self.assertEqual(readFile(f"{self.PROJECT_DIR}/dir1/BUILD"), content2)
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/depg_main.py . --gen_cmake --toolchain {self.TOOLCHAIN_PATH}") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir1_main1"), PROJECT4_MAIN1_OUTPUT)


if __name__ == '__main__':
    unittest.main()
