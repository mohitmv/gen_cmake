import os
import shutil
import collections

from . import common
from . import targets
from . import algorithms
from .default_configs import getDefaultConfigs

from .targets import TargetType

def readBuildFile(filepath, directory=None, file_content=None):
    directory = directory or os.path.dirname(filepath) or "."
    file_content  = file_content or common.readFile(filepath)
    output = collections.OrderedDict()
    def typeFunc(target_type):
        def func(**args):
            args['type'] = target_type
            output[args['name']] = common.Object(args)
        return func
    func_map = {}
    for target_type in targets.TargetType:
        func_map[target_type.funcName()] = typeFunc(target_type)
    locals().update(func_map)
    exec(file_content)
    def expandDep(dep):
        if dep.startswith(":"):
            return directory + "/" + dep[1:]
        else:
            return dep.replace(":", "/")
    for tname, target in output.items():
        for field in ['public_deps', 'private_deps']:
            if field not in target:
                continue
            target[field] = [expandDep(dep) for dep in target[field]]
    return output


def expandTargets(target_names_or_dirs, configs, excluded_input_targets=()):
    """
    Given a list of directories or target names, expand the list by
    translating directories to list of targets in that directory, considering
    all targets recursively in that directory.
    """
    output = utils.OrderedSet()
    common.assertRelativePaths(configs.IGNORED_PATHS)
    excluded = set(common.toRelativePaths(excluded_input_targets))
    excluded |= getAllForbiddenPaths(configs)
    for input_target in target_names_or_dirs:
        input_target = os.path.relpath(input_target)
        if os.path.isdir(input_target):
            files = listDirectoryRecursive(input_target, excluded,
                                           configs.IGNORED_PATHS)
            for file in files:
                target = fileToTarget(file, self.configs)
                if target is not None:
                    output.add(target)
        else:
            target = input_target.replace(":", "/")
            if (target not in excluded) and (input_target not in excluded):
                output.add(target)
    output = list(output)
    return output

def readBuildFileAndFullTargetPaths(build_file):
    output = collections.OrderedDict()
    directory = os.path.dirname(build_file)
    targets = readBuildFile(build_file)
    for tname, target in targets.items():
        for field in ["name", "src"]:
            if field not in target:
                continue
            target[field] = f"{directory}/{target[field]}"
        for field in ["srcs", "hdrs"]:
            if field not in target:
                continue
            target[field] = [f"{directory}/{x}" for x in target[field]]
        for field in ["public_deps", "private_deps"]:
            if field not in target:
                continue
            new_list = []
            for x in target[field]:
                if x.startswith(":"):
                    x = f"{directory}{x}"
                x = x.replace(":", "/")
                new_list.append(x)
            target[field] = new_list
        output[target["name"]] = target
    return output

def getTopLevelForbiddenDirs(configs):
    """
    List of the top level directories (i.e. directly present in git root),
    which are not the source code, hence forbidden for build systems and DepG.
    """
    output = set()
    for i in os.listdir("."):
        if i.startswith("."):
            output.add(i)
            continue
        for j in configs.FORBIDDEN_TOP_LEVEL_DIRS_STARTS_WITH:
            if i.startswith(j):
                output.add(i)
                break
    return output


def getAllForbiddenPaths(configs):
    return (set(common.toRelativePaths(configs.FORBIDDEN_PATHS))
            | getTopLevelForbiddenDirs(configs))


def listBuildFilesRecursive(directory, forbidden_paths, ignored_paths):
    """
    For a given relative path of @directory (w.r.t Git Root),
    list down all the BUILD files in this directory recursively.
    All file paths in the output are also relative w.r.t. Git root.
    Precondition: @directory must exist.

    The directories matching with @forbidden_paths are not visited. No
    forbidden file will be present in output list.

    Similar to @forbidden_paths, the directories matching with @ignored_paths
    are also not visited unless explicitly asked.
    For example let [`a/b`, 'a/c'] are the @ignored_paths but if client query
    listDirectoryRecursive('a/b/q', ...) then all files in directory `a/b/q`
    will be returned even if directory `a/b` was ignored. However if the client
    query `listDirectoryRecursive('a', ...)` then `a/b`, `a/c` won't be visited.

    Note that if [`a/b`, 'a/c'] are the forbidden_paths then result of
    listDirectoryRecursive('a/b/q', ...) will be [].

    Let a path is a valid relative path iff `os.path.relpath(path) == path`

    Preconditions:
    1. @directory is a valid relative path.
    2. @forbidden_paths and @ignored_paths are valid relative paths.

    """
    assert os.path.relpath(directory) == directory
    for i in forbidden_paths:
        if directory.startswith(i):
            return []
    output = []
    for (root, _, _) in os.walk(directory):
        root = os.path.relpath(root)
        if (root in forbidden_paths
                or (root != directory and root in ignored_paths)):
            continue
        build_file = f"{root}/BUILD"
        if os.path.isfile(build_file):
            output.append(build_file)
    return output


def readTargets(target_names_or_dirs, configs):
    build_files_map = {}
    def readBuildFileCached(build_file):
        if build_file not in build_files_map:
            build_files_map[build_file] = readBuildFileAndFullTargetPaths(build_file)
        return build_files_map[build_file]
    target_names = set()
    common.assertRelativePaths(configs.IGNORED_PATHS)
    excluded = set()
    def getTarget(tname, error=''):
        directory = os.path.dirname(tname)
        build_file = f"{directory}/BUILD"
        if not os.path.isfile(build_file):
            assert False, f"File {build_file} not found " + error
        build_file_struct = readBuildFileCached(build_file)
        if tname in build_file_struct:
            return build_file_struct[tname]
        error = f"Target {os.path.basename(tname)} not found in {build_file}" + error
        assert False, error

    for input_target in target_names_or_dirs:
        input_target = os.path.relpath(input_target)
        if os.path.isdir(input_target):
            build_files = listBuildFilesRecursive(input_target, excluded,
                                            configs.IGNORED_PATHS)
            for build_file in build_files:
                build_file_struct = readBuildFileCached(build_file)
                target_names |= set(build_file_struct.keys())
        else:
            target_names.add(input_target.replace(":", "/"))
    def edgeFunc(tname):
        target = getTarget(tname)
        deps = target.get('public_deps', []) + target.get('private_deps', [])
        for dep in deps:
            getTarget(dep, error=f' , used in deps of {tname}')
        return deps
    target_names, cycles = algorithms.topologicalSortedDepsCoverAndCycles(target_names, edgeFunc)
    if len(cycles) > 0:
        print("Found cycles in targets: " + (" -> ".join(cycles[0])))
        exit(1)
    return dict((tname, getTarget(tname)) for tname in target_names)


def mergeListOfList(list_of_list):
    output = []
    [output.extend(x) for x in list_of_list]
    return output


# If any of these targets are founds in deps of a C++ target, we must consider them.
CPP_EXECUTABLE_DEPS_COVER_GO_IN = set([
    TargetType.CPP_SOURCE, TargetType.PROTO_LIBRARY, TargetType.GRPC_LIBRARY,
    TargetType.CPP_SHARED_LIB, TargetType.CPP_STATIC_LIB,
    TargetType.CUSTOM_TARGET])


def combineFields(target_deps_map, target, field):
    output = []
    for tname, dep_target in target_deps_map.items():
        output.extend(dep_target.get(field, []))
    output.extend(target.get(field, []))
    return output


def makeCMakeValuesString(values):
    values_str = ' '.join(values)
    return f'"{values_str}"'


# Implementation overvoew at docs/impl.md
class CMakeFileGen:
    def __init__(self, configs, targets_map):
        self.configs = configs
        self.targets_map = targets_map
        self.cmake_exports = {}
        self.cmake_decl = []

    def makeCMakeDecl(self):
        self.metaDeclaration()
        self.targetsDeclaration()
        return self.cmake_decl

    def metaDeclaration(self):
        """Declare top level stuff like CXX flags etc"""
        if self.configs.INCLUDE_PATHS:
            self.cmake_decl.append(("include_directories", (self.configs.INCLUDE_PATHS)))
        if self.configs.CC_FLAGS:
            joined = makeCMakeValuesString(self.configs.CC_FLAGS)
            self.cmake_decl.append(("set", ["CMAKE_CXX_FLAGS", joined]))

    def targetsDeclaration(self):
        """Declare targets."""
        for _, target in self.targets_map.items():
            if target.type == TargetType.CPP_SOURCE:
                self.handleCppSource(target)
            elif target.type in [TargetType.CPP_EXECUTABLE, TargetType.CPP_TEST]:
                self.handleCppExecutableOrSharedLib(target, is_shared_lib=False)
            elif target.type == TargetType.CPP_SHARED_LIB:
                self.handleCppExecutableOrSharedLib(target, is_shared_lib=True)
            elif target.type in [TargetType.PROTO_LIBRARY, TargetType.GRPC_LIBRARY]:
                self.handleProtoLibrary(target)
            elif target.type == TargetType.CUSTOM_TARGET:
                self.handleCustomTarget(target)
            else:
                assert False, target


    def handleProtoLibrary(self, target):
        self.cmake_exports[target.name] = dict(
            generated_proto_cc_files=[], cpp_targets= [])


    def handleCustomTarget(self, target):
        cmake_tname = target.name.replace("/", "_")
        cmake_export = common.Object(cmake_tname=cmake_tname)
        if target.always_rebuild or "output_files" not in target:
            elms = [cmake_tname]
            if "command" in target:
                elms.append(target.command)
            self.cmake_decl.append(("add_custom_target", elms))
        else:
            elms = ["OUTPUT"]
            elms.extend(target.output_files)
            if "command" in target:
                elms.extend(["COMMAND", target.command])
            self.cmake_decl.append(("add_custom_command", elms))
            elms2 = [cmake_tname, "DEPENDS"] + target.output_files
            self.cmake_decl.append(("add_custom_target", elms2))
        self.cmake_exports[target.name] = cmake_export

    def addCompileOptions(self, cmake_tname, cc_flags):
        if cc_flags:
            self.cmake_decl.append(("target_compile_options",
                    [cmake_tname, "PRIVATE"] + cc_flags))


    def addIncludePaths(self, cmake_tname, include_paths):
        if include_paths:
            self.cmake_decl.append(("target_include_directories",
                    [cmake_tname, "PRIVATE"] + include_paths))

    def handleCppSource(self, target):
        cpp_targets = []
        files = target.get("srcs", []) + target.get("hdrs", [])
        if len(files) > 0:
            cmake_tname = target.name.replace("/", "_")
            elms = [cmake_tname, "OBJECT"]
            elms.extend(files)
            self.cmake_decl.append(("add_library", elms))
            self.handleCppSourceDeps(target, cmake_tname)
            cpp_targets.append(cmake_tname)
        if "library" in target:
            if type(target.library) is str:
                cpp_targets.append(target.library)
            elif type(target.library) is list:
                cpp_targets.extend(target.library)
            else:
                assert False
        self.cmake_exports[target.name] = dict(cpp_targets=cpp_targets)

    def handleCppExecutableOrSharedLib(self, target, is_shared_lib):
        cmake_tname = target["name"].replace("/", "_")
        elms1 = [cmake_tname] + (["SHARED"] if is_shared_lib else [])
        elms1.extend(target.get("srcs", []) + target.get("hdrs", []))
        self.cmake_decl.append(("add_library" if is_shared_lib else "add_executable", elms1))
        self.handleCppSourceDeps(target, cmake_tname)
        self.handleLinkDeps(target, cmake_tname)
        if is_shared_lib:
            cmake_export = dict(cpp_targets=[cmake_tname])
        else:
            cmake_export = dict(cmake_tname=cmake_tname)
        self.cmake_exports[target.name] = cmake_export


    def handleCppSourceDeps(self, target, cmake_tname):
        public_deps_map = self.publicDepsCoverTargetMap(target)
        cc_flags = combineFields(public_deps_map, target, "public_cc_flags") + target.get("private_cc_flags", [])
        include_paths = combineFields(public_deps_map, target, "public_include_paths") + target.get("private_include_paths", [])
        self.addCompileOptions(cmake_tname, cc_flags)
        self.addIncludePaths(cmake_tname, include_paths)
        dep_custom_targets = self.combineExportedFields(
                public_deps_map, "cmake_tname", TargetType.CUSTOM_TARGET)
        output_files = common.JoinList(self.combineExportedFields(
            public_deps_map, "output_files", TargetType.CUSTOM_TARGET))
        self.addCMakeDeps(cmake_tname, dep_custom_targets + output_files)


    def combineExportedFields(self, deps_map, field_name, target_type):
        output = []
        for tname, target in deps_map.items():
            if target.type != target_type:
                continue
            cmake_export = self.cmake_exports[tname]
            if field_name not in cmake_export:
                continue
            output.append(cmake_export[field_name])
        return output


    def handleLinkDeps(self, target, cmake_tname):
        deps_map = self.depsCoverTargetMap(target)
        elms = [cmake_tname]
        for tname, x in deps_map.items():
            cmake_export = self.cmake_exports[tname]
            elms.extend(cmake_export.get("cpp_targets", []))
        link_flags = combineFields(deps_map, target, "link_flags")
        elms.extend(link_flags)
        if len(elms) > 1:
            self.cmake_decl.append(("target_link_libraries", elms))
        cmake_deps = self.combineExportedFields(
            deps_map, "cmake_tname", TargetType.CPP_EXECUTABLE)
        self.addCMakeDeps(cmake_tname, cmake_deps)

    def addCMakeDeps(self, cmake_tname, deps):
        if len(deps) > 0:
            self.cmake_decl.append(("add_dependencies", [cmake_tname] + deps))


    def depsCoverTargetMap(self, target):
        target_names = algorithms.topologicalSortedDepsCover(
                self.filteredAllDeps(target),
                self.cppDepsCoverEdgeFunc)
        return collections.OrderedDict((x, self.targets_map[x]) for x in target_names)

    def publicDepsCoverTargetMap(self, target):
        # Even for public deps, start with all direct deps.
        target_names = algorithms.topologicalSortedDepsCover(
                self.filteredAllDeps(target),
                self.cppPublicDepsCoverEdgeFunc)
        return collections.OrderedDict((x, self.targets_map[x]) for x in target_names)

    def filterDepsInCppDepsCoverPath(self, deps):
        return [dep for dep in deps if self.targets_map[dep].type in CPP_EXECUTABLE_DEPS_COVER_GO_IN]

    def cppPublicDepsCoverEdgeFunc(self, tname):
        target = self.targets_map[tname]
        if target.type in [TargetType.CPP_SHARED_LIB, TargetType.CPP_STATIC_LIB]:
            return []
        deps = target.get("public_deps", [])
        return self.filterDepsInCppDepsCoverPath(deps)

    def filteredAllDeps(self, target):
        deps = target.get("public_deps", []) + target.get("private_deps", [])
        return self.filterDepsInCppDepsCoverPath(deps)

    def cppDepsCoverEdgeFunc(self, tname):
        target = self.targets_map[tname]
        if target.type in [TargetType.CPP_SHARED_LIB, TargetType.CPP_STATIC_LIB]:
            return []
        return self.filteredAllDeps(target)


def unparseCmakeDecl(cmake_decl, project_name="x"):
    output = "cmake_minimum_required(VERSION 3.1)\n"
    output += f"project({project_name})\n"
    for (name, args) in cmake_decl:
        output += f"{name}({' '.join(args)})\n"
    return output

def preprocessConfigs(configs):
    top_dirs = set(os.path.relpath(x) for x in configs.TOP_DIRECTORY_LIST)
    configs.IGNORED_PATHS |= set(i for i in os.listdir(".") if i not in top_dirs)
    return configs

def genCmake(source_directory, configs, targets_n_dirs, cmake_build_dir):
    assert source_directory == os.getcwd(), \
            "Current directory should be source_directory."
    configs = preprocessConfigs(configs)
    targets_map = readTargets(targets_n_dirs, configs)
    cmake_file_gen = CMakeFileGen(configs, targets_map)
    os.makedirs(cmake_build_dir, exist_ok=True)
    cmake_decl = cmake_file_gen.makeCMakeDecl()
    cmake_file_content = unparseCmakeDecl(cmake_decl)
    for top_dir in configs.TOP_DIRECTORY_LIST:
        if os.path.exists(f"{cmake_build_dir}/{top_dir}"):
            os.unlink(f"{cmake_build_dir}/{top_dir}")
        os.symlink(f"../{top_dir}", f"{cmake_build_dir}/{top_dir}")
    common.writeFile(f"{cmake_build_dir}/CMakeLists.txt", cmake_file_content)
