#include <iostream>
#include "dir2/f1.hpp"
#include "dir1/f1.hpp"

int dir2_f1() {
  std::cout << "START dir2_f1" << std::endl;
  dir1_f1();
  std::cout << "END dir2_f1" << std::endl;
  return 10;
}
