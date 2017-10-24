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
 * common.h - Common things.
 *
 * Authors: Jia Wang, jwa112@ece.northwestern.edu
 *
 */

#ifndef COMMON_H
#define COMMON_H

#ifdef _MSC_VER

// no deprecated function for VC8
#ifndef _CRT_SECURE_NO_DEPRECATE
#define _CRT_SECURE_NO_DEPRECATE
#endif // _CRT_SECURE_NO_DEPRECATE
#ifndef _SCL_SECURE_NO_DEPRECATE
#define _SCL_SECURE_NO_DEPRECATE
#endif // _SCL_SECURE_NO_DEPRECATE

// turn off warning 4786 for vc6
//	identifier was truncated to '255' characters in the debug information
#pragma warning(disable: 4786)

// turn off range validation in vector's [] for vc8
#ifdef NDEBUG
#ifndef _SECURE_SCL
#define _SECURE_SCL 0
#endif // _SECURE_SCL
#endif // NDEBUG

#endif // _MSC_VER

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#include <math.h>
#include <sys/types.h>
#include <sys/stat.h>

#ifdef __GNUC__
#define _vsnprintf vsnprintf
#define _strnicmp strncasecmp
#define _stricmp strcasecmp
#endif // __GNUC__

#ifndef _WIN32
#define _popen popen
#define _pclose pclose
#endif

#include <list>
#include <set>
#include <map>
#include <string>
#include <vector>
#include <stdexcept>
#include <functional>
#include <algorithm>
#include <utility>
#include <numeric>
#include <memory>
#include <queue>
#include <complex>

// so far we only care about the following libs from C++11
//   unordered_XXX
//   shared_ptr/unique_ptr
#if _MSC_VER >= 1600
#include <unordered_map>
#define HAS_LIBCXX11
#endif

#if defined __GXX_EXPERIMENTAL_CXX0X__ && \
	__GNUC__*10000+__GNUC_MINOR__*100 >= 40400
#include <unordered_map>
#define HAS_LIBCXX11
#endif

// you can use /Za instead for VC6
#if _MSC_VER < 1300
	#define for if (0) ; else for
#endif

#include "misc_str.h"
#include "misc_functional.h"

#endif // COMMON_H
