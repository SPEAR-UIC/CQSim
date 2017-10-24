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
 * trace.h - Trace.
 *
 * Authors: Jia Wang, jwang@ece.iit.edu
 *
 */

#ifndef TRACE_H
#define TRACE_H

namespace misc
{

class trace_scope_reg;

class tracer
{
	friend class trace_scope_reg;

public:
	tracer();

	bool is_active() const;

	void print(misc::cstr_t format, ...);

	void set_active_level(misc::cstr_t name, int max_level);
	void set_active_level(const std::string &name, int max_level);
	void push_scope(misc::cstr_t name, int level);
	void push_scope(const std::string &name, int level);
	void pop_scope();

	void set_active_levels_using_options();

	void show_scopes(FILE *fp) const;

protected:

	void register_scope(
		const std::string &name,
		int max_level,
		const std::string &info);

	typedef std::pair<int, std::string> level_n_info;
	typedef std::map<std::string, level_n_info> level_map;
	level_map *active_levels_;

	typedef std::pair<level_map::const_iterator, int> scope_pair;
	std::list<scope_pair> scopes_;

}; // class tracer

tracer &get_tracer();

struct trace_scope
{
	trace_scope(const std::string &name, int level)
	{
		get_tracer().push_scope(name, level);
	}

	~trace_scope()
	{
		get_tracer().pop_scope();
	}

}; // struct trace_scope

class trace_scope_reg
{
public:
	trace_scope_reg(
		const std::string &name,
		int max_level,
		const std::string &info);

}; // class trace_scope_reg

} // namespace misc

#ifndef MISC_NO_TRACE

#define RegisterTraceScope(name, max_level, info) \
	namespace {misc::trace_scope_reg register_trace_scope_##name(#name, max_level, info);}

#define TraceScope(name, level) \
	misc::trace_scope _trace_scope_obj(name, level)

#define TracePrint \
	if (!misc::get_tracer().is_active()) \
		; \
	else \
		misc::get_tracer().print

inline bool TraceActive()
{
	return misc::get_tracer().is_active();
}

#else // MISC_NO_TRACE

#define RegisterTraceScope(name, max_level, info)

#define TraceScope(name, level) do {} while (false)

#define TracePrint if (true); else misc::get_tracer().print

inline bool TraceActive()
{
	return false;
}

#endif // MISC_NO_TRACE

#endif // TRACE_H
