%define	pkgname	haskell-src
Summary:	Support for manipulating Haskell source code
Name:		ghc-%{pkgname}
Version:	1.0.1.4
Release:	0.1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	32d181c082393ab859e72610803bac6e
URL:		http://hackage.haskell.org/package/%{pkgname}/
BuildRequires:	ghc >= 6.12.3
%requires_releq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ghcdir		ghc-%(/usr/bin/ghc --numeric-version)

%description
The haskell-src package provides support for manipulating Haskell
source code. The package provides a lexer, parser and pretty-printer,
and a definition of a Haskell abstract syntax tree (AST).
Common uses of this package are to parse or generate Haskell 98 code. 

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/ghc-pkg recache

%postun
/usr/bin/ghc-pkg recache

%files
%defattr(644,root,root,755)
%doc NEWS
%doc %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}
