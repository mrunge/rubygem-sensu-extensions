# Generated from sensu-extensions-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sensu-extensions

Name:           rubygem-%{gem_name}
Version:        1.7.1
Release:        1%{?dist}
Summary:        The Sensu extension loader library
Group:          Development/Languages
License:        MIT
URL:            https://github.com/sensu/sensu-extensions
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:        https://github.com/sensu/%{gem_name}/archive/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(eventmachine)
BuildRequires:  rubygem(sensu-json) >= 1.1.0
BuildRequires:  rubygem(sensu-extension)
BuildRequires:  rubygem(sensu-logger)
BuildRequires:  rubygem(sensu-settings)
BuildRequires:  rubygem(sensu-extensions-debug) = 1.0.0
BuildRequires:  rubygem(sensu-extensions-json) = 1.0.0
BuildRequires:  rubygem(sensu-extensions-occurrences) = 1.1.0
BuildRequires:  rubygem(sensu-extensions-only-check-output) = 1.0.0
BuildRequires:  rubygem(sensu-extensions-ruby-hash) = 1.0.0
BuildRequires:  rubygem(sensu-extensions-system-profile) = 1.0.0

Requires:       rubygem(sensu-json) >= 1.1.0
Requires:       rubygem(sensu-extension)
Requires:       rubygem(sensu-logger)
Requires:       rubygem(sensu-settings)
Requires:       rubygem(sensu-extensions-debug) = 1.0.0
Requires:       rubygem(sensu-extensions-json) = 1.0.0
Requires:       rubygem(sensu-extensions-occurrences) = 1.1.0
Requires:       rubygem(sensu-extensions-only-check-output) = 1.0.0
Requires:       rubygem(sensu-extensions-ruby-hash) = 1.0.0

BuildArch: noarch
%if 0%{?rhel}
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
The Sensu extension loader library.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%if 0%{?dlrn} > 0
%setup -q -D -T -n  %{dlrn_nvr}
%else
%setup -q -D -T -n  %{gem_name}-%{version}
%endif

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

install -d -p %{_builddir}%{gem_instdir}
%if 0%{?dlrn} > 0
tar -xvzf %{SOURCE1} -C %{_builddir}/%{dlrn_nvr}/%{gem_instdir} --strip-components=1 %{gem_name}-%{version}/spec
%else
tar -xvzf %{SOURCE1} -C %{_builddir}/%{gem_name}-%{version}/%{gem_instdir} --strip-components=1 %{gem_name}-%{version}/spec
%endif

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml}


# Run the test suite
%check
pushd .%{gem_instdir}
# Symlink extensions_symlinked was missing in the past, which breaks unit tests,
# see https://github.com/sensu/sensu-extensions/issues/9
# Currently extensions_symlinked is provided, but is not correct symlink,
# so we have to recreate it anyway
pushd ./spec/assets/extensions
rm -f extensions_symlinked
ln -s ../extensions_symlinked extensions_symlinked
popd

rspec -Ilib spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Dec 23 2016 Martin Mágr <mmagr@redhat.com> - 1.7.1-1
- Updated to latest upstream release

* Thu May 05 2016 Martin Mágr <mmagr@redhat.com> - 1.5.0-2
- Fixed runtime JSON dependency

* Thu May 05 2016 Martin Mágr <mmagr@redhat.com> - 1.5.0-1
- Updated to upstream version 1.5.0

* Fri Feb 26 2016 Martin Mágr <mmagr@redhat.com> - 1.4.0-1
- Updated to upstream version 1.4.0

* Tue Jan 27 2015 Graeme Gillies <ggillies@redhat.com> - 1.1.0-1
- Initial package
