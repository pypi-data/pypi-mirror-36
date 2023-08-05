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

#ifndef OCCA_IO_LOCK_HEADER
#define OCCA_IO_LOCK_HEADER

#include <iostream>

namespace occa {
  class hash_t;

  namespace io {
    class lock_t {
    private:
      mutable std::string lockDir;
      mutable bool isMineCached;
      float staleWarning;
      float staleAge;
      mutable bool released;

    public:
      lock_t();

      lock_t(const hash_t &hash,
             const std::string &tag,
             const float staleAge_ = -1);

      ~lock_t();

      bool isInitialized() const;

      const std::string& dir() const;

      void release() const;

      bool isMine();

      bool isReleased();
    };
  }
}

#endif
