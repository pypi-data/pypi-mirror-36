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

#define OCCA_TEST_PARSER_TYPE okl::openmpParser

#include <occa/lang/mode/openmp.hpp>
#include "../parserUtils.hpp"

void testPragma();

int main(const int argc, const char **argv) {
  parser.settings["okl/validate"] = false;
  parser.settings["serial/include-std"] = false;

  // testPragma();

  return 0;
}

//---[ Pragma ]-------------------------
void testPragma() {
  // @outer -> #pragma omp
  parseSource(
    "@kernel void foo() {\n"
    "  for (;;; @outer) {}\n"
    "}"
  );

  ASSERT_EQ(1,
            parser.root.size());

  functionDeclStatement &foo = parser.root[0]->to<functionDeclStatement>();
  ASSERT_EQ(2,
            foo.size());

  pragmaStatement &ompPragma = foo[0]->to<pragmaStatement>();
  ASSERT_EQ("omp parallel for",
            ompPragma.value());
}
//======================================
