let
  pkgs = import <nixpkgs> {};
  stdenv = pkgs.stdenv;
in pkgs.mkShell {
  LD_LIBRARY_PATH="${stdenv.cc.cc.lib}/lib/";
  buildInputs = [
    pkgs.python311
  ];
  shellHook = ''
    fish -c 'source venv/bin/activate.fish'
  '';

  shell = pkgs.fish;
}
