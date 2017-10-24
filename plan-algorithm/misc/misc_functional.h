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
 * misc_functional.h - Common functional things.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef MISC_FUNCTIONAL_H
#define MISC_FUNCTIONAL_H

namespace misc
{

template <class T>
struct identity : public std::unary_function<T, T>
{
	const T &operator () (const T &v) const {return v;}
}; // struct identity<T>

template <class Pair>
struct select_1st : public std::unary_function<Pair, typename Pair::first_type>
{
	typename Pair::first_type &operator () (Pair &p) const {return p.first;}
	const typename Pair::first_type &operator () (const Pair &p) const {return p.first;}
}; // struct select_1st<Pair>

template <class Pair>
struct select_2nd : public std::unary_function<Pair, typename Pair::second_type>
{
	typename Pair::second_type &operator () (Pair &p) const {return p.second;}
	const typename Pair::second_type &operator () (const Pair &p) const {return p.second;}
}; // struct select_2nd<Pair>

// h(x) = f(g(x))
template <class F, class G>
class unary_of_unary
	: public std::unary_function<
		typename G::argument_type,
		typename F::result_type>
{
	const F &f_;
	const G &g_;

public:
	unary_of_unary(const F &f, const G &g) : f_(f), g_(g) {}

	const typename F::result_type &operator () (const typename G::argument_type &x) const
	{
		return f_(g_(x));
	}
}; // class unary_unary<F, G>

// h(x, y) = f(g1(x), g2(y))
template <class F, class G1, class G2>
class binary_of_unary
	: public std::binary_function<
		typename G1::argument_type,
		typename G2::argument_type,
		typename F::result_type>
{
	const F &f_;
	const G1 &g1_;
	const G2 &g2_;

public:
	binary_of_unary(const F &f, const G1 &g1, const G2 &g2) : f_(f), g1_(g1), g2_(g2) {}

	const typename F::result_type &operator () (
		const typename G1::argument_type &x,
		const typename G2::argument_type &y) const
	{
		return f_(g1_(x), g2_(y));
	}
}; // class binary_of_unary<F, G1, G2>

// h(x, y) = f(g(x, y))
template <class F, class G>
class unary_of_binary
	: public std::binary_function<
		typename G::first_argument_type,
		typename G::second_argument_type,
		typename F::result_type>
{
	const F &f_;
	const G &g_;

public:
	unary_of_binary(const F &f, const G &g) : f_(f), g_(g) {}

	const typename F::result_type &operator () (
		const typename G::first_argument_type &x,
		const typename G::second_argument_type &y) const
	{
		return f_(g_(x, y));
	}
}; // class unary_of_binary<F, G1, G2>

template <class F, class G> unary_of_unary<F, G>
combine_11(const F &f, const G &g) {return unary_of_unary<F, G>(f, g);}

template <class F, class G1, class G2> binary_of_unary<F, G1, G2>
combine_21(const F &f, const G1 &g1, const G2 &g2) {return binary_of_unary<F, G1, G2>(f, g1, g2);}

template <class F, class G> unary_of_binary<F, G>
combine_12(const F &f, const G &g) {return unary_of_binary<F, G>(f, g);}

} // namespace misc

#endif // MISC_FUNCTIONAl_H
