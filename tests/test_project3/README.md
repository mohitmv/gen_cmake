- Test the use of private_cc_flags and public_cc_flags and how they are
  propogated.


Deps Graph: 

dir1/f1 ; deps = []
dir1/f2 ; deps = [dir1/f1]
dir1/main1 ; deps = [dir1/f2]
