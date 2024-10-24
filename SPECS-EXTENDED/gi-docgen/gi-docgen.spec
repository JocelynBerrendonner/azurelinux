Summary:        Documentation tool for GObject-based libraries
Name:           gi-docgen
Version:        2024.1
Release:        1%{?dist}
# Based on the “Copyright and Licensing terms” in README.md, on the contents of
# .reuse/dep5, and on inspection of SPDX headers or other file contents with
# assistance from licensecheck.
#
# The entire source is (Apache-2.0 OR GPL-3.0-or-later) except the following files that are
# packaged or are used to generate packaged files:
#
# (Apache-2.0 OR GPL-3.0-or-later) AND BSD-2-Clause:
#   - gidocgen/mdext.py
#
# MIT:
#   - gidocgen/templates/basic/fzy.js
#   - gidocgen/templates/basic/solarized-{dark,light}.js
#
# CC0-1.0:
#   - gi-docgen.pc.in (from which gi-docgen.pc is generated)
#   - gidocgen/templates/basic/*.png
#   - docs/CODEOWNERS (-doc subpackage)
#   - examples/*.toml (-doc subpackage)
#
# Note that CC0-1.0 is allowed in Fedora for content only; all of the above
# files may reasonably be called content.
#
# Additionally, CC0-1.0 appears in certain sample configuration snippets within
# the following files, which are otherwise (Apache-2.0 OR GPL-3.0-or-later):
#   - docs/project-configuration.rst
#   - docs/tutorial.rst
# On one hand, these are copied from real projects; on the other hand, they are
# very trivial. It’s not obvious whether they should be considered “real”
# CC0-1.0 content or not.
#
# The identifier LGPL-2.1-or-later also appears in a sample configuration
# template in docs/tutorial.rst, but the configuration in question is filled
# with placeholder values and is not copied from a real project, so it’s
# reasonable to consider LGPL-2.1-or-later a placeholder rather than a real
# license as well.
#
# -----
#
# Additionally, the following sources are under licenses other than (Apache-2.0
# OR GPL-3.0-or-later), but are not packaged in any of the binary RPMs:
#
# CC0-1.0:
#   - .editorconfig (not installed)
#   - .gitlab-ci.yml (not installed)
#   - gi-docgen.doap (not installed)
#   - MANIFEST.in (not installed)
#   - pytest.ini (not installed; test only)
#   - tests/data/config/*.toml (not installed; test only)
#
# CC-BY-SA-3.0:
#   - docs/gi-docgen.{png,svg} (for HTML docs; not currently packaged)
#   - code-of-conduct.md (not installed)
#
# OFL-1.1:
#   - gidocgen/templates/basic/*.{woff,woff2} (removed in prep)
#
# GPL-2.0-or-later:
#   - tests/data/gir/{Utility-1.0,Regress-1.0}.gir (not installed; test only)
#
# LGPL-2.0-or-later:
#   - tests/data/gir/{GLib,GObject,Gio}-2.0.gir (not installed; test only)
#
# LGPL-2.0-or-later OR MPL-1.1:
#   - tests/data/gir/cairo-1.0.gir (not installed; test only)
License:        %{shrink:
                (Apache-2.0 OR GPL-3.0-or-later) AND
                BSD-2-Clause AND
                MIT AND
                CC0-1.0
                }
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.gnome.org/GNOME/gi-docgen
Source:         %{url}/-/archive/%{version}/gi-docgen-%{version}.tar.bz2
# We are prohibited from bundling fonts, and we are prohibited from shipping
# fonts in web font formats; see
# https://docs.fedoraproject.org/en-US/packaging-guidelines/FontsPolicy/#_web_fonts.
#
# Since upstream uses *only* web fonts, we need a patch. We haven’t offered it
# upstream since upstream has no reason NOT to use web fonts.
#
# This patch removes all references to WOFF/WOFF2 font files (which we still
# must remove in %%prep) and ensures the CSS correctly references corresponding
# or stand-in local system fonts.
Patch0:         gi-docgen-2022.2-no-web-fonts.patch
# Unbundling fonts:
BuildRequires:  freefont
BuildRequires:  python3-devel
BuildRequires:  python3-markdown
BuildRequires:  python3-markupsafe
BuildRequires:  python3-pip
BuildRequires:  python3-typogrify
BuildRequires:  python3-wheel
BuildRequires:  python3dist(pytest)
# Unbundling fonts:
Requires:       gi-docgen-fonts = %{version}-%{release}
# Trivial fork of https://github.com/jhawthorn/fzy.js (looks like it was
# basically just wrapped in an IIFE). Given that modification, it’s not clear
# how we could unbundle it, either downstream or with some kind of upstream
# support.
#
# It’s not clear what version was used for the fork.
Provides:       bundled(js-fzy)
BuildArch:      noarch

%description
GI-DocGen is a document generator for GObject-based libraries. GObject is the
base type system of the GNOME project. GI-Docgen reuses the introspection data
generated by GObject-based libraries to generate the API reference of these
libraries, as well as other ancillary documentation.

GI-DocGen is not a general purpose documentation tool for C libraries.

While GI-DocGen can be used to generate API references for most GObject/C
libraries that expose introspection data, its main goal is to generate the
reference for GTK and its immediate dependencies. Any and all attempts at
making this tool more generic, or to cover more use cases, will be weighted
heavily against its primary goal.

GI-DocGen is still in development. The recommended use of GI-DocGen is to add
it as a sub-project to your Meson build system, and vendor it when releasing
dist archives.

You should not depend on a system-wide installation until GI-DocGen is declared
stable.

%package fonts
Summary:        Metapackage providing fonts for gi-docgen output
# Really, there is nothing copyrightable in this metapackage, so we give it the
# overall license of the project.
License:        Apache-2.0 OR GPL-3.0-or-later
Requires:       freefont

%description fonts
Because web fonts from upstream are not bundled in the gi-docgen package,
documentation packages generated with gi-docgen must depend on this metapackage
to ensure the proper system fonts are present.

%package doc
Summary:        Documentation for gi-docgen
License:        (Apache-2.0 OR GPL-3.0-or-later) AND CC0-1.0

%description doc
Documentation for gi-docgen.

%{generate_buildrequires}
%{pyproject_buildrequires}

%prep
%autosetup -p1

# Remove all bundled fonts. See gi-docgen-*-no-web-fonts.patch.
find . -type f \( -name '*.woff' -o -name '*.woff2' \) -print -delete


%build
%{pyproject_wheel}


%install
%{pyproject_install}
%pyproject_save_files gidocgen

install -t '%{buildroot}%{_pkgdocdir}' -D -m 0644 -p \
    CHANGES.md \
    CONTRIBUTING.md \
    docs/CODEOWNERS \
    README.md
cp -rp examples '%{buildroot}%{_pkgdocdir}/'


%check
%pytest


%files -f %{pyproject_files}
%license LICENSES/ .reuse/dep5

%{_bindir}/gi-docgen
%{_mandir}/man1/gi-docgen.1*
# Normally, this would go in a -devel package, but there is little point in
# providing a -devel package for *just* the .pc file when there are no
# libraries or headers.
%{_datadir}/pkgconfig/gi-docgen.pc

%files fonts
# Empty; this is a metapackage

%files doc
%license LICENSES/ .reuse/dep5
%doc %{_pkgdocdir}/

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 2024-1
- Integrating the spec into Azure Linux
  ## START: Generated by rpmautospec

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2024.1-2
- Rebuilt for Python 3.13

* Fri May 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.1-1
- Update to 2024.1 (close RHBZ#2281806)

* Thu May 23 2024 Ray Strode <rstrode@redhat.com> - 2023.3-6
- Drop Source Code Pro dependency on RHEL

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2023.3-2
- Add patch to fix broken Since/Obsoletes

* Sun Nov 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.3-1
- Update to 2023.3 (close RHBZ#2251397)

* Sun Nov 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-10
- Package LICENSES/ as a directory

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-8
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2023.1-7
- Rebuilt for Python 3.12

* Fri Mar 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-3
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-1
- Update to 2023.1 (close RHBZ#2158850)

* Fri Dec 30 2022 Miro Hrončok <miro@hroncok.cz> - 2022.2-3
- Use tomllib (tomli) instated of deprecated python3-toml

* Fri Nov 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.2-2
- Update License to SPDX

* Fri Nov 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.2-1
- Update to 2022.2 (close RHBZ#2140725)

* Thu Nov 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-9
- Drop explicit -r for pyproject_buildrequires; no longer needed

* Thu Nov 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-8
- Drop code-of-conduct.md from the -doc subpackage

* Tue Aug 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-7
- Parallelize sphinx-build

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2022.1-5
- Rebuilt for Python 3.11

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-4
- Drop “forge” macros, which are not doing much here

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-3
- Update spec file comment

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-2
- Stop numbering patches

* Wed Feb 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-1
- Update to 2022.1 (close RHBZ#2053858)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.8-2
- Reduce LaTeX PDF build verbosity

* Thu Oct 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.8-1
- Update to 2021.8 (close RHBZ#2016447)

* Thu Oct 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-5
- Reduce macro indirection in the spec file

* Wed Sep 29 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-4
- Improve comments about test availability

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-3
- Build PDF docs instead of HTML

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-2
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Mon Aug 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-1
- Update to 2021.7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.6-1
- Initial package
## END: Generated by rpmautospec