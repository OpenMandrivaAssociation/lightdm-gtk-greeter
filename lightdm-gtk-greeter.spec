Summary:	LightDM GTK+ Greeter
Name:		lightdm-gtk-greeter
Version:	1.1.4
Release:	1
Group:		System/X11
License:	GPLv3
URL:		https://launchpad.net/lightdm-gtk-greeter
Source0:	https://launchpad.net/lightdm-gtk-greeter/+download/%{name}-%{version}.tar.gz

BuildRequires:	intltool
BuildRequires:	pkgconfig(liblightdm-gobject-1)
BuildRequires:	pkgconfig(gtk+-3.0)

Requires: gnome-themes-standard
Provides: lightdm-greeter

%description
A LightDM greeter that uses the GTK+ toolkit.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf
%{_sbindir}/lightdm-gtk-greeter
%{_datadir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop

