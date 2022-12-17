#include "dir1/f3.hpp"

#include <iostream>

#include "dir1/f2.hpp"

int dir1_f3() {
  std::cout << "START dir1_f3" << std::endl;
  int o = dir1_f2();
  std::cout << "END dir1_f3" << std::endl;
  return 12 + o;
}
