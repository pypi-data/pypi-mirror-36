/* The MIT License (MIT)
 *
 * Copyright (c) 2014-2018 David Medina and Tim Warburton
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 */

#ifndef OCCA_DEFINES_OS_HEADER
#define OCCA_DEFINES_OS_HEADER

#include <occa/defines/compiledDefines.hpp>

#ifndef OCCA_USING_VS
#  ifdef _MSC_VER
#    define OCCA_USING_VS 1
#    define OCCA_OS OCCA_WINDOWS_OS
#  else
#    define OCCA_USING_VS 0
#  endif
#endif

#ifndef OCCA_OS
#  if defined(WIN32) || defined(WIN64)
#    if OCCA_USING_VS
#      define OCCA_OS OCCA_WINDOWS_OS
#    else
#      define OCCA_OS OCCA_WINUX_OS
#    endif
#  elif __APPLE__
#    define OCCA_OS OCCA_MACOS_OS
#  else
#    define OCCA_OS OCCA_LINUX_OS
#  endif
#endif

#endif
