#include <iostream>
#include "dir2/f1.hpp"
#include "f2.hpp"  // test relative import.
#include "common_stuff.h"

int dir2_shared_lib() {
  std::cout << "START dir2_shared_lib" << std::endl;
  common_stuff();
  dir2_f1();
  dir2_f2();
  std::cout << "END dir2_shared_lib" << std::endl;
  return 10;
}
