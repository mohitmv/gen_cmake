#include <iostream>

#include "dir1/f1.hpp"
#include "libB/libB.hpp"

int dir1_f1() {
  std::cout << "dir1_f1: libA() = " << libA() << std::endl;
  std::cout << "dir1_f1: libB() = " << libB() << std::endl;
  return 10;
}
