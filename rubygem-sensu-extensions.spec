# Generated from sensu-extensions-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sensu-extensions

Name:           rubygem-%{gem_name}
Version:        1.5.0
Release:        2%{?dist}
Summary:        The Sensu extension loader library
Group:          Development/Languages
License:        MIT
URL:            https://github.com/sensu/sensu-extensions
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(rspec)
BuildRequires:  rubygem(eventmachine)
BuildRequires:  rubygem(sensu-json) >= 1.1.0
BuildRequires:  rubygem(sensu-extension) >= 1.3.0
BuildRequires:  rubygem(sensu-logger)
BuildRequires:  rubygem(sensu-settings)
BuildRequires:  rubygem(sensu-em)
BuildRequires:  rubygem(uuidtools)

Requires:       rubygem(sensu-json) >= 1.1.0
Requires:       rubygem(sensu-extension)
Requires:       rubygem(sensu-logger)
Requires:       rubygem(sensu-settings)

BuildArch: noarch
%if 0%{?fedora} <= 20 || 0%{?el7}
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

%setup -q -D -T -n  %{gem_name}-%{version}

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

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml}


# Run the test suite
%check
pushd .%{gem_instdir}
# Disable codeclimate-test-reporter as it's not needed
sed -i '/^.*codeclimate-test-reporter.*$/d' spec/helpers.rb
sed -i /CodeClimate::TestReporter.start/d spec/helpers.rb

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
%doc %{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile

%changelog
* Thu May 05 2016 Martin Mágr <mmagr@redhat.com> - 1.5.0-2
- Fixed runtime JSON dependency

* Thu May 05 2016 Martin Mágr <mmagr@redhat.com> - 1.5.0-1
- Updated to upstream version 1.5.0

* Fri Feb 26 2016 Martin Mágr <mmagr@redhat.com> - 1.4.0-1
- Updated to upstream version 1.4.0

* Tue Jan 27 2015 Graeme Gillies <ggillies@redhat.com> - 1.1.0-1
- Initial package
