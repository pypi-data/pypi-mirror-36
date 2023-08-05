#ifndef PYTHONIC_INCLUDE_NUMPY_POWER_HPP
#define PYTHONIC_INCLUDE_NUMPY_POWER_HPP

#include "pythonic/include/types/numpy_op_helper.hpp"
#include "pythonic/include/utils/meta.hpp"
#include "pythonic/include/utils/numpy_traits.hpp"
#include "pythonic/include/utils/functor.hpp"

#include <boost/simd/function/pow.hpp>

PYTHONIC_NS_BEGIN

namespace numpy
{
  namespace wrapper
  {
    template <class T0, class T1>
    auto pow(T0 const &t0, T1 const &t1) -> typename std::enable_if<
        !std::is_integral<T1>::value,
        decltype(boost::simd::pow((typename std::common_type<T0, T1>::type)t0,
                                  (typename std::common_type<T0, T1>::type)
                                      t1))>::type
    {
      return boost::simd::pow((typename std::common_type<T0, T1>::type)t0,
                              (typename std::common_type<T0, T1>::type)t1);
    }

    template <class T0, class T1>
    auto pow(T0 const &t0, T1 const &t1) ->
        typename std::enable_if<std::is_integral<T1>::value, T0>::type
    {
      T0 a = t0;
      T1 b = t1;
      const int recip = b < 0;
      T0 r = 1;
      while (1) {
        if (b & 1)
          r *= a;
        b /= 2;
        if (b == 0)
          break;
        a *= a;
      }
      return recip ? 1 / r : r;
    }

    // See https://github.com/MetaScale/nt2/issues/794
    double pow(long const &n, double const &m)
    {
      return pow(static_cast<double>(n), m);
    }
    template <class T>
    std::complex<T> pow(T const &n, std::complex<T> const &m)
    {
      return std::pow(n, m);
    }
    template <class T>
    std::complex<T> pow(std::complex<T> const &n, std::complex<T> const &m)
    {
      return std::pow(n, m);
    }
    template <class T>
    std::complex<T> pow(std::complex<T> const &n, T const &m)
    {
      return std::pow(n, m);
    }
  }
#define NUMPY_NARY_FUNC_NAME power
#define NUMPY_NARY_FUNC_SYM wrapper::pow
// no need to adapt_type here, as it may turn a**2 into a**2.f
#define NUMPY_NARY_RESHAPE_MODE reshape_type
#include "pythonic/include/types/numpy_nary_expr.hpp"
}
PYTHONIC_NS_END

#endif
