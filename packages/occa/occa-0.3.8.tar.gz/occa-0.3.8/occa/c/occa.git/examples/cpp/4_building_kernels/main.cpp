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
#include <iostream>

#include <occa.hpp>

class map {
public:
  occa::kernel kernel;

  map() {}

  void setup(const std::string &inType,
             const std::string &inName,
             const std::string &outType,
             const std::string &outName,
             const std::string &equation) {
    setup(occa::getDevice(),
          inType , inName,
          outType, outName,
          equation);
  }

  void setup(occa::device device,
             const std::string &inType,
             const std::string &inName,
             const std::string &outType,
             const std::string &outName,
             const std::string &equation) {

    std::stringstream ss;

    ss << "@kernel void map(const int entries,\n"
       << "                 const " << inType  << " *red_input ,\n"
       << "                       " << outType << " *red_output) {\n"
       << "  for (int group = 0; group < entries; group += 128; @outer) {\n"
       << "    for (int item = group; item < (group + 128); ++item; @inner) {\n"
       << "      const int n = item;\n\n"

       << "      if (n < entries) {\n"
       << "        const " << inType  << ' ' << inName  << " = red_input[item];\n"
       << "              " << outType << ' ' << outName << ";\n"
       << "        " << equation << '\n'
       << "        red_output[item] = " << outName << ";\n"
       << "      }\n"
       << "    }\n"
       << "  }\n"
       << '}';

    kernel = device.buildKernelFromString(ss.str(),
                                          "map");
  }

  void operator () (const int entries, occa::memory &in, occa::memory &out) {
    kernel(entries, in, out);
  }
};

occa::json parseArgs(int argc, const char **argv);

int main(int argc, const char **argv) {
  occa::json args = parseArgs(argc, argv);

  occa::setDevice((std::string) args["options/device"]);

  int entries = 5;

  float *vec  = new float[entries];
  float *vec2 = new float[entries];

  for (int i = 0; i < entries; ++i) {
    vec[i]  = i;
    vec2[i] = 0;
  }

  map squareArray;
  occa::memory o_vec, o_vec2;

  o_vec  = occa::malloc(entries*sizeof(float));
  o_vec2 = occa::malloc(entries*sizeof(float));

  squareArray.setup("float", "vec",
                    "float", "vec2",
                    "vec2 = vec * vec;");

  o_vec.copyFrom(vec);
  o_vec2.copyFrom(vec2);

  squareArray(entries, o_vec, o_vec2);

  o_vec2.copyTo(vec2);

  for (int i = 0; i < 5; ++i)
    std::cout << vec[i] << "^2 = " << vec2[i] << '\n';

  for (int i = 0; i < entries; ++i) {
    if (vec2[i] != (vec[i] * vec[i]))
      throw 1;
  }

  delete [] vec;
  delete [] vec2;

  return 0;
}

occa::json parseArgs(int argc, const char **argv) {
  // Note:
  //   occa::cli is not supported yet, please don't rely on it
  //   outside of the occa examples
  occa::cli::parser parser;
  parser
    .withDescription(
      "Example which shows run-time kernel source code generation"
    )
    .addOption(
      occa::cli::option('d', "device",
                        "Device properties (default: \"mode: 'Serial'\")")
      .withArg()
      .withDefaultValue("mode: 'Serial'")
    )
    .addOption(
      occa::cli::option('v', "verbose",
                        "Compile kernels in verbose mode")
    );

  occa::json args = parser.parseArgs(argc, argv);
  occa::settings()["kernel/verbose"] = args["options/verbose"];

  return args;
}
