%define name gdeploy
%define version master
%define release 0
%define gdeploymod ansible/modules/extras/system/glusterfs
%define gdeploytemp /usr/share/ansible/gdeploy
%define gdeploydoc /usr/share/doc/gdeploy
%define gdeploysrc http://download.gluster.org/pub/gluster/gdeploy/LATEST

Name:           %{name}
Version:        %{version}
Release:        %{?release}
Summary:        Tool to deploy and manage GlusterFS cluster

Group:          Applications/System
License:        GPLv3
URL:            http://www.redhat.com/storage
Source0:        %{gdeploysrc}/%{name}-%{version}-%{release}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       ansible >= 1.9 python >= 2.6 ecdsa >= 0.13 Jinja2 >= 2.7.3
Requires:       MarkupSafe >= 0.23 paramiko >= 1.15.2 pycrypto >= 2.6.1
Requires:       PyYAML >= 3.11


BuildRequires:  python-setuptools

%description
gdeploy is an Ansible based deployment tool. Initially gdeploy was written to
install GlusterFS clusters, eventually it grew out to do lot of other things. On
a given set of hosts, gdeploy can create physical volumes, volume groups, and
logical volumes, install packages, subscribe to RHN channels, run shell
commands, create GlusterFS volumes and lot more.

See http://gdeploy.readthedocs.io/en/latest/ for more details

%prep
%setup -q -n %{name}-%{version}-%{release}

%build
python setup.py build

%install
# Install the binary and python libraries
rm -rf %{buildroot}
python setup.py install -O1 --root=%{buildroot} --install-scripts %{_bindir}

mkdir -p %{buildroot}/%{python_sitelib}/%{gdeploymod}
install -m 755 modules/* \
    %{buildroot}/%{python_sitelib}/%{gdeploymod}

# Install the playbooks into /usr/share/ansible/gdeploy/playbooks
mkdir -p %{buildroot}/%{gdeploytemp}
cp -r playbooks %{buildroot}/%{gdeploytemp}

# Install scripts
cp -r extras/scripts %{buildroot}/%{gdeploytemp}

# Install Openshift-templates
cp -r extras/openshift-templates %{buildroot}/%{gdeploytemp}

# Documentation
mkdir -p %{buildroot}/%{gdeploydoc} %{buildroot}/%{_mandir}/man1/ \
       %{buildroot}/%{_mandir}/man5/
cp -r doc/* README.md examples %{buildroot}/%{gdeploydoc}
cp man/gdeploy.1* %{buildroot}/%{_mandir}/man1/
cp man/gdeploy.conf* %{buildroot}/%{_mandir}/man5/

%clean
rm -rf %{buildroot}

%files
%{_bindir}/gdeploy
%{python_sitelib}/gdeploylib/
%{python_sitelib}/gdeploycore/
%{python_sitelib}/gdeployfeatures/
%{python_sitelib}/%{gdeploymod}
%{gdeploytemp}
%{python_sitelib}/gdeploy-%{version}-*.egg-info/

%doc README.md
%docdir %{gdeploydoc}
%{_mandir}/man1/gdeploy*
%{_mandir}/man5/gdeploy*
%{gdeploydoc}

%changelog
* Fri Jun 3 2016 Sachidananda Urs <sac@redhat.com> 2.0-16
- Cleaning up the spec file

* Mon Feb 1 2016 Sachidananda Urs <sac@redhat.com> 2.0
- New design, refer: doc/gdeploy-2

* Fri Nov 6 2015 Sachidananda Urs <sac@redhat.com> 1.1
- Patterns in configs are to be tested
- Backend setup config changes(This includes alot)
- Rerunning the config do not throw error
- Backend reset
- Host specific and group specific changes.
- Quota
- Snapshot
- Geo-replication
- Subscription manager
- Package install
- Firewalld
- samba
- CTDB
- CIFS mount

* Mon Aug 3 2015 Sachidananda Urs <sac@redhat.com> 1.0
- Initial release.
