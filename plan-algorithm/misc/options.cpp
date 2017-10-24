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
 * options.cpp - Implementation of option handling.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#include "common.h"
#include "auto_file.h"
#include "token_parser.h"

#include "options.h"

namespace misc
{

options &options::get()
{
	static options opts;
	return opts;
}

bool options::add_option(cstr_t opt)
{
	if (!safe_)
		return false;

	std::vector<std::string> pair;

	split_tokens(opt, &pair, "=");

	if (pair.size() == 2)
	{
		opts_[pair[0]] = std::make_pair(pair[1], "unknown");
		return true;
	}
	else
	{
		return false;
	}
}

void options::add_options(int argc, char *argv[])
{
	if (!safe_)
		return;

	for (int i = 0; i < argc; ++i)
		add_option(argv[i]);
}

int options::find_int(const std::string &name, int def) const
{
	if (!safe_)
		return def;

	opt_map::const_iterator it = opts_.find(name);
	if (it == opts_.end())
		return def;
	else
		return atoi(it->second.first.c_str());
}

double options::find_double(const std::string &name, double def) const
{
	if (!safe_)
		return def;

	opt_map::const_iterator it = opts_.find(name);
	if (it == opts_.end())
		return def;
	else
		return atof(it->second.first.c_str());
}

cstr_t options::find_str(const std::string &name, cstr_t def) const
{
	if (!safe_)
		return def;

	opt_map::const_iterator it = opts_.find(name);
	if (it == opts_.end())
		return def;
	else
		return it->second.first.c_str();
}

bool options::find_bool(const std::string &name, bool def) const
{
	if (!safe_)
		return def;

	opt_map::const_iterator it = opts_.find(name);
	if (it == opts_.end())
		return def;
	else
		return it->second.first == "true";
}

option_reg::option_reg(
	const std::string &key,
	const std::string &value,
	const std::string &info)
{
	options &opt = options::get();

	if (!opt.safe_)
		return;

	options::opt_map::iterator it = opt.opts_.find(key);

	if (it != opt.opts_.end())
	{
		fprintf(stderr,
			"error: duplicated option %s: old %s, new %s\n",
			key.c_str(),
			it->second.second.c_str(),
			info.c_str());
		throw std::runtime_error("duplicated_option_key");
	}

	opt.opts_.insert(std::make_pair(key, std::make_pair(value, info)));
}

void options::load_options(int argc, char *argv[])
{
	for (int i = 0; i < argc; ++i)
		load_option(argv[i]);
}

bool options::load_options(const std::string &option_file)
{
	fprintf(stderr,
		"warning: ignore option file %s: not implemented\n",
		option_file.c_str());

	return true;
}

bool options::load_option(const std::string &option_str)
{
	if (!safe_)
		return false;

	std::vector<std::string> pair;

	split_tokens(option_str.c_str(), &pair, "=");

	if (pair.size() != 2)
		return false;

	if (pair[0] == "options")
	{
		std::vector<std::string> files;
		split_tokens(pair[1].c_str(), &files, ",");
		for (size_t i = 0; i < files.size(); ++i)
			load_options(files[i]);

		return true;
	}

	opt_map::iterator it = opts_.find(pair[0]);

	if (it == opts_.end())
	{
		fprintf(stderr,
			"warning: unknown option %s\n",
			pair[0].c_str());
		return true;
	}

	it->second.first = pair[1];

	return true;
}

void options::show_options(FILE *fp) const
{
	fprintf(fp, "%u options:\n", opts_.size());

	for (opt_map::const_iterator it = opts_.begin();
		it != opts_.end(); ++it)
		fprintf(fp,
			"  %s=%s: %s\n",
			it->first.c_str(),
			it->second.first.c_str(),
			it->second.second.c_str());
}

int options::as_int(const std::string &key) const
{
	return atoi(as_str(key));
}

double options::as_double(const std::string &key) const
{
	return atof(as_str(key));
}

cstr_t options::as_str(const std::string &key) const
{
	if (!safe_)
		return "";

	opt_map::const_iterator it = opts_.find(key);
	if (it == opts_.end())
	{
		fprintf(stderr,
			"error: unknown option %s\n",
			key.c_str());
		throw std::runtime_error("unknown_option_key");
	}

	return it->second.first.c_str();
}

bool options::as_bool(const std::string &key) const
{
	return strcmp(as_str(key), "true") == 0;
}

std::vector<int> options::as_int_vec(const std::string &key) const
{
	std::vector<std::string> strs = as_str_vec(key);

	std::vector<int> ret(strs.size());

	for (size_t i = 0; i < ret.size(); ++i)
		ret[i] = atoi(strs[i].c_str());

	return ret;
}

std::vector<double> options::as_double_vec(const std::string &key) const
{
	std::vector<std::string> strs = as_str_vec(key);

	std::vector<double> ret(strs.size());

	for (size_t i = 0; i < ret.size(); ++i)
		ret[i] = atof(strs[i].c_str());

	return ret;
}

std::vector<std::string> options::as_str_vec(const std::string &key) const
{
	std::vector<std::string> ret;

	split_tokens(as_str(key), &ret, ",");

	return ret;
}

} // namespace misc
