{
  inputs.nixpkgs2009.url =github:galtys/nixpkgs/nixos-20.03pillow;
  inputs.nixpkgs24.url = github:galtys/nixpkgs/nixos-24.05;
  #inputs.flake-utils.url = github:numtide/flake-utils;
  #nix run .#openerp-server -- -c /home/jan/projects/server_pjbrefct.conf
  outputs = { self, nixpkgs2009, nixpkgs24 }: 
    let
      #mainCFG = config.services.migrated_pjb70;
      #pkgs9=removeAttrs nixpkgs2009.legacyPackages.x86_64-linux ["pillow" "psycopg2"];
      pkgs9=nixpkgs2009.legacyPackages.x86_64-linux;
      #pkgs24=nixpkgs24.legacyPackages.x86_64-linux;
      pkgs24=(import nixpkgs24 {
        system = "x86_64-linux";
        config = {
          permittedInsecurePackages = [
            "openssl-1.1.1w"
          ];
        };
      });
      #wkhtml = pkgs9.callPackage ./wk/package2.nix {};
      #wkpdf = pkgs9.callPackage ./pdf_wk/package.nix {};      
      #wkpdf = pkgs24.callPackage ./pdf_wk/package.nix {};
      my_py_packages=((import ./for_flake.nix) {pkgs =pkgs9;});
      #nixpkgs.overlays=[(final: prev: {
      #  python27 = prev.python27.override {
      #    extraPkgs = my_py_packages;
      #  };


      #} )];
      mypython = pkgs9.python27.buildEnv.override {
        #buildInputs=my_py_packages;
        extraLibs =   my_py_packages;
        #extraInputs = my_py_packages;
        ignoreCollisions = true;
      };
      
      #pj_bridgman_addons = pkgs9.python27.pkgs.buildPythonPackage rec {
      #  pname = "pj_bridgman";
      #  version = "0.0.2";
      #  # nix-prefetch-git --url git@github.com:/galtys/pj_bridgman.git --rev 1c597249d49a607763871662753765478af1ecd7
      #  src = pkgs9.fetchFromGitHub {
      #      rev = "1c597249d49a607763871662753765478af1ecd7";
      #      owner = "galtys";
      #      repo = "pj_bridgman";
      #   	 sha256 = "0298ll1y3ya631mjnkb0msdq9h0av85qi9l1h59r26sn4a32rp6b";
      #  };
        
      #};
      migrated_pjb70 = pkgs9.python27.pkgs.buildPythonPackage rec {
        pname = "openerp-server";
        version = "1.1.1";
        #nix-prefetch-git --url https://github.com/galtys/odoo.git --rev c285b25954eac9e85e4fbdd35d916fd7b36ff925
        src = pkgs9.fetchFromGitHub {
            rev = "c285b25954eac9e85e4fbdd35d916fd7b36ff925";
            owner = "galtys";
            repo = "odoo";
         	 sha256 = "1fsflsp1kd9k0k764agb503hb09nravf58cbk7wxnnii8zg8xsfd";
        };
        #src = /home/jan/github.com/migrated_pjb70;
        #postPatch = ''
        #  # don't test bash builtins
        #  rm testing/test_argcomplete.py
        #'';
        doCheck = false;
        #checkInputs = [ hypothesis ];
        #nativeBuildInputs = [ setuptools_scm ];
        propagatedBuildInputs = my_py_packages;

        python = mypython;
        #meta = with lib; {
        #  maintainers = with maintainers; [ ];
        #  description = "Framework for writing tests";
        #};
      };
      pjberp7Module = import ./.;
      
    in  
      {
        #pkgs=nixpkgs2009.legacyPackages.${system};
        # Notice the reference to nixpkgs here
        packages.x86_64-linux.pjbenv=
        with import nixpkgs2009 { system = "x86_64-linux"; };
        stdenv.mkDerivation rec {
          name = "migrated_pjb70_env";
          src = self;
          buildInputs = [mypython pkgs.python27.pkgs.ipython pkgs24.wkhtmltopdf-bin pkgs.ghostscript pkgs24.dbeaver-bin];#  pkgs.wkhtmltopdf pkgs24.pgadmin
          #shellHook = "export NIXPKGS_ALLOW_INSECURE=1";
        };
        packages.x86_64-linux.migrated_pjb70=migrated_pjb70;
        #packages.x86_64-linux.pj_bridgman_addons=pj_bridgman_addons;
        
        packages.x86_64-linux.mypython27=mypython;
        packages.x86_64-linux.my_py_packages=my_py_packages;
        packages.x86_64-linux.wkhtmltopdf-bin=pkgs24.wkhtmltopdf-bin;
        #wkhtml
        devShell=pkgs9.mkShell {
            buildInputs = [mypython  pkgs9.python27.pkgs.ipython];# 
            inputsFrom = builtins.attrValues self.packages.x86_64-linux;
            shellHook = "export NIXPKGS_ALLOW_INSECURE=1";
        };
        defaultPackage.x86_64-linux = self.packages.x86_64-linux.pjbenv;

        nixosModules = rec {
          pjbserver = pjberp7Module;  
          default = pjbserver;   
        };
        #cfg = config.mailserver;
        nixosModule = self.nixosModules.default; # compatibility


          
        #defaultPackage.x86_64-linux = self.devShell;
        #defaultPackage.x86_64-linux = migrated_pjb70;
    # vscode
      
      #stdenv.mkDerivation {
      #  name = "hello";
      #  src = self;
      #  buildPhase = "gcc -o hello ./hello.c";
     #  installPhase = "mkdir -p $out/bin; install -t $out/bin hello";
      #};
  };
    #flake-utils.lib.eachDefaultSystem (system:
    #  {
    #    packages = (import ./migrated_pjb70_nixos2009.nix)
    #        { pkgs = nixpkgs.legacyPackages.${system}; };
    #  }
    #);
}
  
