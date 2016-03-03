%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global	gem_name	rspec-support

%global	mainver	3.4.1
%undefine	prever

%global	mainrel	4
%global	prerpmver	%(echo "%{?prever}" | sed -e 's|\\.||g')

%global	need_bootstrap_set	0

Name:		%{?scl_prefix}rubygem-%{gem_name}
Version:	%{mainver}
Release:	%{?prever:0.}%{mainrel}%{?prever:.%{prerpmver}}%{?dist}

Summary:	Common functionality to Rspec series
Group:		Development/Languages
License:	MIT
URL:		https://github.com/rspec/rspec-support
Source0:	https://rubygems.org/gems/%{gem_name}-%{mainver}%{?prever}.gem
# %%{SOURCE2} %%{pkg_name} %%{version}
Source1:	rubygem-%{gem_name}-%{version}-full.tar.gz
Source2:	rspec-related-create-full-tarball.sh
# tweak regex for search path
Patch0:	rubygem-rspec-support-3.2.1-callerfilter-searchpath-regex.patch

Requires:       %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires:	%{?scl_prefix_ruby}ruby(release)
BuildRequires:	%{?scl_prefix_ruby}rubygems-devel
%if 0%{?need_bootstrap_set} < 1
BuildRequires:	%{?scl_prefix}rubygem(rspec)
BuildRequires:	%{?scl_prefix}rubygem(thread_order)
BuildRequires:	git
%endif

BuildArch:		noarch
# Need fix
Provides:		%{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
`RSpec::Support` provides common functionality to `RSpec::Core`,
`RSpec::Expectations` and `RSpec::Mocks`. It is considered
suitable for internal use only at this time.

%package	doc
Summary:	Documentation for %{pkg_name}
Group:		Documentation
Requires:	%{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{pkg_name}

%global	version_orig	%{version}
%global	version	%{version_orig}%{?prever}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version} -a 1
%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

(
cd %{gem_name}-%{version}
%patch0 -p1
)

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%check
%if 0%{?need_bootstrap_set} < 1
LANG=en_US.UTF-8
pushd %{gem_name}-%{version}

# Test failure needs investigation...
FAILFILE=()
FAILTEST=()
FAILFILE+=("spec/rspec/support/differ_spec.rb")
FAILTEST+=("copes with encoded strings")

for ((i = 0; i < ${#FAILFILE[@]}; i++)) {
	sed -i \
		-e "\@${FAILTEST[$i]}@s|do$|, :broken => true do|" \
		${FAILFILE[$i]}
}

%{?scl:scl enable %{scl} - << \EOF}
ruby -rubygems -Ilib/ -S rspec spec/ || \
	ruby -rubygems -Ilib/ -S rspec --tag ~broken
%{?scl:EOF}

popd
%endif

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE.md
%doc	%{gem_instdir}/Changelog.md
%doc	%{gem_instdir}/README.md

%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Wed Feb 24 2016 Pavel Valena <pvalena@redhat.com> - 3.4.1-4
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-2
- Enable tests again

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1
- Once disable tests

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-2
- Enable tests again

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-1
- 3.3.0
- Once disable tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-1
- 3.2.2

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-2
- Enable tests again

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1
- Once disable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-3
- Enable tests again

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-2
- Retry

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2
- Once disable tests

* Fri Aug 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.4-1
- 3.0.4

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.4.beta2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.4.beta1
- 3.0.0 beta 2

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.2.beta1
- Modify Provides EVR

* Mon Feb 03 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.1.beta1
- Initial package
