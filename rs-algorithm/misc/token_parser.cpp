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
 * token_parser.cpp - Implementation of token parser and helper functions.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#include "common.h"

#include "token_parser.h"

namespace misc
{

delimit_bmp create_delimit_bmp(cstr_t delimit)
{
	delimit_bmp ret;

	for (size_t i = 0; i < 8; ++i)
		ret.bmp[i] = 0;

	for (; *delimit != 0; ++delimit)
	{
		size_t i = (unsigned char)(*delimit)/32;
		size_t bit = (unsigned char)(*delimit)%32;

		ret.bmp[i] |= (1 << bit);
	}
	return ret;
}

template <class T>
T skip_space_tmpl(T buf, cstr_t delimit)
{
	for (; *buf != 0; ++buf)
	{
		size_t i;
		for (i = 0; delimit[i] != 0; ++i)
			if (*buf == delimit[i])
				break;
		if (delimit[i] == 0)
			return buf;
	}
	return buf;
}

template <class T>
T goto_space_tmpl(T buf, cstr_t delimit)
{
	for (; *buf != 0; ++buf)
		for (size_t i = 0; delimit[i] != 0; ++i)
			if (*buf == delimit[i])
				return buf;
	return buf;
}

template <class T>
T skip_space_bmp_tmpl(T buf, const delimit_bmp &bmp)
{
	for (; *buf != 0; ++buf)
	{
		size_t i = (unsigned char)(*buf)/32;
		size_t bit = (unsigned char)(*buf)%32;

		if ((bmp.bmp[i] & (1 << bit)) == 0)
			return buf;
	}
	return buf;
}

template <class T>
T goto_space_bmp_tmpl(T buf, const delimit_bmp &bmp)
{
	for (; *buf != 0; ++buf)
	{
		size_t i = (unsigned char)(*buf)/32;
		size_t bit = (unsigned char)(*buf)%32;

		if ((bmp.bmp[i] & (1 << bit)) != 0)
			return buf;
	}
	return buf;
}

char *skip_space(char *buf, cstr_t delimit)
{
	return skip_space_tmpl(buf, delimit);
}

char *skip_space(char *buf, const delimit_bmp &bmp)
{
	return skip_space_bmp_tmpl(buf, bmp);
}

char *goto_space(char *buf, cstr_t delimit)
{
	return goto_space_tmpl(buf, delimit);
}

char *goto_space(char *buf, const delimit_bmp &bmp)
{
	return goto_space_bmp_tmpl(buf, bmp);
}

const char *skip_space(const char *buf, cstr_t delimit)
{
	return skip_space_tmpl(buf, delimit);
}

const char *skip_space(const char *buf, const delimit_bmp &bmp)
{
	return skip_space_bmp_tmpl(buf, bmp);
}

const char *goto_space(const char *buf, cstr_t delimit)
{
	return goto_space_tmpl(buf, delimit);
}

const char *goto_space(const char *buf, const delimit_bmp &bmp)
{
	return goto_space_bmp_tmpl(buf, bmp);
}

void split_tokens(char *buf, std::vector<cstr_t> *ptokens, cstr_t delimit)
{
	for (char *begin = buf; *begin != 0;)
	{
		char *end = goto_space(begin, delimit);
		ptokens->push_back(begin);
		if (*end == 0)
			return;
		*end = 0;
		begin = skip_space(end+1, delimit);
	}
}

// split to string vector
void split_tokens(const char *buf, std::vector<std::string> *ptokens, cstr_t delimit)
{
	for (const char *begin = buf; *begin != 0;)
	{
		const char *end = goto_space(begin, delimit);
		ptokens->push_back(std::string(begin, end));
		if (*end == 0)
			return;
		begin = skip_space(end+1, delimit);
	}
}

void split_tokens(char *buf, std::vector<cstr_t> *ptokens, const delimit_bmp &bmp)
{
	for (char *begin = buf; *begin != 0;)
	{
		char *end = goto_space(begin, bmp);
		ptokens->push_back(begin);
		if (*end == 0)
			return;
		*end = 0;
		begin = skip_space(end+1, bmp);
	}
}

void split_tokens(const char *buf, std::vector<std::string> *ptokens, const delimit_bmp &bmp)
{
	for (const char *begin = buf; *begin != 0;)
	{
		const char *end = goto_space(begin, bmp);
		ptokens->push_back(std::string(begin, end));
		if (*end == 0)
			return;
		begin = skip_space(end+1, bmp);
	}
}

bool read_logical_line(
	FILE *fp,
	std::string &line,
	char lnch,
	char cmtch,
	size_t *p_line_no)
{
	for (;;)
	{
		// read a physical line
  		char linebuf[1024];
		if (fgets(linebuf, sizeof(linebuf), fp) == 0)
		{
			if (line == "")
				return false;
			else
				break;
		}
		if (p_line_no != 0)
			++(*p_line_no);

		// see if there is any comment
		char *cmt = strchr(linebuf, cmtch);
		if (cmt == 0)
		{
			line += linebuf;
		}
		else
		{
			*cmt = 0;
			line += linebuf;
			break;
		}

		char flags[3] = {0, 0, 0}; // 0: any, 1: \, 2: \r or \n
		for (size_t i = 0, j = line.length();
			(i < 3) && (j > 0); ++i, --j)
			if ((line[j-1] == '\r') || (line[j-1] == '\n'))
				flags[i] = 2;
			else if (line[j-1] == lnch)
				flags[i] = 1;

		if (flags[0] == 2)
			// end of physical line
		{
			if (flags[1] == 1) // "\\\n"
				// logical line not end yet, pop two
				line.erase(line.end()-2, line.end());
			else if ((flags[1] == 2) && (flags[2] == 1)) // "\\\r\n"
				// logical line not end yet, pop three
				line.erase(line.end()-3, line.end());
			else
				// logical line end as well
				break;
		}
	}

	return true;
}

bool getline(FILE *fp, std::string &line)
{
	line.clear();

	for (;;)
	{
		// attempt to read a line
  		char linebuf[1024];
		if (fgets(linebuf, sizeof(linebuf), fp) == 0)
			return line != ""; // watch out for last line w/o \n

		line += linebuf;

		size_t l = line.length();
		assert(l > 0);

		if ((line[l-1] == '\r') || (line[l-1] == '\n'))
			break;
	}
	return true;
}

} // namespace misc
