%global __provides_exclude_from (%{_libdir}|%{_libexecdir})/gcc/%{_target_platform}/%{version}/
%global __requires_exclude_from (%{_libdir}|%{_libexecdir})/gcc/%{_target_platform}/%{version}/

%global _lto_cflags %{nil}
%global _warning_options -Wall -Wno-error=missing-include-dirs
%global _configure ../configure

Name:           cuda-gcc
Version:        12.3.0
Release:        2%{?dist}
Summary:        GNU Compiler Collection CUDA compatibility package
License:        GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:            http://gcc.gnu.org

# Platforms supported by CUDA:
BuildArch:      aarch64 x86_64 ppc64le

%if 0%{?snapshot:1}
Source0:        https://gcc.gnu.org/pub/gcc/snapshots/%{snapshot}/gcc-%{snapshot}.tar.xz
%else
Source0:        http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
%endif

BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel >= 6.1.0
BuildRequires:  isl-devel >= 0.16.1
BuildRequires:  libmpc-devel >= 1.0.3
BuildRequires:  mpfr-devel >= 3.1.4
BuildRequires:  zlib-devel

Requires:       binutils

# Disable annobin
%undefine _annotated_build

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

This package adds Fortran support to the GNU Compiler Collection.

%prep
%if 0%{?snapshot:1}
%autosetup -p1 -n gcc-%{snapshot}
%else
%autosetup -p1 -n gcc-%{version}
%endif

%build
mkdir objdir
pushd objdir

%configure \
    --build=%{_target_platform} \
    --target=%{_target_platform} \
    --disable-bootstrap \
    --disable-libsanitizer \
    --disable-libssp \
    --disable-multilib \
    --enable-__cxa_atexit \
    --enable-languages=c,c++,fortran \
    --enable-libquadmath \
    --enable-libquadmath-support \
    --enable-linker-build-id \
    --enable-threads=posix \
    --enable-version-specific-runtime-libs \
    --with-system-zlib

%make_build

popd

%install
pushd objdir
%make_install
popd

mv %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/include-fixed/*.h \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/include/

mv %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{_lib}/* \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/

rm -fr \
    %{buildroot}%{_bindir}/%{_target_platform}-* \
    %{buildroot}%{_datadir}/locale \
    %{buildroot}%{_infodir}/{dir,libgomp.info,libitm.info,cpp.info,cppinternals.info,gcc.info,gccinstall.info,gccint.info,gfortran.info}* \
    %{buildroot}%{_mandir}/man* \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/include-fixed \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/install-tools \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{version}/plugin \
    %{buildroot}%{_libdir}/gcc/%{_target_platform}/%{_lib}/ \
    %{buildroot}%{_libdir}/libcc1.so* \
    %{buildroot}%{_libexecdir}/gcc/%{_target_platform}/%{version}/install-tools \
    %{buildroot}%{_libexecdir}/gcc/%{_target_platform}/%{version}/plugin

find %{buildroot} -name "*.la" -delete

# Move binaries under bin/cuda:
mv %{buildroot}%{_bindir} %{buildroot}/temp
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}/temp %{buildroot}%{_bindir}/cuda

# Always call nvcc with -ccbin parameter if this package is installed:
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh <<EOF
export NVCC_PREPEND_FLAGS='-ccbin %{_bindir}/cuda'
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh <<EOF
setenv NVCC_PREPEND_FLAGS '-ccbin %{_bindir}/cuda'
EOF

%files
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_bindir}/cuda/gcc
%{_bindir}/cuda/gcc-ar
%{_bindir}/cuda/gcc-nm
%{_bindir}/cuda/gcc-ranlib
%{_bindir}/cuda/gcov
%{_bindir}/cuda/gcov-dump
%{_bindir}/cuda/gcov-tool
%{_bindir}/cuda/lto-dump
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{_target_platform}
%dir %{_libdir}/gcc/%{_target_platform}/%{version}
%{_libdir}/gcc/%{_target_platform}/%{version}/crt*.o
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{_target_platform}
%dir %{_libexecdir}/gcc/%{_target_platform}/%{version}
%{_libexecdir}/gcc/%{_target_platform}/%{version}/cc1
%{_libexecdir}/gcc/%{_target_platform}/%{version}/collect2
%{_libexecdir}/gcc/%{_target_platform}/%{version}/lto1
%{_libexecdir}/gcc/%{_target_platform}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{_target_platform}/%{version}/liblto_plugin.so*
%ifarch ppc64le
%{_libdir}/gcc/%{_target_platform}/%{version}/ecrti.o
%{_libdir}/gcc/%{_target_platform}/%{version}/ecrtn.o
%{_libdir}/gcc/%{_target_platform}/%{version}/ncrti.o
%{_libdir}/gcc/%{_target_platform}/%{version}/ncrtn.o
%endif
%{_libdir}/gcc/%{_target_platform}/%{version}/libatomic.*
%{_libdir}/gcc/%{_target_platform}/%{version}/libcaf_single.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcc_s.*
%{_libdir}/gcc/%{_target_platform}/%{version}/libgcov.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libgomp.*
%{_libdir}/gcc/%{_target_platform}/%{version}/libitm.*
%{_libdir}/gcc/%{_target_platform}/%{version}/libquadmath.*
%{_libdir}/gcc/%{_target_platform}/%{version}/include/
%exclude %{_libdir}/gcc/%{_target_platform}/%{version}/include/ISO_Fortran_binding.h

%files c++
%{_bindir}/cuda/c++
%{_bindir}/cuda/cpp
%{_bindir}/cuda/g++
%{_libexecdir}/gcc/%{_target_platform}/%{version}/cc1plus
%{_libexecdir}/gcc/%{_target_platform}/%{version}/g++-mapper-server
%{_libdir}/gcc/%{_target_platform}/%{version}/include/c++/
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++.*
%{_libdir}/gcc/%{_target_platform}/%{version}/libstdc++fs.a
%{_libdir}/gcc/%{_target_platform}/%{version}/libsupc++.a
%{_datadir}/gcc-%{version}/python/libstdcxx

%files gfortran
%{_bindir}/cuda/gfortran
%{_libdir}/gcc/%{_target_platform}/%{version}/finclude/
%{_libdir}/gcc/%{_target_platform}/%{version}/include/ISO_Fortran_binding.h
%{_libexecdir}/gcc/%{_target_platform}/%{version}/f951
%{_libdir}/gcc/%{_target_platform}/%{version}/libgfortran.*

%changelog
* Fri Mar 31 2023 Simone Caronni <negativo17@gmail.com> - 12.2.1-2
- Re-enable libquadmath support.
- Fix rpm perl macro invocation during build and double bin path.

* Mon Mar 13 2023 Simone Caronni <negativo17@gmail.com> - 12.2.1-1
- Update to latest 12 snapshot.
- Simplify installation. If the package is installed, nvcc is always executed
  with -ccbin.

* Mon Aug 08 2022 Peter Kovář <peter.kovar@reflexion.tv> - 11.3.0-2
- Remove info files.

* Tue May 17 2022 Simone Caronni <negativo17@gmail.com> - 11.3.0-1
- Update to 11.3.0
- Simplify SPEC file.

* Fri Apr 30 2021 Simone Caronni <negativo17@gmail.com> - 9.3.0-1
- Update to 9.3.0.
- Disable LTO.
- SPEC file clean up.

* Sun Apr 07 2019 Simone Caronni <negativo17@gmail.com> - 8.3.0-1
- Update to 8.3.0.

* Thu Jan 03 2019 Simone Caronni <negativo17@gmail.com> - 7.3.1-2
- Update to 7.3.1 snapshot with backported hardening features from Fedora 27.

* Mon Aug 27 2018 Simone Caronni <negativo17@gmail.com> - 7.3.0-1
- Update to 7.3.0.

* Tue May 08 2018 Simone Caronni <negativo17@gmail.com> - 6.4.0-7
- Fix build on Fedora 28 (thanks Rok Mandeljc).

* Sun Dec 17 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-6
- Remove GDB plugin.

* Thu Dec 14 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-4
- Cleanup.

* Mon Dec 11 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-3
- Enable shared objects.

* Mon Dec 11 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-2
- Disable quadmath support.

* Tue Oct 10 2017 Simone Caronni <negativo17@gmail.com> - 6.4.0-1
- First build.
