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

#ifndef OCCA_CORE_BASE_HEADER
#define OCCA_CORE_BASE_HEADER

#include <iostream>
#include <vector>

#include <stdint.h>

#include <occa/defines.hpp>
#include <occa/types.hpp>

#if OCCA_SSE
#  include <xmmintrin.h>
#endif

#include <occa/core/device.hpp>
#include <occa/core/kernel.hpp>
#include <occa/core/memory.hpp>
#include <occa/core/stream.hpp>
#include <occa/core/streamTag.hpp>

namespace occa {
  //---[ Device Functions ]-------------
  device host();
  device& getDevice();

  void setDevice(device d);
  void setDevice(const occa::properties &props);

  const occa::properties& deviceProperties();

  void loadKernels(const std::string &library = "");

  void finish();

  void waitFor(streamTag tag);

  double timeBetween(const streamTag &startTag,
                     const streamTag &endTag);

  stream createStream(const occa::properties &props = occa::properties());
  stream getStream();
  void setStream(stream s);

  streamTag tagStream();
  //====================================

  //---[ Kernel Functions ]-------------
  kernel buildKernel(const std::string &filename,
                     const std::string &kernelName,
                     const occa::properties &props = occa::properties());

  kernel buildKernelFromString(const std::string &content,
                               const std::string &kernelName,
                               const occa::properties &props = occa::properties());

  kernel buildKernelFromBinary(const std::string &filename,
                               const std::string &kernelName,
                               const occa::properties &props = occa::properties());
  //====================================

  //---[ Memory Functions ]-------------
  occa::memory malloc(const dim_t bytes,
                      const void *src = NULL,
                      const occa::properties &props = occa::properties());

  void* umalloc(const dim_t bytes,
                const void *src = NULL,
                const occa::properties &props = occa::properties());

  void memcpy(void *dest, const void *src,
              const dim_t bytes,
              const occa::properties &props = properties());

  void memcpy(memory dest, const void *src,
              const dim_t bytes = -1,
              const dim_t offset = 0,
              const occa::properties &props = properties());

  void memcpy(void *dest, memory src,
              const dim_t bytes = -1,
              const dim_t offset = 0,
              const occa::properties &props = properties());

  void memcpy(memory dest, memory src,
              const dim_t bytes = -1,
              const dim_t destOffset = 0,
              const dim_t srcOffset = 0,
              const occa::properties &props = properties());

  void memcpy(void *dest, const void *src,
              const occa::properties &props);

  void memcpy(memory dest, const void *src,
              const occa::properties &props);

  void memcpy(void *dest, memory src,
              const occa::properties &props);

  void memcpy(memory dest, memory src,
              const occa::properties &props);
  //====================================

  //---[ Free Functions ]---------------
  void free(device d);
  void free(stream s);
  void free(kernel k);
  void free(memory m);
  //====================================

  void printModeInfo();
}

#endif
