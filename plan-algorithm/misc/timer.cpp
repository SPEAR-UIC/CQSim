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
 * timer.cpp - Implement time calculating.
 *
 * Authors: Hai Zhou, haizhou@ece.northwestern.edu
 *          Jia Wang, jwa112@ece.northwestern.edu
 */

#include "common.h"

#ifdef _WIN32

#include <windows.h>

#else // !_WIN32

#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>

#endif // _WIN32

#include "timer.h"

namespace os
{

namespace detail
{

#ifdef _WIN32

class timer_impl_t
{
	ULARGE_INTEGER real_, real_stop_, user_, user_stop_, sys_, sys_stop_;

public:
	timer_impl_t()
	{
		stop();

		real_.QuadPart = real_stop_.QuadPart;
		user_.QuadPart = user_stop_.QuadPart;
		sys_.QuadPart = sys_stop_.QuadPart;
	}

	void stop()
	{
		real_.QuadPart = real_stop_.QuadPart;
		user_.QuadPart = user_stop_.QuadPart;
		sys_.QuadPart = sys_stop_.QuadPart;

		GetSystemTimeAsFileTime((LPFILETIME)&real_stop_);

		FILETIME a, b;
		GetProcessTimes(GetCurrentProcess(), &a, &b,
			(LPFILETIME)&sys_stop_, (LPFILETIME)&user_stop_);
	}

	double real() const {return (real_stop_.QuadPart-real_.QuadPart)/1e7;}
	double user() const {return (user_stop_.QuadPart-user_.QuadPart)/1e7;}
	double sys() const {return (sys_stop_.QuadPart-sys_.QuadPart)/1e7;}

}; // timer_impl_t

class timer2_impl
{
	ULARGE_INTEGER real_, user_, sys_;

public:
	timer2_impl()
	{
		get_current_time();
	}

	void get_current_time()
	{
		GetSystemTimeAsFileTime((LPFILETIME)&real_);

		FILETIME a, b;
		GetProcessTimes(GetCurrentProcess(), &a, &b,
			(LPFILETIME)&sys_, (LPFILETIME)&user_);
	}

	double real(const timer2_impl &t) const
	{
		return (real_.QuadPart-t.real_.QuadPart)/1e7;
	}
	double user(const timer2_impl &t) const
	{
		return (user_.QuadPart-t.user_.QuadPart)/1e7;
	}
	double sys(const timer2_impl &t) const
	{
		return (sys_.QuadPart-t.sys_.QuadPart)/1e7;
	}

}; // timer2_impl

#else // !_WIN32

class timer_impl_t
{
	double real_, real_stop_, user_, user_stop_, sys_, sys_stop_;

public:
	timer_impl_t()
	{
		stop();

		real_ = real_stop_;
		user_ = user_stop_;
		sys_ = sys_stop_;
	}

	void stop()
	{
		real_ = real_stop_;
		user_ = user_stop_;
		sys_ = sys_stop_;

		timeval tv;
		gettimeofday(&tv, 0);

		rusage ru;
		getrusage(RUSAGE_SELF, &ru);

		real_stop_ = tv.tv_sec+tv.tv_usec/1e6;
		user_stop_ = ru.ru_utime.tv_sec+ru.ru_utime.tv_usec/1e6;
		sys_stop_ = ru.ru_stime.tv_sec+ru.ru_stime.tv_usec/1e6;
	}

	double real() const {return real_stop_-real_;}
	double user() const {return user_stop_-user_;}
	double sys() const {return sys_stop_-sys_;}

}; // timer_impl_t

class timer2_impl
{
	double real_, user_, sys_;

public:
	timer2_impl()
	{
		get_current_time();
	}

	void get_current_time()
	{
		timeval tv;
		gettimeofday(&tv, 0);

		rusage ru;
		getrusage(RUSAGE_SELF, &ru);

		real_ = tv.tv_sec+tv.tv_usec/1e6;
		user_ = ru.ru_utime.tv_sec+ru.ru_utime.tv_usec/1e6;
		sys_ = ru.ru_stime.tv_sec+ru.ru_stime.tv_usec/1e6;
	}

	double real(const timer2_impl &t) const
	{
		return real_-t.real_;
	}
	double user(const timer2_impl &t) const
	{
		return user_-t.user_;
	}
	double sys(const timer2_impl &t) const
	{
		return sys_-t.sys_;
	}

}; // timer2_impl

#endif // _WIN32
} // namespace detail

timer_t::timer_t()
	: p_(new detail::timer_impl_t)
{
}

timer_t::~timer_t()
{
	delete p_;
}

void timer_t::stop()
{
	p_->stop();
}

double timer_t::real() const
{
	return p_->real();
}

double timer_t::user() const
{
	return p_->user();
}

double timer_t::sys() const
{
	return p_->sys();
}

timer2::timer2()
	: start_(new detail::timer2_impl), stop_(new detail::timer2_impl)
{
}

timer2::~timer2()
{
}

void timer2::start_now()
{
	start_->get_current_time();
}

void timer2::start_last()
{
	*start_ = *stop_;
}

void timer2::stop_now()
{
	stop_->get_current_time();
}

double timer2::real() const
{
	return stop_->real(*start_);
}

double timer2::user() const
{
	return stop_->user(*start_);
}

double timer2::sys() const
{
	return stop_->sys(*start_);
}

timer_vec::timer_vec()
	:total_real_(0), total_user_(0), total_sys_(0)
{
	items_.reserve(3000);
}

void timer_vec::start_now()
{
	timer_.start_now();
}

void timer_vec::start_last()
{
	timer_.start_last();
}

void timer_vec::stop_now()
{
	timer_.stop_now();

	double r = timer_.real();
	double u = timer_.user();
	double s = timer_.sys();

	items_.push_back(r);
	items_.push_back(u);
	items_.push_back(s);

	total_real_ += r;
	total_user_ += u;
	total_sys_ += s;
}

size_t timer_vec::num_items() const
{
	return items_.size()/3;
}

double timer_vec::real(size_t i) const
{
	assert(i < num_items());

	return items_[i*3];
}

double timer_vec::user(size_t i) const
{
	assert(i < num_items());

	return items_[i*3+1];
}

double timer_vec::sys(size_t i) const
{
	assert(i < num_items());

	return items_[i*3+2];
}

double timer_vec::total_real() const
{
	return total_real_;
}

double timer_vec::total_user() const
{
	return total_user_;
}

double timer_vec::total_sys() const
{
	return total_sys_;
}

} // namespace os
