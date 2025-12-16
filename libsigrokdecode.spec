%define major 4
%define libname %mklibname sigrokdecode
%define devname %mklibname sigrokdecode -d
%define irmpname %mklibname libirmp0
# disable building of static libraries
%bcond static 0

%define sourcedate 20251204
%define gitcommit 71f4514

# NOTE To update this package run package-source.sh in order to create a new source
# NOTE tarball from the latest upstream git master branch.
# NOTE The script will adjust sourcedate & gitcommit defines to match created tarball.
# NOTE You may have to reload this file to see the changed values.

Name:		libsigrokdecode
%define baseversion 0.6.0
Version:	0.6.0+git%{sourcedate}.%{gitcommit}
Release:	2
Summary:	libsigrokdecode is a shared library written in C which provides the basic API for running sigrok protocol decoders.
URL:		http://www.sigrok.org
License:	GPL-3.0-or-later
Group:		Productivity/Scientific
Source0:	%{name}-%{sourcedate}-%{gitcommit}.tar.zst
#Source0:	https://sigrok.org/download/source/%%{name}/%%{name}-%%{version}.tar.gz
# Alternative GH source
#Source0:	https://github.com/sigrokproject/libsigrokdecode/archive/%%{version}/%%{name}-%%{version}.tar.gz
Patch0:		libsigrokdecode-versioned-decoders.patch


BuildRequires:	autoconf automake slibtool libtool-base
BuildRequires:	doxygen
BuildRequires:	fdupes
BuildRequires:	graphviz
BuildRequires:	make
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(glib-2.0)		>= 2.24.0
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(libsigrok)	>= 0.5.0

%description
The sigrok project aims at creating a portable, cross-platform,
Free/Libre/Open-Source signal analysis software suite that supports various
device types (such as logic analyzers, oscilloscopes, multimeters, and more).

%{name} is a shared library written in C which provides the basic
API for running sigrok protocol decoders.

The protocol decoders themselves are written in Python.

%package -n %{libname}
Summary:	libsigrokdecode is a shared library written in C which provides the basic API for running sigrok protocol decoders.
Group:		Productivity/Scientific
Requires:	python >= 3.11

%description -n %{libname}
The sigrok project aims at creating a portable, cross-platform,
Free/Libre/Open-Source signal analysis software suite that supports various
device types (such as logic analyzers, oscilloscopes, multimeters, and more).

%{name} is a shared library written in C which provides the basic
API for running sigrok protocol decoders.

The protocol decoders themselves are written in Python.

%package -n %{irmpname}
Summary:	Protocol Decoder Library for sigrok
Group:		System/Libraries

%description -n %{irmpname}
The sigrok project aims at creating a portable, cross-platform,
Free/Libre/Open-Source logic analyzer software that supports various
logic analyzer hardware products.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	python-devel >= 3.11

%description -n %{devname}
Development files (Headers etc.) for %{name}.


%prep
%autosetup -n %{name}-%{sourcedate}-%{gitcommit} -p1

%build
autoreconf -fiv
%configure \
	%{!?with_static:--disable-static}

%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%fdupes %{buildroot}%{_datadir}/%{name}-%{baseversion}/

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{irmpname} -p /sbin/ldconfig
%postun -n %{irmpname} -p /sbin/ldconfig

%files -n %{libname}
%doc README NEWS
%license COPYING
%{_libdir}/%{name}.so.%{major}*
%{_datadir}/%{name}-%{baseversion}/

%files -n %{irmpname}
%{_libdir}/libirmp*.so.*
%license COPYING

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/libirmp.so
%{_libdir}/pkgconfig/%{name}.pc
