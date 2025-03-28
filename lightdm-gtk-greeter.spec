%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

Summary:	The Light Display Manager (GTK+ greeter)
Name:		lightdm-gtk-greeter
Version:	2.0.9
Release:	2
License:	GPLv3
Group:		Graphical desktop/Other
Url:		https://www.freedesktop.org/wiki/Software/LightDM
Source0:	https://github.com/Xubuntu/lightdm-gtk-greeter/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
# Old sources
#Source0:	https://launchpad.net/%{name}/%{url_ver}/%{version}/+download/%{name}-%{version}.tar.gz
Patch2:		lightdm-gtk-greeter-2.0.2-omv.patch
BuildRequires:	intltool >= 0.35.0
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(liblightdm-gobject-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	gnome-common
BuildRequires:	xfce4-dev-tools
# Optional
BuildRequires:	pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:	pkgconfig(ayatana-indicator3-0.4)
BuildRequires:	pkgconfig(libayatana-ido3-0.4)
BuildRequires:	pkgconfig(libxklavier)

%description
A LightDM greeter that uses the GTK+ toolkit.

%package common
Summary:	Common files for the Light Display Manager
Group:		Graphical desktop/Other
BuildArch:	noarch
# For mga logo:
Requires:	desktop-common-data
# For icons in top right corner
Requires:	gnome-icon-theme
Conflicts:	%{name} < 1.6.0-6

%description common
This package contains the common files for the Light Display Manager.

%package -n lightdm-gtk3-greeter
Summary:	The Light Display Manager (GTK3 greeter)
Group:		Graphical desktop/Other
Provides:	lightdm-greeter
Requires:	lightdm-gtk-greeter-common = %{version}-%{release}
Requires:	lightdm
Requires(pre,post,postun):	update-alternatives
Obsoletes:	%{name} < 1.6.0-6
# GTK2 greeter was removed
Obsoletes:	lightdm-gtk2-greeter < 2.0.0

%description -n lightdm-gtk3-greeter
A LightDM greeter that uses the GTK3 toolkit.

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure
%make_build

%install
%make_install

# rename gtk3 greeter
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/lightdm-gtk3-greeter

# install .desktop files
mv %{buildroot}%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop \
	%{buildroot}%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop

# fix .desktop files
sed -i -e 's,%{name},lightdm-gtk3-greeter,g' %{buildroot}%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop

# handle docs in files section
rm -rf %{buildroot}%{_docdir}

%find_lang %{name}

%post -n lightdm-gtk3-greeter
%{_sbindir}/update-alternatives \
        --install %{_datadir}/xgreeters/lightdm-greeter.desktop \
        lightdm-greeter \
        %{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop \
        20

%postun	-n lightdm-gtk3-greeter
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
        --remove lightdm-greeter \
        %{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop
fi


%files common -f %{name}.lang
%doc NEWS
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_iconsdir}/hicolor/scalable/places/*.svg

%files -n lightdm-gtk3-greeter
%{_sbindir}/lightdm-gtk3-greeter
%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop

