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
 * token_parser.h - Token parser and helper functions.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef TOKEN_PARSER_H
#define TOKEN_PARSER_H

namespace misc
{

// delimit chars are spaces
char *skip_space(char *buf, cstr_t delimit);
char *goto_space(char *buf, cstr_t delimit);
const char *skip_space(const char *buf, cstr_t delimit);
const char *goto_space(const char *buf, cstr_t delimit);

// in-place split by delimit chars
void split_tokens(char *buf, std::vector<cstr_t> *ptokens, cstr_t delimit);

// split to string vector
void split_tokens(const char *buf, std::vector<std::string> *ptokens, cstr_t delimit);

// faster op through bmp
struct delimit_bmp {unsigned int bmp[8];};
delimit_bmp create_delimit_bmp(cstr_t delimit);
char *skip_space(char *buf, const delimit_bmp &bmp);
char *goto_space(char *buf, const delimit_bmp &bmp);
void split_tokens(char *buf, std::vector<cstr_t> *ptokens, const delimit_bmp &bmp);
const char *skip_space(const char *buf, const delimit_bmp &bmp);
const char *goto_space(const char *buf, const delimit_bmp &bmp);
void split_tokens(const char *buf, std::vector<std::string> *ptokens, const delimit_bmp &bmp);

// read a logical line and append to line
// first, every logical line stop at the cmtch char
// second every logical line across a line ending eith lnch
// so lnch at the end of comments will be ignored
// will increase *p_line_no if presented
bool read_logical_line(
   FILE *fp,
   std::string &line,
   char lnch = '\\',
   char cmtch = '#',
   size_t *p_line_no = 0);

// get a line, similar as std::getline but takes FILE *
// return false for eof
bool getline(FILE *fp, std::string &line);

} // namespace misc

#endif // TOKEN_PARSER_H
