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
 * timer.h - Time calculating.
 *
 * Authors: Hai Zhou, haizhou@ece.northwestern.edu
 *          Jia Wang, jwa112@ece.northwestern.edu
 */

#ifndef TIMER_H
#define TIMER_H

namespace os
{

namespace detail {class timer_impl_t;}

// for low-resolution timing, e.g. 100ms or more
// clock() will wrap back soon so we have this class
// work like a stop-watch, begin counting once you
// create it and reset/record when you call stop() 
class timer_t
{
	// no copy, no assign
	timer_t(const timer_t &);
	timer_t &operator = (const timer_t &);

	detail::timer_impl_t *p_;

public:
	timer_t();
	~timer_t();

	void stop();

	double real() const;
	double user() const;
	double sys() const;

}; // class timer_t

namespace detail {class timer2_impl;}

class timer2
{
	timer2(timer2 &);
	timer2 &operator = (const timer2 &);

public:
	timer2(); // will set start and stop both to current
	~timer2();

	// count time between start and stop
	void start_now(); // current time
	void start_last(); // last stop
	void stop_now(); // current time

	double real() const;
	double user() const;
	double sys() const;

protected:
#ifdef HAS_LIBCXX11
	std::unique_ptr<detail::timer2_impl> start_, stop_;
#else
	std::auto_ptr<detail::timer2_impl> start_, stop_;
#endif // HAS_LIBCXX11

}; // class timer2

class timer_vec
{
public:
	timer_vec();

	void start_now();
	void start_last();
	void stop_now();

	size_t num_items() const;
	double real(size_t i) const;
	double user(size_t i) const;
	double sys(size_t i) const;

	double total_real() const;
	double total_user() const;
	double total_sys() const;

protected:
	std::vector<double> items_;
	
	timer2 timer_;

	double total_real_, total_user_, total_sys_;

}; // class timer_vec

} // namespace os

#endif
