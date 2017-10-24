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
 * auto_file.h - Automatic file/pipe.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef AUTO_FILE_H
#define AUTO_FILE_H

namespace os
{

// follow the perl convention
// "> name" write
// ">> name" append
// "name", "< name" read
// "+> name" read/write
// "| cmd" pipe to
// "cmd |" pipe from

class auto_file
{
	// no copy/assign
	auto_file(const auto_file &);
	auto_file &operator = (const auto_file &);

	FILE *fp_;
	bool pipe_;

public:
	auto_file();
	~auto_file();

	void clear();

	// will clear the old one automatically
	// make sure you get the right text/binary mode
	bool file_open(const std::string &name, misc::cstr_t mode);
	bool pipe_open(const std::string &cmd, misc::cstr_t mode);

	FILE *get_fp() const;

	// some commonly used commands
	bool gz_read(const std::string &name, bool binary = false);
	bool gz_write(const std::string &name, bool binary = false);

}; // class auto_file

} // namespace os

#endif // AUTO_FILE_H
