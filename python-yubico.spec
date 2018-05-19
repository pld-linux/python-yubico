#
# Conditional build:
%bcond_with	tests	# run tests (requires connected YubiKey USB device)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
#
%define		module		yubico
%define		egg_name	python_yubico
Summary:	Python 2 code for talking to Yubico's YubiKeys
Summary(pl.UTF-8):	Kod Pythona 2 do komunikacji z urządzeniami Yubico YubiKey
Name:		python-%{module}
Version:	1.3.2
Release:	1
License:	BSD
Group:		Libraries/Python
# release tarballs:
#Source0:	https://developers.yubico.com/python-yubico/Releases/%{name}-%{version}.tar.gz
Source0:	https://github.com/Yubico/python-yubico/archive/%{name}-%{version}.tar.gz
# Source0-md5:	3012d95a043b1da93486e0b555b95234
URL:		https://developers.yubico.com/python-yubico/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 2
%{?with_tests:BuildRequires:	python-pyusb}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
%{?with_tests:BuildRequires:	python3-pyusb}
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules >= 2
Requires:	python-pyusb
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 code for talking to Yubico's YubiKeys.

%description -l pl.UTF-8
Kod Pythona 2 do komunikacji z urządzeniami Yubico YubiKey.

%package -n python3-%{module}
Summary:	Python 3 code for talking to Yubico's YubiKeys
Summary(pl.UTF-8):	Kod Pythona 3 do komunikacji z urządzeniami Yubico YubiKey
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2
Requires:	python3-pyusb

%description -n python3-%{module}
Python 2 code for talking to Yubico's YubiKeys.

%description -n python3-%{module} -l pl.UTF-8
Kod Pythona 3 do komunikacji z urządzeniami Yubico YubiKey.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -type f \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -type f \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING NEWS README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif
