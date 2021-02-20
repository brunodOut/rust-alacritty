# Generated by rust2rpm 16
# Fedora 33 comes with ncurses 6.2 which includes terminfo for alacritty.
%if 0%{?fedora} >= 33
%global build_terminfo 0
%else
%global build_terminfo 1
%endif

%bcond_without check
%global __cargo_skip_build 0

%global crate alacritty

Name:           rust-%{crate}
Version:        0.7.2
Release:        1%{?dist}
Summary:        Fast, cross-platform, OpenGL terminal emulator

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            https://crates.io/crates/alacritty
Source:         %{crates_source}
Source1:        https://github.com/alacritty/alacritty/archive/v%{version}/alacritty-github-sources-%{version}.tar.gz

# Initial patched metadata:
# - remove windows and macos targets
Patch0:         alacritty-fix-metadata.diff

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  desktop-file-utils

%global _description %{expand:
Fast, cross-platform, OpenGL terminal emulator.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
# * ASL 2.0
# * ASL 2.0 and MIT
# * ASL 2.0 or Boost
# * ASL 2.0 or MIT
# * BSD
# * CC0
# * ISC
# * MIT
# * MIT or ASL 2.0
# * Unlicense or MIT
# * WTFPL
# * zlib
# * zlib or ASL 2.0 or MIT
License:        ASL 2.0 and BSD and CC0 and ISC and MIT and WTFPL and zlib

%if !%{build_terminfo}
BuildRequires:  ncurses >= 6.2
%endif

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE-APACHE
%doc README.md
%dir %{_datadir}/%{crate}
%{_bindir}/%{crate}
%{_mandir}/man1/alacritty.1*
%{_datadir}/applications/Alacritty.desktop
%{_datadir}/pixmaps/Alacritty.svg
%{_datadir}/%{crate}/alacritty.yml
%if %{build_terminfo}
%{_datadir}/terminfo/a/alacritty*
%endif
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/alacritty
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_alacritty
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/alacritty.fish

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# Provides post build files for:
# - Desktop Entry
# - Manual Pages
# - Terminfo
# - Shell Completions
# - Application Config File
tar -xzvf %{SOURCE1}
cp -a %{crate}-%{version_no_tilde}/alacritty.yml ..
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/linux/Alacritty.desktop \
    %{buildroot}%{_datadir}/applications/Alacritty.desktop
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/logo/alacritty-term.svg \
    %{buildroot}%{_datadir}/pixmaps/Alacritty.svg
install -p -D -m644 %{crate}-%{version_no_tilde}/alacritty.yml \
    %{buildroot}%{_datadir}/%{crate}/alacritty.yml
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/completions/alacritty.bash \
    %{buildroot}%{_datadir}/bash-completion/completions/%{crate}
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/completions/_alacritty \
    %{buildroot}%{_datadir}/zsh/site-functions/_alacritty
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/completions/alacritty.fish \
    %{buildroot}%{_datadir}/fish/vendor_completions.d/alacritty.fish
install -p -D -m644 %{crate}-%{version_no_tilde}/extra/alacritty.man \
    %{buildroot}%{_mandir}/man1/alacritty.1

%if %{build_terminfo}
tic -xe alacritty,alacritty-direct %{crate}-%{version_no_tilde}/extra/alacritty.info \
    -o %{buildroot}%{_datadir}/terminfo
%endif

%if %{with check}
%check
desktop-file-validate %{buildroot}%{_datadir}/applications/Alacritty.desktop
%cargo_test
%endif

%changelog
* Sat Feb 20 15:45:00 CET 2021 returntrip <stefano@figura.im> - 0.7.2-1
- Update to 0.7.2 (Fixes RHZB#1930981)

* Sat Feb 6 12:25:00 CET 2021 returntrip <stefano@figura.im> - 0.7.1-1
- Update to 0.7.1 (Fixes RHZB#1914242)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 13:27:02 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.6.0-2
- Rebuild

* Sun Nov 29 17:30:00 CEST 2020 returntrip <stefano@figura.im> - 0.6.0-1
- Update to 0.6.0

* Fri Oct 16 13:45:04 CEST 2020 returntrip <stefano@figura.im> - 0.5.0-1
- Initial package
