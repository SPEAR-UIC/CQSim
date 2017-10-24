/*
 * Copyright (c) 2004-2008 Northwestern University.
 *                         NuCAD Group.
 *
 * Copyright (c) 2008-2009 Illinois Institute of Technology.
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
 * trace.cpp - Implementation of tracer.
 *
 * Authors: Jia Wang, jwang@ece.iit.edu
 *
 */

#include "common.h"
#include "options.h"

#include <stdarg.h>

#include "trace.h"

namespace misc
{

namespace
{

typedef std::pair<int, std::string> level_n_info;
typedef std::map<std::string, level_n_info> level_map;
volatile level_map *st_active_levels = 0;

} // namespace

tracer::tracer()
	: active_levels_(0)
{
	if (st_active_levels == 0)
		st_active_levels = new level_map;

	active_levels_ = (level_map *)st_active_levels;
}

bool tracer::is_active() const
{
	if (scopes_.empty())
		return false;

	const scope_pair &sp = scopes_.back();

	return (sp.first->second.first == -1)
		|| (sp.first->second.first >= sp.second);
}

void tracer::print(misc::cstr_t format, ...)
{
	va_list params;

	va_start(params, format);

	vfprintf(stdout, format, params);

	va_end(params);
}

void tracer::set_active_level(misc::cstr_t name, int max_level)
{
	set_active_level(std::string(name), max_level);
}

void tracer::set_active_level(const std::string &name, int max_level)
{
	level_map::iterator it = active_levels_->find(name);

	if (it == active_levels_->end())
	{
		fprintf(stderr,
			"error: unknown scope %s\n",
			name.c_str());
		throw std::runtime_error("unknown_trace_scope");
	}

	it->second.first = max_level;
}

void tracer::register_scope(
	const std::string &name,
	int max_level,
	const std::string &info)
{
	char tmp[1000];
	sprintf(tmp, "%d", max_level);
	option_reg register_me(name, tmp, info);

	level_map::iterator it = active_levels_->find(name);

	if (it != active_levels_->end())
	{
		fprintf(stderr,
			"error: duplicated trace scopes %s: old %s, new %s\n",
			name.c_str(),
			it->second.second.c_str(),
			info.c_str());
		throw std::runtime_error("duplicated_trace_scope");
	}

	active_levels_->insert(std::make_pair(name,
		std::make_pair(max_level, info)));
}

void tracer::push_scope(misc::cstr_t name, int level)
{
	push_scope(std::string(name), level);
}

void tracer::push_scope(const std::string &name, int level)
{
	level_map::const_iterator it = active_levels_->find(name);

	if (it == active_levels_->end())
	{
		fprintf(stderr,
			"error: unknown scope %s\n",
			name.c_str());
		throw std::runtime_error("unknown_trace_scope");
	}

	scopes_.push_back(std::make_pair(it, level));
}

void tracer::pop_scope()
{
	scopes_.pop_back();
}

trace_scope_reg::trace_scope_reg(
	const std::string &name,
	int max_level,
	const std::string &info)
{
	get_tracer().register_scope(name, max_level, info);
}

void tracer::set_active_levels_using_options()
{
	options &opt = options::get();

	for (options::opt_map::iterator it = opt.opts_.begin();
		it != opt.opts_.end(); ++it)
	{
		level_map::iterator itt = active_levels_->find(it->first);

		if (itt != active_levels_->end())
		{
			itt->second.first = atoi(it->second.first.c_str());
		}
	}
}

namespace
{

#ifdef _WIN32

  #ifdef _MSC_VER

__declspec(thread) tracer *st_tracer = 0;

  #else

#warning "multithreaded trace requires TLS support"

tracer *st_tracer = 0;

  #endif

#else

__thread tracer *st_tracer = 0;

#endif // _MSC_VER

} // namespace

tracer &get_tracer()
{
	if (st_tracer == 0)
		st_tracer = new tracer;

	return *st_tracer;
}

} // namespace misc
