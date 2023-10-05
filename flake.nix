{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils"; # loop over systems
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      ( system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };
          my-python-packages = python-packages: with python-packages; [
            virtualenv
          ];
          python-with-my-packages = pkgs.python311.withPackages my-python-packages;
        in
        with pkgs;
        { devShells.default = pkgs.mkShell {
            packages = [
              pkg-config
              python-with-my-packages
              libxml2
              libxslt
            ];
          };
        }
      );
}
