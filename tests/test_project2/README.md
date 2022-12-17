- Test the use of SharedLib targets and dependencies.

Deps Graph: 

dir1/f1 ; deps = []
dir1/f2 ; deps = [dir1/f1]
dir1/f3 ; deps = [dir1/f2]

dir2/f1 ; deps = [dir1/f1]
dir2/f2 ; deps = []
dir2/shared_lib ; deps = [dir2/f1, dir2/f2]

dir_main/main1 ; deps = [dir1/f2, dir1/f3]
dir_main/main2 ; deps = [dir1/f2, dir2/shared_lib]

