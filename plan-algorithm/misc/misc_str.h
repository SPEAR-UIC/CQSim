/*
 * Copyright (c) 2004-2005 Northwestern University.
 *                         NuCAD Group.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/*
 * misc_str.h - Common string things.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef MISC_STR_H
#define MISC_STR_H

namespace misc
{

typedef const char *cstr_t;

struct cstr_less : public std::binary_function<cstr_t, cstr_t, bool>
{
	bool operator() (cstr_t a, cstr_t b) const
	{
		return strcmp(a, b) < 0;
	}
}; // struct cstr_less

struct cstr_equal_to : public std::binary_function<cstr_t, cstr_t, bool>
{
	bool operator() (cstr_t a, cstr_t b) const
	{
		return strcmp(a, b) == 0;
	}
}; // struct cstr_equal_to

struct cstr_hash : public std::unary_function<cstr_t, size_t>
{
	size_t operator()(cstr_t s) const
	{
		size_t ret = 5381;

		for(; *s != 0; ++s)
			ret = ret*33+*s;

		return ret;
	};
}; // struct cstr_hash

// python-like slicing: str[:n] and str[n:]
std::string str_left(cstr_t str, int n);
std::string str_left(const std::string &str, int n);
std::string str_right(cstr_t str, int n);
std::string str_right(const std::string &str, int n);

} // namespace misc

// I don't know where to put them now ...
namespace os
{

std::string basename(misc::cstr_t str);
std::string basename(const std::string &str);
std::string dirname(misc::cstr_t str);
std::string dirname(const std::string &str);

} // namespace os

#endif // MISC_STR_H
