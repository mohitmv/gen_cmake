#include <iostream>

#include "dir1/f1.hpp"
#include "dir1/f2.hpp"

int main() {
  std::cout << "START dir1_main" << std::endl;
  dir1_f1() + dir1_f2();

#if defined(PUBLIC_F1_FLAG)
  std::cout << "dir1_main1: PUBLIC_F1_FLAG = " << PUBLIC_F1_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PUBLIC_F1_FLAG not defined " << std::endl;
#endif

#if defined(PRIVATE_F1_FLAG)
  std::cout << "dir1_main1: PRIVATE_F1_FLAG = " << PRIVATE_F1_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PRIVATE_F1_FLAG not defined " << std::endl;
#endif

#if defined(PUBLIC_F2_FLAG)
  std::cout << "dir1_main1: PUBLIC_F2_FLAG = " << PUBLIC_F2_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PUBLIC_F2_FLAG not defined " << std::endl;
#endif

#if defined(PRIVATE_F2_FLAG)
  std::cout << "dir1_main1: PRIVATE_F2_FLAG = " << PRIVATE_F2_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PRIVATE_F2_FLAG not defined " << std::endl;
#endif

#if defined(PUBLIC_MAIN_FLAG)
  std::cout << "dir1_main1: PUBLIC_MAIN_FLAG = " << PUBLIC_MAIN_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PUBLIC_MAIN_FLAG not defined " << std::endl;
#endif

#if defined(PRIVATE_MAIN_FLAG)
  std::cout << "dir1_main1: PRIVATE_MAIN_FLAG = " << PRIVATE_MAIN_FLAG << std::endl;
#else
  std::cout << "dir1_main1: PRIVATE_MAIN_FLAG not defined " << std::endl;
#endif

  std::cout << "END dir1_main" << std::endl;
}
