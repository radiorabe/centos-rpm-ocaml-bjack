%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:     ocaml-bjack


Version:  0.1.5
Release:  1
Summary:  OCaml blocking JACK API
License:  LGPLv2
URL:      https://github.com/savonet/ocaml-bjack
Source0:  https://github.com/savonet/ocaml-bjack/releases/download/%{version}/ocaml-bjack-%{version}.tar.gz

BuildRequires: libsamplerate-devel
BuildRequires: ocaml
BuildRequires: ocaml-findlib
BuildRequires: jack-audio-connection-kit-devel


%description
OCaml blocking JACK API

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       jack-audio-connection-kit-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q


%build
./bootstrap
autoconf
# USER tricks configure into not complaining about being executed as root
USER=operator ./configure \
   --prefix=%{_prefix} \
   --disable-ldconf
make -C src byte
%if %opt
make -C src opt
%endif


%install
export DESTDIR=%{buildroot}
export OCAMLFIND_DESTDIR=%{buildroot}$(ocamlfind printconf destdir)
export DLLDIR=$OCAMLFIND_DESTDIR/stublibs

install -d $OCAMLFIND_DESTDIR/%{ocamlpck}
install -d $OCAMLFIND_DESTDIR/stublibs
make install


%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/bjack
%if %opt
%exclude %{_libdir}/ocaml/bjack/*.a
%exclude %{_libdir}/ocaml/bjack/*.cmxa
%exclude %{_libdir}/ocaml/bjack/*.cmx
%endif
%exclude %{_libdir}/ocaml/bjack/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%defattr(-,root,root,-)
%doc README
%if %opt
%{_libdir}/ocaml/bjack/*.a
%{_libdir}/ocaml/bjack/*.cmxa
%{_libdir}/ocaml/bjack/*.cmx
%endif
%{_libdir}/ocaml/bjack/*.mli
