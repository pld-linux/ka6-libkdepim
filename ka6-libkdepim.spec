#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.05.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkdepim
Summary:	libkdepim
Name:		ka6-%{kaname}
Version:	24.05.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7d13e67866a1b0d8e8d022209dd64694
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Designer-devel
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6UiTools-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-contacts-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-mime-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-search-devel >= %{kdeappsver}
BuildRequires:	ka6-kldap-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwallet-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for common kdepim apps.

%description -l pl.UTF-8
Biblioteka wspólna dla aplikacji kdepim.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname}_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}_qt.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6Libkdepim.so.*.*
%ghost %{_libdir}/libKPim6Libkdepim.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/kdepim6widgets.so
%{_datadir}/dbus-1/interfaces/org.kde.addressbook.service.xml
%{_datadir}/dbus-1/interfaces/org.kde.mailtransport.service.xml
%{_datadir}/qlogging-categories6/libkdepim.categories
%{_datadir}/qlogging-categories6/libkdepim.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/Libkdepim
%{_libdir}/cmake/KPim6Libkdepim
%{_libdir}/cmake/KPim6MailTransportDBusService
%{_libdir}/libKPim6Libkdepim.so
