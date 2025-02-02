{pkgs}: {
  deps = [
    pkgs.unixODBC
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
  ];
}
