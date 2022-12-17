#include <iostream>
#include "dir1/f1.hpp"

int dir1_f1() {

#if defined(PUBLIC_F1_FLAG)
  std::cout << "dir1_f1: PUBLIC_F1_FLAG = " << PUBLIC_F1_FLAG << std::endl;
#else
  std::cout << "dir1_f1: PUBLIC_F1_FLAG not defined " << std::endl;
#endif

#if defined(PRIVATE_F1_FLAG)
  std::cout << "dir1_f1: PRIVATE_F1_FLAG = " << PRIVATE_F1_FLAG << std::endl;
#else
  std::cout << "dir1_f1: PRIVATE_F1_FLAG not defined " << std::endl;
#endif

  return 10;
}
