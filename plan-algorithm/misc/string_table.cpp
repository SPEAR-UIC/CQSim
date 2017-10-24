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
 * string_table.cpp - Constant strings with identities.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#include "common.h"

#include "string_table.h"

namespace misc
{

namespace detail
{

class string_table_t
{
	typedef std::pair<size_t, char *> buf_t;
	std::vector<buf_t> bufs_;

	std::list<std::string> big_strs_;

	enum {BUF_SIZE = 1024*1024, MAX_LEN = 1024};

	~string_table_t()
	{
		for (size_t i = 0; i < bufs_.size(); ++i)
			delete[] bufs_[i].second;
	}

public:
	static string_table_t &get_table()
	{
		static string_table_t table;
		return table;
	}

	cstr_t store_string(const char *str, size_t len)
	{
		++len; // plus 0

		if (len > MAX_LEN)
		{
			big_strs_.push_back(std::string());
			big_strs_.back().assign(str, str+len-1);
			return big_strs_.back().c_str();
		}
		else
		{
			if ((bufs_.size() == 0) || (bufs_.back().first+len > BUF_SIZE))
				bufs_.push_back(std::make_pair(0, new char[BUF_SIZE]));

			char *ret = bufs_.back().second+bufs_.back().first;

			memcpy(ret, str, len);
			bufs_.back().first += len;

			return ret;
		}
	}
}; // class string_table_t

}

cstr_t string_table_store_str(cstr_t str)
{
	return detail::string_table_t::get_table()
		.store_string(str, strlen(str));
}

cstr_t string_table_store_str(const std::string &str)
{
	return detail::string_table_t::get_table()
		.store_string(str.c_str(), str.length());
}

} // namespace misc
