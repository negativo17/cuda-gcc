%global _gnu %{nil}
%global _host %{_target_platform}
%global gcc_compat_version 64
%global gcc_target_platform %{_target_platform}
%global gmp_version 4.3.2
%global libmpc_version 0.8.1
%global mpfr_version 2.4.2
%global binary_prefix cuda-

Name:           cuda-gcc
Version:        6.4.0
Release:        2%{?dist}
Summary:        GNU Compiler Collection CUDA compatibility package
License:        GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:            http://gcc.gnu.org

Source0:        http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
Patch0:         gcc-6.4.0-libatomic.patch
Patch1:         gcc-6.4.0-unwind.patch
Patch2:         gcc-6.4.0-libsanitizer.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
# from contrib/download_prerequisites
BuildRequires:  gmp-devel >= %{gmp_version}
BuildRequires:  isl-devel >= 0.15
BuildRequires:  libmpc-devel >= %{libmpc_version}
BuildRequires:  mpfr-devel >= %{mpfr_version}
BuildRequires:  zlib-devel

%description
The %{name} package contains a CUDA supported version of the GNU Compiler
Collection.

%package c++
Summary:        C++ support for GCC CUDA compatibility package
Requires:       %{name} = %{version}-%{release}

%description c++
The %{name} package contains a CUDA supported version of the GNU Compiler
Collection.

This package adds C++ support to the GNU Compiler Collection.

%package gfortran
Summary:        Fortran support for GCC CUDA compatibility package
Requires:       %{name} = %{version}-%{release}

%description gfortran
The %{name} package contains a CUDA supported version of the GNU Compiler
Collection.

This package adds C++ support to the GNU Compiler Collection.

%package gdb-plugin
Summary:        GCC plugin for GDB for GCC CUDA compatibility package
Requires:       %{name} = %{version}-%{release}

%description gdb-plugin
The %{name} package contains a CUDA supported version of the GNU Compiler
Collection.

This package contains a GCC plugin for GDB C expression evaluation.

%package plugin-devel
Summary:        Support for compiling GCC CUDA compatibility package plugins
Requires:       %{name} = %{version}-%{release}
Requires:       gmp-devel >= %{gmp_version}
Requires:       libmpc-devel >= %{libmpc_version}
Requires:       mpfr-devel >= %{mpfr_version}

%description plugin-devel
The %{name} package contains a CUDA supported version of the GNU Compiler
Collection.

This package contains header files and other support files for compiling GCC
plugins. The GCC plugin ABI is currently not stable, so plugins must be rebuilt
any time GCC is updated.

%prep
%autosetup -p1 -n gcc-%{version}

%build
export CFLAGS=`echo %{optflags} | sed -e 's/-Werror=format-security//g'`
export CXXFLAGS=`echo %{optflags} | sed -e 's/-Werror=format-security//g'`

# Parameter '--enable-version-specific-runtime-libs' can't be used as it
# prevents the proper include directories to be added by default to cc1/cc1plus
%configure \
    --build=%{gcc_target_platform} \
    --disable-bootstrap \
    --disable-libquadmath \
    --disable-libquadmath-support \
    --disable-libssp \
    --disable-multilib \
    --disable-shared \
    --enable-__cxa_atexit \
    --enable-languages=c,c++,fortran \
    --enable-linker-build-id \
    --enable-threads=posix \
    --program-prefix=cuda- \
    --with-system-zlib

%make_build

%install
%make_install

#mkdir -p %{buildroot}%{_includedir}/c++/%{version}
#mv %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/c++/* \
#    %{buildroot}%{_includedir}/c++/%{version}/

mv %{buildroot}%{_libdir}/*.{a,o,spec,py} \
    %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/

mv %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include-fixed/*.h \
    %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/

rm -fr \
    %{buildroot}%{_datadir}/locale \
    %{buildroot}%{_infodir}/{dir,libgomp.info,libitm.info}* \
    %{buildroot}%{_mandir}/man7/{fsf-funding,gfdl,gpl}* \
    %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include-fixed \
    %{buildroot}%{_libdir}/gcc/%{gcc_target_platform}/%{version}/install-tools \
    %{buildroot}%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/install-tools \
    %{buildroot}%{_datadir}/gcc-%{version} \

find %{buildroot} -name "*.la" -delete

# Remove binaries with full target platform in the name
rm -f %{buildroot}%{_bindir}/%{gcc_target_platform}-*

%files
%{_bindir}/%{?binary_prefix}gcc
%{_bindir}/%{?binary_prefix}gcc-ar
%{_bindir}/%{?binary_prefix}gcc-nm
%{_bindir}/%{?binary_prefix}gcc-ranlib
%{_bindir}/%{?binary_prefix}gcov
%{_bindir}/%{?binary_prefix}gcov-dump
%{_bindir}/%{?binary_prefix}gcov-tool
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{gcc_target_platform}
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{version}
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/crt*.o
%{_mandir}/man1/%{?binary_prefix}gcc.1*
%{_mandir}/man1/%{?binary_prefix}gcov.1*
%{_mandir}/man1/%{?binary_prefix}gcov-dump.1*
%{_mandir}/man1/%{?binary_prefix}gcov-tool.1*
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{gcc_target_platform}
%dir %{_libexecdir}/gcc/%{gcc_target_platform}/%{version}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/cc1
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/collect2
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/lto1
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/liblto_plugin.so*
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libasan.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libasan_preinit.o
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libatomic.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libcaf_single.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libcilkrts.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libcilkrts.spec
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgcc.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgcov.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgomp.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgomp.spec
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libitm.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libitm.spec
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/liblsan.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libmpx.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libmpx.spec
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libmpxwrappers.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libsanitizer.spec
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libtsan.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libubsan.a

# Headers
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stddef.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdarg.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdfix.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/varargs.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/float.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/limits.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdbool.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/iso646.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/syslimits.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/unwind.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdint.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdint-gcc.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdalign.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdnoreturn.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/emmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/pmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/tmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/ammintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/smmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/nmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/bmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/wmmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/immintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avxintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/x86intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/fma4intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xopintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/lwpintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/popcntintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/bmiintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/tbmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/ia32intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx2intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/bmi2intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/f16cintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/fmaintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/lzcntintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/rtmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xtestintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/adxintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/prfchwintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/rdseedintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/fxsrintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xsaveintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xsaveoptintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512cdintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512erintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512fintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512pfintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/shaintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/mm_malloc.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/mm3dnow.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/cpuid.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/cross-stdarg.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512bwintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512dqintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512ifmaintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512ifmavlintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512vbmiintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512vbmivlintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512vlbwintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512vldqintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/avx512vlintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/clflushoptintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/clwbintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/mwaitxintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xsavecintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/xsavesintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/clzerointrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/pkuintrin.h
%endif
%ifarch ia64
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/ppc-asm.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/altivec.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/spe.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/paired.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/ppu_intrinsics.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/si2vmx.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/spu2vmx.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/vec_types.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/htmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/unwind-arm-common.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/arm_neon.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/arm_acle.h
%endif
%ifarch aarch64
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/arm_neon.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/arm_acle.h
%endif
%ifarch sparc sparcv9 sparc64
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/s390intrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/htmintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/htmxlintrin.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/vecintrin.h
%endif
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/cilk
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/sanitizer

%files c++
%{_bindir}/%{?binary_prefix}c++
%{_bindir}/%{?binary_prefix}cpp
%{_bindir}/%{?binary_prefix}g++
%{_mandir}/man1/%{?binary_prefix}cpp.1*
%{_mandir}/man1/%{?binary_prefix}g++.1*
%dir %{_includedir}/c++
%dir %{_includedir}/c++/%{version}
%{_includedir}/c++/%{version}/[^gjos]*
%{_includedir}/c++/%{version}/os*
%{_includedir}/c++/%{version}/s[^u]*
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/cc1plus
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libstdc++.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libstdc++.a-gdb.py
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libstdc++fs.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libsupc++.a

# Headers
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/omp.h
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/include/openacc.h

%files gfortran
%{_bindir}/%{?binary_prefix}gfortran
%{_mandir}/man1/%{?binary_prefix}gfortran.1*
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/finclude
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/f951
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgfortran.a
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/libgfortran.spec

%files gdb-plugin
%{_libdir}/libcc1.so*
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{version}/plugin
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/plugin/libcc1plugin.so*

%files plugin-devel
%dir %{_libdir}/gcc/%{gcc_target_platform}/%{version}/plugin
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/plugin/gtype.state
%{_libdir}/gcc/%{gcc_target_platform}/%{version}/plugin/include
%{_libexecdir}/gcc/%{gcc_target_platform}/%{version}/plugin

%changelog
* Mon Dec 11 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-2
- Disable quadmath support.

* Tue Oct 10 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-1
- First build.