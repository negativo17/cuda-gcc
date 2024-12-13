%global gcc_major 13

Name:           cuda-gcc
Version:        13.3.1
Release:        1%{?dist}
Summary:        GNU Compiler Collection CUDA compatibility package
License:        BSD
URL:            http://gcc.gnu.org

BuildArch:      noarch

Requires:       gcc%{gcc_major}-c++

Provides:       cuda-gcc = %{version}-%{release}
Obsoletes:      cuda-gcc < %{version}-%{release}
Provides:       cuda-gcc-c++ = %{version}-%{release}
Obsoletes:      cuda-gcc-c++ < %{version}-%{release}
Provides:       cuda-gcc-gfortran = %{version}-%{release}
Obsoletes:      cuda-gcc-gfortran < %{version}-%{release}

%description
The %{name} package contains scripts that are sourced in the environment to use
the GCC compatibility packages when invoking NVCC.

%install
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh <<EOF
export NVCC_CCBIN='g++-%{gcc_major}'

# Alternatively you can use the following:
export NVCC_PREPEND_FLAGS='-ccbin %{_bindir}/g++-%{gcc_major}'
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh <<EOF
setenv NVCC_CCBIN 'g++-%{gcc_major}'

# Alternatively you can use the following:
setenv NVCC_PREPEND_FLAGS '-ccbin %{_bindir}/g++-%{gcc_major}'
EOF

%files
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.csh
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.sh

%changelog
* Fri Dec 13 2024 Simone Caronni <negativo17@gmail.com> - 13.3.1-1
- There is no need anymore for a custom GCC package, as Fedora ships gcc13 as a
  compatibility package. Adjust accordingly. This package is just now a profile.

* Wed Jul 10 2024 Simone Caronni <negativo17@gmail.com> - 13.3.0-1
- Update to 13.3.0.

* Mon Mar 25 2024 Simone Caronni <negativo17@gmail.com> - 12.3.0-2
- Fix library exclusions.

* Sat Jun 03 2023 Simone Caronni <negativo17@gmail.com> - 12.3.0-1
- Update to 12.3.0.
- Adjust binary move.

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
