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

#include <cstdio>
#include <cmath>

#include <occa/tools/testing.hpp>

namespace occa {
  namespace test {
    template <>
    bool areEqual<float, float>(const float &a, const float &b) {
      const double diff = (a - b)/(fabs(a) + fabs(b) + 1e-50);
      return (fabs(diff) < 1e-8);
    }
    template <>
    bool areEqual<double, float>(const double &a, const float &b) {
      const double diff = (a - b)/(fabs(a) + fabs(b) + 1e-50);
      return (fabs(diff) < 1e-8);
    }
    template <>
    bool areEqual<float, double>(const float &a, const double &b) {
      const double diff = (a - b)/(fabs(a) + fabs(b) + 1e-50);
      return (fabs(diff) < 1e-8);
    }

    template <>
    bool areEqual<double, double>(const double &a, const double &b) {
      const double diff = (a - b)/(fabs(a) + fabs(b) + 1e-50);
      return (fabs(diff) < 1e-14);
    }

    template <>
    bool areEqual<const char*, const char*>(const char * const &a,
                                            const char * const &b) {
      return (std::string(a) == std::string(b));
    }
  }
}
