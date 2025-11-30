{
  inputs.nixpkgs2009.url =github:galtys/nixpkgs/nixos-20.03pillow;
  outputs = { self, nixpkgs2009}: 
    let
      pkgs9=nixpkgs2009.legacyPackages.x86_64-linux;
      my_py_packages=((import ./for_flake.nix) {pkgs =pkgs9;});
    in  
      {
        packages.x86_64-linux=my_py_packages;
  };
}
  
