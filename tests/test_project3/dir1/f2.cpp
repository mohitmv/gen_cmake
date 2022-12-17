#include "dir1/f2.hpp"

#include <iostream>

#include "dir1/f1.hpp"

int dir1_f2() {
  std::cout << "START dir1_f2" << std::endl;
  dir1_f1();

  #if defined(PUBLIC_F1_FLAG)
    std::cout << "dir1_f2: PUBLIC_F1_FLAG = " << PUBLIC_F1_FLAG << std::endl;
  #else
    std::cout << "dir1_f2: PUBLIC_F1_FLAG not defined " << std::endl;
  #endif

  #if defined(PRIVATE_F1_FLAG)
    std::cout << "dir1_f2: PRIVATE_F1_FLAG = " << PRIVATE_F1_FLAG << std::endl;
  #else
    std::cout << "dir1_f2: PRIVATE_F1_FLAG not defined " << std::endl;
  #endif

#if defined(PUBLIC_F2_FLAG)
  std::cout << "dir1_f2: PUBLIC_F2_FLAG = " << PUBLIC_F2_FLAG << std::endl;
#else
  std::cout << "dir1_f2: PUBLIC_F2_FLAG not defined " << std::endl;
#endif

#if defined(PRIVATE_F2_FLAG)
  std::cout << "dir1_f2: PRIVATE_F2_FLAG = " << PRIVATE_F2_FLAG << std::endl;
#else
  std::cout << "dir1_f2: PRIVATE_F2_FLAG not defined " << std::endl;
#endif


  std::cout << "END dir1_f2" << std::endl;
  return 0;
}
