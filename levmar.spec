#define debug_package %{nil}

%define major 2
%define minor 6

%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# BLAS lib
%global blaslib flexiblas

# _with = default off, _without = default on
%bcond_without demo

Summary:	Levenberg-Marquardt nonlinear least squares algorithms in C/C++
Name:		levmar
Version:	%{major}.%{minor}
Release:	2
Group:		Sciences/Mathematics
License:	GPLv2+
URL:		https://users.ics.forth.gr/~lourakis/%{name}/
Source0:	http://users.ics.forth.gr/~lourakis/%{name}/%{name}-%{version}.tgz
Patch0:		%{name}-2.6-shared.patch

BuildRequires:	cmake ninja
BuildRequires:	chrpath
%if %{with demo}
BuildRequires:	f2c
%endif
BuildRequires:	pkgconfig(%{blaslib})
BuildRequires:	pkgconfig(lapack)

%description
# from README.txt
levmaris a copylefted C/C++ implementation of the Levenberg-Marquardt
non-linear least squares algorithm. levmar includes double and single
precision LM versions, both with analytic and finite difference
approximated Jacobians. levmar also has some support for constrained
non-linear least squares, allowing linear equation, box and linear
inequality constraints.

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Levenberg-Marquardt nonlinear least squares algorithms in C/C++
Group:		Sciences/Mathematics

%description -n %{libname}
# from README.txt
levmaris a copylefted C/C++ implementation of the Levenberg-Marquardt
non-linear least squares algorithm. levmar includes double and single
precision LM versions, both with analytic and finite difference
approximated Jacobians. levmar also has some support for constrained
non-linear least squares, allowing linear equation, box and linear
inequality constraints.

%files -n %{libname}
%license LICENSE
%doc README.txt
%if %{with demo}
%{_bindir}/lmdemo
%endif
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%license LICENSE
%doc README.txt
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake -Wno-dev \
	-DLINSOLVERS_RETAIN_MEMORY:BOOL=OFF \
	-DNEED_F2C:BOOL=OFF \
	-DBUILD_DEMO:BOOL=%{?with_demo:ON}%{!?with_demo:OFF} \
	-DLAPACKBLAS_LIB_NAMES:STRING=%{blaslib} \
	-DLAPACKBLAS_DIR:PATH=%{_libdir} \
	-DVERSION_MAJOR:INTEGER=%{major} \
	-DVERSION_MINOR:INTEGER=%{minor} \
	-G Ninja
%ninja_build

%install
#cmkae_install -C build

# header
install -dm 755 %{buildroot}%{_includedir}/
install -pm 644 %{name}.h %{buildroot}%{_includedir}/

# libs
install -dm 755 %{buildroot}%{_libdir}/
install -pm 755 %{_vpath_builddir}/lib%{name}.so.%{major}.%{minor} %{buildroot}%{_libdir}/
ln -s "lib%{name}.so.%{major}.%{minor}" "%{buildroot}%{_libdir}/lib%{name}.so.%{major}"
ln -s "lib%{name}.so.%{major}.%{minor}" "%{buildroot}%{_libdir}/lib%{name}.so"

# demo
%if %{with demo}
install -dm 755 %{buildroot}%{_bindir}/
install -pm 755 %{_vpath_builddir}/lmdemo %{buildroot}%{_bindir}/
chrpath --delete "%{buildroot}%{_bindir}/lmdemo"
%endif

# pkg-config
install -dm 755 %{buildroot}%{_libdir}/pkgconfig/
cat << EOF > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}
libdir=%{_libdir}

Name: %{name}
Description: Levenberg-Marquardt nonlinear least squares algorithms in C/C++
Version: %{version}
Requires: %{blaslib}
Libs: -L\${libdir} -l%{name} -lm
Cflags: -I\${includedir}
EOF

%check
pushd %{_vpath_builddir}
LD_PATH="$PWD $LD_PATH"\
./lmdemo
popd

