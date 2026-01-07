Name:           count-files
Version:        1.0
Release:        1%{?dist}
Summary:        Script to count regular files in /etc

License:        MIT
URL:            https://github.com/roma4aliy/linux-lab-scripts
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       bash
Requires:       coreutils
Requires:       findutils

%description
A Bash script that counts the number of regular files
in the /etc directory, excluding directories and symbolic links.

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 count_files %{buildroot}%{_bindir}/count_files

%files
%{_bindir}/count_files

%changelog
* Thu Dec 18 2025 Your Name <email@example.com> - 1.0-1
- Initial package release
