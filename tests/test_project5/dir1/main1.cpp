#include <iostream>

#include "dir1/f1.hpp"
#include "dir1/f2.hpp"

int main() {
  std::cout << "START dir1_main" << std::endl;
  dir1_f1() + dir1_f2();
  std::cout << "END dir1_main" << std::endl;
}
