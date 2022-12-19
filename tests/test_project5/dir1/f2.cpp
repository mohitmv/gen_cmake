#include "dir1/f2.hpp"

#include <iostream>

#include "dir1/f1.hpp"
#include "dir1/version.hpp"

int dir1_f2() {
  std::cout << "dir1_f2 : version = " << VERSION << std::endl;
  std::cout << "START dir1_f2" << std::endl;
  int o = dir1_f1();
  std::cout << "END dir1_f2" << std::endl;
  return 12 + o;
}
