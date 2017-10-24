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
 * misc_str.cpp - Common string things.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#include "common.h"

#include "misc_str.h"

namespace misc
{

namespace
{

std::string left(cstr_t str, size_t len, int n)
{
	if (n < 0)
		n += (int)len;

	// truncate
	if (n < 0)
		n = 0;
	if (n > (int)len)
		n = (int)len;

	return std::string(str, str+n);
}

std::string right(cstr_t str, size_t len, int n)
{
	if (n < 0)
		n += (int)len;

	// truncate
	if (n < 0)
		n = 0;
	if (n > (int)len)
		n = (int)len;

	return std::string(str+n, str+len);
}

} // namespace

std::string str_left(cstr_t str, int n)
{
	return left(str, strlen(str), n);
}

std::string str_left(const std::string &str, int n)
{
	return left(str.c_str(), str.length(), n);
}

std::string str_right(cstr_t str, int n)
{
	return right(str, strlen(str), n);
}

std::string str_right(const std::string &str, int n)
{
	return right(str.c_str(), str.length(), n);
}

} // namespace misc

namespace os
{

namespace
{

size_t after_last_sep(misc::cstr_t str, size_t len)
{
	for (; len != 0; --len)
		if ((str[len-1] == '\\') || (str[len-1] == '/'))
			break;
	return len;
}

} // namespace

std::string basename(misc::cstr_t str)
{
	size_t len = strlen(str);

	return std::string(str+after_last_sep(str, len), str+len);
}

std::string basename(const std::string &str)
{
	return str.substr(after_last_sep(str.c_str(), str.length()));
}

std::string dirname(misc::cstr_t str)
{
	size_t i = after_last_sep(str, strlen(str));

	if (i == 0)
		return std::string();
	else
		return std::string(str, str+i-1);
}

std::string dirname(const std::string &str)
{
	size_t i = after_last_sep(str.c_str(), str.length());

	if (i < 2)
		return ".";
	else
		return str.substr(0, i-1);
}

} // namespace os
