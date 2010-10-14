%define builtin_release_name Beta2
%define product_family FrameOS
%define base_release_version 5.5
%define builtin_release_variant Server
%define builtin_release_version %{base_release_version}
%define real_release_version %{?release_version}%{!?release_version:%{builtin_release_version}}
%define real_release_name %{?release_name}%{!?release_name:%{builtin_release_name}}
%define product_family FrameOS

%define current_arch %{_arch}

Summary: %{product_family} release file
Name: frameos-release
Epoch: 10
Version: 5
Release: 6.b2.el5.frameos
License: GPL
Group: System Environment/Base
Source: frameos-release-%{builtin_release_version}.tar.gz
Patch: centos-release-skip-eula.patch

Obsoletes: rawhide-release redhat-release-as redhat-release-es redhat-release-ws redhat-release-de comps 
Obsoletes: rpmdb-redhat redhat-release whitebox-release fedora-release sl-release enterprise-release
Provides: frameos-release centos-release redhat-release yumconf
Requires: frameos-release-notes

BuildRoot: %{_tmppath}/frameos-release-root

%description
%{product_family} release files

%prep
%setup -q -n frameos-release-%{builtin_release_version}
%patch -p1

%build
python -c "import py_compile; py_compile.compile('eula.py')"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
echo "%{product_family} release %{base_release_version} (%{real_release_name})" > $RPM_BUILD_ROOT/etc/redhat-release
cp $RPM_BUILD_ROOT/etc/redhat-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

mkdir -p $RPM_BUILD_ROOT/usr/share/firstboot/modules
cp eula.py* $RPM_BUILD_ROOT/usr/share/firstboot/modules

mkdir -p $RPM_BUILD_ROOT/usr/share/eula
cp eula.[!py]* $RPM_BUILD_ROOT/usr/share/eula

#mkdir -p $RPM_BUILD_ROOT/var/lib
#cp %{current_arch}/supportinfo $RPM_BUILD_ROOT/var/lib/supportinfo

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *.repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
        install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0644,root,root) /etc/redhat-release
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/*
%doc EULA GPL autorun-template
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
/usr/share/firstboot/modules/eula.py*
/usr/share/eula/eula.*
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
#/var/lib/supportinfo

%changelog
* Wed Aug 04 2010 Sergio Rubio <rubiojr@frameos.org>
- Updated to Beta 2

* Tue Jun 15 2010 Sergio Rubio <rubiojr@frameos.org>
- Initial release
