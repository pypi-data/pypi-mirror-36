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

#include <occa/defines.hpp>

#if OCCA_CUDA_ENABLED
#  ifndef OCCA_MODES_CUDA_REGISTRATION_HEADER
#  define OCCA_MODES_CUDA_REGISTRATION_HEADER

#include <occa/mode.hpp>
#include <occa/mode/cuda/device.hpp>
#include <occa/mode/cuda/kernel.hpp>
#include <occa/mode/cuda/memory.hpp>
#include <occa/tools/styling.hpp>
#include <occa/core/base.hpp>

namespace occa {
  namespace cuda {
    class modeInfo : public modeInfo_v {
    public:
      modeInfo();

      bool init();
      styling::section& getDescription();
    };

    extern occa::mode<cuda::modeInfo,
                      cuda::device> mode;
  }
}

#  endif
#endif
