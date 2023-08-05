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

#ifndef OCCA_TOOLS_HASH_HEADER
#define OCCA_TOOLS_HASH_HEADER

#include <iostream>

#include <occa/defines.hpp>
#include <occa/types.hpp>

namespace occa {
  // Uses FNV hashing
  class hash_t {
  public:
    bool initialized;
    int h[8];

    mutable std::string h_string;
    mutable int sh[8];

    hash_t();
    hash_t(const int *h_);
    hash_t(const hash_t &hash);
    hash_t& operator = (const hash_t &hash);

    void clear();

    inline bool isInitialized() const { return initialized; }

    bool operator < (const hash_t &fo) const;
    bool operator == (const hash_t &fo) const;
    bool operator != (const hash_t &fo) const;

    hash_t& operator ^= (const hash_t hash);

    template <class TM>
    hash_t operator ^ (const TM &t) const;

    std::string toFullString() const;
    std::string toString() const;
    operator std::string () const;

    static hash_t fromString(const std::string &s);

    friend std::ostream& operator << (std::ostream &out, const hash_t &hash);
  };
  std::ostream& operator << (std::ostream &out, const hash_t &hash);

  hash_t hash(const void *ptr, udim_t bytes);

  template <class TM>
  inline hash_t hash(const TM &t) {
    return hash(&t, sizeof(TM));
  }

  template <class TM>
  inline hash_t hash_t::operator ^ (const TM &t) const {
    return (*this ^ hash(t));
  }

  template <>
  hash_t hash_t::operator ^ (const hash_t &hash) const;

  hash_t hash(const char *c);
  hash_t hash(const std::string &str);
  hash_t hashFile(const std::string &filename);
}

#endif
