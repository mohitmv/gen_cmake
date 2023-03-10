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

PROJECT5_MAIN1_OUTPUT_START = """\
START dir1_main
dir1_f1
dir1_f2 : version = """

PROJECT5_MAIN1_OUTPUT_END = """\
START dir1_f2
dir1_f1
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


def deleteIfExists(path):
    if os.path.exists(path):
        shutil.rmtree(path)


class TestProject1(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project1")

    def setUp(self):
        deleteIfExists(f"{self.PROJECT_DIR}/build")

    def test_main(self):
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir1_main1"), PROJECT1_MAIN1_OUTPUT)


class TestProject2(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project2")

    def setUp(self):
        deleteIfExists(f"{self.PROJECT_DIR}/build")

    def test_main(self):
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir_main_main1"), PROJECT2_MAIN1_OUTPUT)
        self.assertEqual(cmdOutput("./dir_main_main2"), PROJECT2_MAIN2_OUTPUT)


class TestProject3(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project3")

    def setUp(self):
        deleteIfExists(f"{self.PROJECT_DIR}/build")

    def test_main(self):
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
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
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project4")
    TOOLCHAIN_PATH = "/tmp/toolchain/depg_test_project4"

    def setUp(self):
        deleteIfExists(f"{self.PROJECT_DIR}/build")
        deleteIfExists(self.TOOLCHAIN_PATH)

    def test_main(self):
        makeToolchain(self.TOOLCHAIN_PATH, {
            "libA": ("const char* libA();",
                     'const char* libA() { return "libA";}'),
            "libB": ('#include "libA/libA.hpp"\nconst char* libB();',
                     'const char* libB() { return "libB";}'),
            })
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        self.assertEqual(cmdOutput("./dir1_main1"), PROJECT4_MAIN1_OUTPUT)



directory = "/home/mohit/projects/gen_cmake/tests/test_project5/dir1"

TestProject5_GEN_SOURCE = """
with open(f"{directory}/generated_source.cpp", 'w') as fd:
  content = open(f"{directory}/source_template.txt").read()
  fd.write(content.replace("PARAM_OUTPUT", "25"))
"""

class TestProject5(unittest.TestCase):
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/test_project5")

    def setUp(self):
        deleteIfExists(f"{self.PROJECT_DIR}/build")
        gen_version_content = ("import time\n"
            "version = int(1000000000 * time.time())\n"
            f"with open('{self.PROJECT_DIR}/dir1/version.hpp', 'w') as fd:\n"
            "  fd.write(f'#define VERSION {version}L\\n')\n")
        os.makedirs("/tmp/test_project5/", exist_ok=True)
        writeFile("/tmp/test_project5/gen_version.py", gen_version_content)
        self.gen_source_code = (f'directory = "{self.PROJECT_DIR}/dir1"'
             + TestProject5_GEN_SOURCE)
        writeFile("/tmp/test_project5/gen_source.py", self.gen_source_code)
        self.source_txt_file = f"{self.PROJECT_DIR}/dir1/source_template.txt"
        self.original_source_template = readFile(self.source_txt_file)

    def tearDown(self):
        writeFile(self.source_txt_file, self.original_source_template)


    def test_main(self):
        self.assertTrue(os.system(f"{self.PROJECT_DIR}/tools/gen_cmake_main.py --out build") == 0)
        self.assertTrue(os.path.isfile(f"{self.PROJECT_DIR}/build/CMakeLists.txt"))
        os.chdir(f"{self.PROJECT_DIR}/build")
        self.assertTrue(os.system("cmake . && make") == 0)
        result = cmdOutput("./dir1_main1")
        self.assertTrue(result.startswith(PROJECT5_MAIN1_OUTPUT_START))
        self.assertTrue(result.endswith(PROJECT5_MAIN1_OUTPUT_END))
        result2 = cmdOutput("./dir1_main1")
        self.assertEqual(result, result2)
        self.assertTrue(os.system("cmake . && make") == 0)
        result3 = cmdOutput("./dir1_main1")
        self.assertTrue(result3.startswith(PROJECT5_MAIN1_OUTPUT_START))
        self.assertTrue(result3.endswith(PROJECT5_MAIN1_OUTPUT_END))
        self.assertTrue(result2 != result3)
        result3 = cmdOutput("./dir1_main2")
        self.assertEqual(result3, "source_template() = 43\n")
        dir1_main2_time1 = os.path.getctime("dir1_main2")
        self.assertTrue(os.system("cmake . && make") == 0)
        dir1_main2_time2 = os.path.getctime("dir1_main2")
        self.assertEqual(dir1_main2_time1, dir1_main2_time2)
        result3 = cmdOutput("./dir1_main2")
        self.assertEqual(result3, "source_template() = 43\n")
        writeFile(self.source_txt_file,
                self.original_source_template.replace("18", "17"))
        self.assertTrue(os.system("cmake . && make") == 0)
        result3 = cmdOutput("./dir1_main2")
        self.assertEqual(result3, "source_template() = 42\n")
        self.assertTrue(os.system("cmake . && make") == 0)
        result3 = cmdOutput("./dir1_main2")
        self.assertEqual(result3, "source_template() = 42\n")


if __name__ == '__main__':
    unittest.main()
