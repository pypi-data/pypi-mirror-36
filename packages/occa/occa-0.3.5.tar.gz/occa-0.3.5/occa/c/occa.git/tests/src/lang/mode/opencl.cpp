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
#define OCCA_TEST_PARSER_TYPE okl::openclParser

#include <occa/lang/mode/opencl.hpp>
#include "../parserUtils.hpp"

#undef parseAndPrintSource
#define parseAndPrintSource(str_)                                       \
  parseSource(str_);                                                    \
  ASSERT_TRUE(parser.success)                                           \
  {                                                                     \
    printer pout;                                                       \
    parser.hostParser.root.print(pout);                                 \
    std::cout << "---[ Host ]-----------------------------------\n";    \
    std::cout << pout.str();                                            \
    std::cout << "==============================================\n\n";  \
    pout.clear();                                                       \
    parser.root.print(pout);                                            \
    std::cout << "---[ Device ]---------------------------------\n";    \
    std::cout << pout.str();                                            \
    std::cout << "==============================================\n\n";  \
  }

void testPragma();
void testLoopExtraction();
void testGlobalConst();
void testKernelAnnotation();
void testKernelArgs();
void testSharedAnnotation();
void testBarriers();
void testSource();

int main(const int argc, const char **argv) {
  parser.settings["okl/validate"] = false;
  testPragma();

  parser.settings["okl/validate"] = true;
  testLoopExtraction();
  testGlobalConst();
  testKernelAnnotation();
  testKernelArgs();
  testSharedAnnotation();
  testBarriers();
  testSource();

  return 0;
}

//---[ Pragma ]-------------------------
void testPragma() {
  parseSource("");
  ASSERT_EQ(1,
            parser.root.size());

  ASSERT_EQ("OPENCL EXTENSION cl_khr_fp64 : enable\n",
            parser.root[0]
            ->to<pragmaStatement>()
            .value());

  parser.settings["opencl/extensions/cl_khr_fp64"] = false;
  parseSource("");
  ASSERT_EQ(0,
            parser.root.size());


  parser.settings["opencl/extensions/foobar"] = true;
  parseSource("");
  ASSERT_EQ(1,
            parser.root.size());

  ASSERT_EQ("OPENCL EXTENSION foobar : enable\n",
            parser.root[0]
            ->to<pragmaStatement>()
            .value());

  parser.settings["opencl/extensions/foobar"] = false;
  parser.settings["opencl/extensions/cl_khr_fp64"] = true;
}
//======================================

//---[ Loops ]--------------------------
void testLoopExtraction() {
  // SPLIT LOOPS!!
}
//======================================

//---[ Constant ]-----------------------
void testGlobalConst() {
  // Global const -> __constant
}
//======================================

//---[ Kernel ]-------------------------
void testKernelAnnotation() {
  // @kernel -> __kernel
}
//======================================

//---[ Kernel Args ]--------------------
void testKernelArgs() {
  // @kernel arg -> __global
}
//======================================

//---[ Shared ]-------------------------
void testSharedAnnotation() {
  // @shared -> __local
}
//======================================

//---[ Barriers ]-----------------------
void testBarriers() {
  // Add barriers barrier(CLK_LOCAL_MEM_FENCE)
}
//======================================

void testSource() {
  // TODO:
  //   @exclusive ->
  //     - std::vector<value>
  //     - vec.reserve(loopIterations)
  //     - Add iterator index to inner-most @inner loop
  parseAndPrintSource(
    "const int var[10];\n"
    "void foo() {}\n"
    "int baz(int i) {}\n"
    "@kernel void kernel(@restrict int * arg, const int bar) {\n"
    "  for (int o1 = 0; o1 < O1; ++o1; @outer) {\n"
    "    for (int o0 = 0; o0 < O0; ++o0; @outer) {\n"
    "      @shared int shr[3];\n"
    "      @exclusive int excl;\n"
    "      if (true) {\n"
    "        for (int i1 = 10; i1 < (I1 + 4); i1 += 3; @inner) {\n"
    "          for (int i0 = 0; i0 < I0; ++i0; @inner) {\n"
    "            for (;;) {\n"
    "               excl = i0;\n"
    "            }\n"
    "            for (;;) {\n"
    "               excl = i0;\n"
    "            }\n"
    "          }\n"
    "        }\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "  for (int o1 = 0; o1 < O1; ++o1; @outer(0)) {\n"
    "    for (int o0 = 0; o0 < O0; ++o0; @outer(1)) {\n"
    "      @shared int shr[3];\n"
    "      @exclusive int excl;\n"
    "      if (true) {\n"
    "        for (int i1 = 10; i1 < (I1 + 4); i1 += 3; @inner(1)) {\n"
    "          for (int i0 = 0; i0 < I0; ++i0; @inner(0)) {\n"
    "            for (;;) {\n"
    "               excl = i0;\n"
    "            }\n"
    "            for (;;) {\n"
    "               excl = i0;\n"
    "            }\n"
    "          }\n"
    "        }\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "  for (int ib = 0; ib < entries; ib += 16; @outer) {\n"
    "    for (int it = 0; it < 16; ++it; @inner) {\n"
    "      const int i = ib + it;\n"
    "      if (i < entries) {\n"
    "        ab[i] = a[i] + b[i];\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "}\n"
  );
  parseAndPrintSource(
    "@kernel void addVectors(const int entries,\n"
    "                        const float *a,\n"
    "                        const float *b,\n"
    "                        float *ab) {\n"
    "  for (int i = 0; i < entries; ++i; @tile(16, @outer, @inner)) {\n"
    "    ab[i] = a[i] + b[i];\n"
    "  }\n"
    "}\n"
  );
  parseAndPrintSource(
    "@kernel void addVectors(const int entries,\n"
    "                        const float *a,\n"
    "                        const float *b,\n"
    "                        float *ab) {\n"
    "  for (int ib = 0; ib < entries; ib += 16; @outer) {\n"
    "    @shared int foo[10];\n"
    "    for (int it = 0; it < 16; ++it; @inner) {\n"
    "      const int i = ib + it;\n"
    "      if (i < entries) {\n"
    "        foo[i] = a[i] + b[i];\n"
    "      }\n"
    "    }\n"
    "    for (int it = 0; it < 16; ++it; @inner) {\n"
    "      const int i = ib + it;\n"
    "      if (i < entries) {\n"
    "        foo[i] = a[i] + b[i];\n"
    "      }\n"
    "    }\n"
    "  }\n"
    "}\n"
  );
}
