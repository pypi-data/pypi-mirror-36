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

#include <occa/io/utils.hpp>
#include <occa/tools/properties.hpp>
#include <occa/tools/string.hpp>

namespace occa {
  properties::properties() {
    type = object_;
    initialized = false;
  }

  properties::properties(const properties &other) {
    type = object_;
    value_ = other.value_;
    initialized = other.initialized;
  }

  properties::properties(const json &j) {
    type = object_;
    value_ = j.value_;
    initialized = true;
  }

  properties::properties(const char *c) {
    properties::load(c);
  }

  properties::properties(const std::string &s) {
    properties::load(s);
  }

  properties::~properties() {}

  bool properties::isInitialized() {
    if (!initialized) {
      initialized = value_.object.size();
    }
    return initialized;
  }

  void properties::load(const char *&c) {
    lex::skipWhitespace(c);
    loadObject(c);
    initialized = true;
  }

  void properties::load(const std::string &s) {
    const char *c = s.c_str();
    lex::skipWhitespace(c);
    loadObject(c);
    initialized = true;
  }

  properties properties::read(const std::string &filename) {
    properties props;
    props.load(io::read(filename));
    return props;
  }

  template <>
  hash_t hash(const properties &props) {
    return props.hash();
  }
}
