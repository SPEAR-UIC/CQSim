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
 * options.h - Handling options.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef OPTIONS_H
#define OPTIONS_H

namespace misc
{

class option_reg;
class tracer;

// opt_name=opt_value ...
class options
{
	friend class option_reg;
	friend class tracer;

	bool safe_; // pretended to be empty when not safe

	// key, value, info
	typedef std::pair<std::string, std::string> str_pair;
	typedef std::map<std::string, str_pair> opt_map;
	opt_map opts_;

	// for singleton
	options() : safe_(true) {}
	~options() {safe_ = false;}

public:

	// get instance
	static options &get();

	// obselete functions
	bool add_option(cstr_t opt); // add one option, ignore strings without a '=' and return false
	void add_options(int argc, char *argv[]); // from command-line
	int find_int(const std::string &name, int def = 0) const;
	double find_double(const std::string &name, double def = 0) const;
	cstr_t find_str(const std::string &name, cstr_t def = "") const;
	bool find_bool(const std::string &name, bool def = false) const;

	// will automaticly load option files via key options
	// will replace existing values
	void load_options(int argc, char *argv[]);
	bool load_options(const std::string &option_file);
	bool load_option(const std::string &option_str);

	// show options
	void show_options(FILE *fp) const;

	// find an option and convert to single value
	int as_int(const std::string &key) const;
	double as_double(const std::string &key) const;
	cstr_t as_str(const std::string &key) const;
	bool as_bool(const std::string &key) const;

	// find an option and convert to multiple values separated by commas
	std::vector<int> as_int_vec(const std::string &key) const;
	std::vector<double> as_double_vec(const std::string &key) const;
	std::vector<std::string> as_str_vec(const std::string &key) const;

}; // class options

class option_reg
{
public:
	option_reg(
		const std::string &key,
		const std::string &value,
		const std::string &info);

}; // class option_reg

} // namespace misc

#define RegisterOption(key, value, info) \
	namespace {misc::option_reg register_option_##key(#key, value, info);}

#endif // OPTIONS_H
