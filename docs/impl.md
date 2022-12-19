# Implementation Overview

There are two main step:

1. Read build files and computing deps_cover of requested targets.

## 


## CMakeFileGen

The deps cover graph includes mixed set of targets. A C++ target doesn't need to
depend on other target at leaf level if they are hidden behind something, for
example an executable target.

### Simple Case

CppExecutable(A, deps=[B])
CppSource(B, deps=[C, D])
CppSource(C, deps=[D])
CppSource(D, deps=[])

In this case, executable A depends on B, C and D.
Hence, first these file are compiled into objects `A.o`, `B.o`, `C.o`, `D.o` 
which don't depend on each other, hence they can be compiled at the same time.
but the final executable `A` depends on `A.o`, `B.o`, `C.o`, `D.o`, hence it
needs to be linked after compiling all these targets and the linker must
include `A.o`, `B.o`, `C.o`, `D.o`.

### Custom Targets

CppExecutable(A, deps=[B])
CppSource(B, deps=[C, D])
CppSource(C, deps=[D, E])
CppSource(D, deps=[])
CustomTarget(E, deps=[F])
CppExecutable(F, deps=[G])
CppSource(G, deps=[])

In this case, executable A needs to be linked after compiling G.o but it doesn't
need to include G.o for linking. The reason being, target `C` depends on `E`
but that is `CustomTarget`, hence we don't go deeper into that route to find out
C++ objects required for linking `A`.

Here is the general mechanism of deciding when to stop going down into deps
path:

1. When finding overall list of objects for `CppExecutable` or `CppSharedLib` or
   `CppStaticLib` or `CppTest` target, we go into deps, starting from the direct
   deps, and then deps of deps and so on, but:

  - We stop when we encounter `CppSharedLib` or `CppStaticLib` in deps somewhere
    (i.e. we don't go into their `deps` further), but include these targets in
    linking.

  - We continue going deeper when we encounter `CppSource` or `ProtoLibrary`
    targets, and include the `cpp_targets` fields exported by these targets.

  - We should not encounter a `CppTest` target.

  - We stop when we encounter `CustomTarget` (i.e. we don't go further into
    their deps), but we add a dependency from main target to this CustomTarget.
    We do the same when we encounter a `CppExecutable` or any other unknown
    target.

2. When finding overall list of targets to depend on for `CppSource` target, we
   go into deps, starting from the direct deps, and then their public deps, so
   on but:

  - We stop when we encounter `CustomTarget` (i.e. we don't go further into
    their deps), but we add a dependency from main target to this CustomTarget.

  - We continue going deeper when we encounter `CppSource` or `ProtoLibrary`
    targets. In case of `ProtoLibrary` targets, we add the dependency on
    `generated_proto_cc_files` fields exported by these `ProtoLibrary`. Note
    that `ProtoLibrary` exports both `generated_proto_cc_files` fields as well
    as `cpp_targets` fields. We only depend on `generated_proto_cc_files`.

  - We ignore when we encounter `CppSharedLib` / `CppStaticLib` /
    `CppExecutable`. We do so, because we know, if this `CppSource` is being
    used in a main executable, these `CppSharedLib` / `CppStaticLib` targets
    will appear in their deps_cover as well, and that main executable need to
    link with those `CppSharedLib` / `CppStaticLib`. The compilation of a
    translation unit (CppSource) doesn't need to depend on compilation of
    `CppSharedLib` / `CppStaticLib` declared in deps.

  - We should not encounter a `CppTest` target.

3. When finding overall list of targets to to depend on for `ProtoLibrary`, we
   go into deps, starting from the direct deps, and then their deps, so on but:

  - We stop when we encounter `CustomTarget` (i.e. we don't go further into
    their deps), but we add a dependency from main target to this CustomTarget.

  - We continue going deeper when we encounter `ProtoLibrary` targets. In case
    of `ProtoLibrary` targets, we add the dependency on thier `x.proto` source
    files.

  - We should not encounter a `CppTest`, `CppExecutable`, `CppSource`,
    `CppStaticLib` or `CppSharedLib` target.

4. When finding overall list of targets to to depend on for `CustomTarget`:

  - We just declare dependency for the direct deps of CustomTarget as well as
    it's `input_files` and create a add_custom_target / add_custom_command based on
    `should_always_rebuild` flag.

