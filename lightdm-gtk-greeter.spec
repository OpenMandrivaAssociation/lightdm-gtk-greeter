%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	The Light Display Manager (GTK+ greeter)
Name:		lightdm-gtk-greeter
Version:	1.8.5
Release:	1
License:	GPLv3
Group:		Graphical desktop/Other
Url:		http://www.freedesktop.org/wiki/Software/LightDM
Source0:	https://launchpad.net/%{name}/%{url_ver}/%{version}/+download/%{name}-%{version}.tar.gz
Patch0:		lightdm-gtk-greeter_customizations.patch
BuildRequires:	intltool >= 0.35.0
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(liblightdm-gobject-1)
BuildRequires:	pkgconfig(x11)

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
# For icons in HighContrast mode
Requires:	gnome-themes-standard
Conflicts:	%{name} < 1.6.0-6

%description common
This package contains the common files for the Light Display Manager.

%package -n lightdm-gtk2-greeter
Summary:	The Light Display Manager (GTK2 greeter)
Group:		Graphical desktop/Other
Provides:	lightdm-greeter
Requires:	lightdm-gtk-greeter-common = %{version}-%{release}
Requires:	lightdm
Requires(pre,post,postun):	update-alternatives
Obsoletes:	%{name} < 1.6.0-6

%description -n lightdm-gtk2-greeter
A LightDM greeter that uses the GTK2 toolkit.

%package -n lightdm-gtk3-greeter
Summary:	The Light Display Manager (GTK3 greeter)
Group:		Graphical desktop/Other
Provides:	lightdm-greeter
Requires:	lightdm-gtk-greeter-common = %{version}-%{release}
Requires:	lightdm
Requires(pre,post,postun):	update-alternatives
Obsoletes:	%{name} < 1.6.0-6

%description -n lightdm-gtk3-greeter
A LightDM greeter that uses the GTK3 toolkit.

%prep
%setup -q
%apply_patches

# create dirs fro gtk2/gtk3 build
mkdir -p gtk2 gtk3

%build
export CONFIGURE_TOP=..
pushd gtk2
	%configure2_5x \
		--disable-static \
		--with-gtk2
	%make
popd

pushd gtk3
        %configure2_5x \
                --disable-static
	%make
popd

%install
%makeinstall_std -C gtk2

# rename gtk2 greeter
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/lightdm-gtk2-greeter

# install gtk3 greeter
install -Dpm755 gtk3/src/%{name} %{buildroot}%{_sbindir}/lightdm-gtk3-greeter

# install .desktop files
install -Dpm644	%{buildroot}%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop \
	%{buildroot}%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
install -Dpm644 %{buildroot}%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop \
	%{buildroot}%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop
rm -rf %{buildroot}%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop

# fix .desktop files
sed -i -e 's,%{name},lightdm-gtk2-greeter,g' %{buildroot}%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
sed -i -e 's,%{name},lightdm-gtk3-greeter,g' %{buildroot}%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop

# handle docs in files section
rm -rf %{buildroot}%{_docdir}

%find_lang %{name}

%pre -n lightdm-gtk2-greeter
if [ -f %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop ]; then
	%{_sbindir}/update-alternatives \
		--remove lightdm-greeter \
	        %{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
fi

%post -n lightdm-gtk2-greeter
%{_sbindir}/update-alternatives \
	--install %{_datadir}/xgreeters/lightdm-greeter.desktop \
	lightdm-greeter \
	%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop \
	25

%post -n lightdm-gtk3-greeter
%{_sbindir}/update-alternatives \
        --install %{_datadir}/xgreeters/lightdm-greeter.desktop \
        lightdm-greeter \
        %{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop \
        20

%postun -n lightdm-gtk2-greeter
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
	--remove lightdm-greeter \
	%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop
fi

%postun	-n lightdm-gtk3-greeter
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives \
        --remove lightdm-greeter \
        %{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop
fi


%files common -f %{name}.lang
%doc NEWS
%config(noreplace) %{_sysconfdir}/lightdm/lightdm-gtk-greeter.conf

%files -n lightdm-gtk2-greeter
%{_sbindir}/lightdm-gtk2-greeter
%{_datadir}/xgreeters/lightdm-gtk2-greeter.desktop

%files -n lightdm-gtk3-greeter
%{_sbindir}/lightdm-gtk3-greeter
%{_datadir}/xgreeters/lightdm-gtk3-greeter.desktop

