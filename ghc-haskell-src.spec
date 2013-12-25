#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	haskell-src
Summary:	Support for manipulating Haskell source code
Summary(pl.UTF-8):	Obsługa operacji na kodzie źródłowym w Haskellu
Name:		ghc-%{pkgname}
Version:	1.0.1.5
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/haskell-src
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6bce9743d2719bb49727aeb08374b30d
URL:		http://hackage.haskell.org/package/haskell-src
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-pretty
BuildRequires:	ghc-syb
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-pretty-prof
BuildRequires:	ghc-syb-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-pretty
Requires:	ghc-syb
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The haskell-src package provides support for manipulating Haskell
source code. The package provides a lexer, parser and pretty-printer,
and a definition of a Haskell abstract syntax tree (AST). Common uses
of this package are to parse or generate Haskell 98 code.

%description -l pl.UTF-8
Pakiet haskell-src zapewnia obsługę operacji na kodzie źródłowym w
Haskellu. Zawiera analizator leksykalny i składniowy, funkcję
wypisującą oraz definicję abstrakcyjnego drzewa składniowego (AST) dla
Haskella. Najczęstsze zastosowania tego pakietu to analiza i
generowanie kodu w Haskellu 98.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-pretty-prof
Requires:	ghc-syb-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
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
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HShaskell-src-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
