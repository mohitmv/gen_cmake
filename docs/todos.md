## TODOs

13. [P0] Add support for resolving {args}, {configs} and {params} in BUILD files... in any of the string, using python's f-string.

11. [P0] Figure out how i will handle copy-target at different path. May be support also_install_at = ["{args.build_dir}/bin", "{args.gcab_install_dir}"]

9. [P1] Add support and unit tests for target level link flags.

1. [P2] Add support for passing the BUILD file topmost comment via config params.

2. [P2] Add support for passing cmake topmost stuff (version and project name) via config params.

3. [P2] Add support for proto_library,

12. [P2] Use relative paths in CMakeLists.txt file and stop creating symlinks.



## Dones

3. [Done] Respect the INCLUDE_PATHs while auto-generating BUILD files because we cannot find headers otherwise anyways.

8. [Done][P0] Test out in a try cmake file, create a dummy target and make it depend on multiple things... (
        https://stackoverflow.com/a/47555485/2145334)

6. [Done][P0] Add support and unit tests for target level ccflags

7. [Done][P0] Test out with cmake `execute_process`, generating CMakeLists.txt and include it in the same script.

11. [Done][P1] Add a unit tests around the usage of third_party BUILD file and targets used in main source.

10. [Done][P2] Add support and unit tests for target level include_paths.

10. [Done][P0] Figure out how to handle custom target produced by scripts and how to make other depend on them. Example version.hpp is dependent on a custom script to run.

12. [Done][P1] Add support for CustomTarget with options like:
                output_files, input_files, private_deps, always_rebuild=False|True

5. [Done][P2] Rename cxx_flags to cc_flags (top level configs)

