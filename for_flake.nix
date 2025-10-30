{ pkgs, ... }:
#{ pkgs ? import <nixpkgs> {} }:
let 
#with import <nixpkgs> {}; 
    #my_nixos = import <nixpkgs/nixos>;


    my_helpscout = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "python-helpscout-v2";
      version = "2";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;

      src = pkgs.fetchFromGitHub {
        rev = "d1cfba119e0f87da9de9798304e1969a75a48189";
        owner = "santiher";
        repo="python-helpscout-v2";
        #sha256 = "0bbbfz8mwiy06zydi1fkwn4kiffkfhd18j5qmhz8dqlsy8d8aaaa";
        sha256 = "lvf6bRrz6DNq7Y17HDGMvpAxsIMPhsj5kvM3aNps2cY=";
        
      };
     doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "https://github.com/santiher/python-helpscout-v2";
        description = "santiher python-helpscout-v2";
      };
    };


    my_oauthlib2xxx = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "oauthlib";
      version = "2";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;

      src = pkgs.fetchFromGitHub {
        rev = "4fddf07313aed766b633a6ca400bca67980017ad";
        owner = "oauthlib";
        repo="oauthlib";
        #sha256 = "0bbbfz8mwiy06zydi1fkwn4kiffkfhd18j5qmhz8dqlsy8d8aaaa";
        sha256 = "WwOUGfCRFWvtF2ahRO5YJJxfPktCDX8TPB3EEOC//a0=";
        
      };
     doCheck = false;
      propagatedBuildInputs = [  ]  ;
      meta = {
        homepage = "https://github.com/oauthlib/oauthlib";
        description = "oauthlib";
      };
    };

    
    my_requests_oauthlib = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "requests-oauthlib";
      version = "2";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;

      src = pkgs.fetchFromGitHub {
        rev = "46f886ccb74652fc9c850ece960edcf2bce765a5";
        owner = "requests";
        repo="requests-oauthlib";
        #sha256 = "0bbbfz8mwiy06zydi1fkwn4kiffkfhd18j5qmhz8dqlsy8d8aaaa";
        sha256 = "W/zqzTnVbqOcrkVZf+GbZwU604s/QP05Kiug7Ljs90Q=";
        
      };
     doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "https://github.com/requests/requests-oauthlib";
        description = "oauthlib";
      };
    };
    
    my_oauthlib = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "oauthlib";
      version = "3.1.0";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "f4526d078aedd5187d0508aa5f9a01eae6a48a470ed678406da94b4cd652aaaa";
        sha256 = "sha256-vuQcw1/MpumIRjysw7y4qWIk9HDKVH5pe2BMxpey+Ik=";
      };

      doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "https://github.com/requests/requests-oauthlib";
        description = "oauthlib";
      };
    };
    my_twilio = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "twilio";
      version = "6.63.2";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "f4526d078aedd5187d0508aa5f9a01eae6a48a470ed678406da94b4cd652aaaa";
        #sha256 = "sha256-vuQcw1/MpumIRjysw7y4qWIk9HDKVH5pe2BMxpeaaaa=";
        sha256 = "sha256-zRRWtd64IWbV9B1eXuzXk45lamJlcTMrnZroBiMD+r0=";
      };

      doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.requests pkgs.python27.pkgs.pyjwt pkgs.python27.pkgs.pytz ]  ;
      meta = {
        homepage = "https://github.com/requests/requests-oauthlib";
        description = "oauthlib";
      };
    };


    
/*
    my_trustpilot = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "python-trustpilot";
      version = "2";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;

      src = pkgs.fetchFromGitHub {
        rev = "6f56609f7d0174a4925219dbf1249c5b8bbbde3a";
        owner = "trustpilot";
        repo="python-trustpilot";
        #sha256 = "0bbbfz8mwiy06zydi1fkwn4kiffkfhd18j5qmhz8dqlsy8d8aaaa";
        sha256 = "BxAnSObwk3tXPsWse28E5zWsD5i89uKsyw2jQweaBfU=";
        
      };
     doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "https://github.com/trustpilot/python-trustpilot";
        description = "santiher python-trustpilot";
      };
    };
*/


   my_werkzeug = pkgs.python27.pkgs.buildPythonPackage rec {
     pname = "Werkzeug";
     version = "0.15.5";

     src = pkgs.python27.pkgs.fetchPypi {
       inherit pname version;
       sha256 = "a13b74dd3c45f758d4ebdb224be8f1ab8ef58b3c0ffc1783a8c7d9f4f50227e6";
     };

     propagatedBuildInputs = [ pkgs.python27.pkgs.itsdangerous ];
     checkInputs = [ pkgs.python27.pkgs.pytest pkgs.python27.pkgs.requests pkgs.python27.pkgs.hypothesis ];

     checkPhase = ''
         pytest ${pkgs.stdenv.lib.optionalString pkgs.stdenv.isDarwin "-k 'not test_get_machine_id'"}
           '';           

     meta = with pkgs.stdenv.lib; {
       homepage = "https://palletsprojects.com/p/werkzeug/";
       description = "A WSGI utility library for Python";
       license = licenses.bsd3;
     };
   };



    
   my_psycopg2 = pkgs.python27.pkgs.buildPythonPackage rec {
     pname = "psycopg2";
     version = "2.7.7";

     #disabled = pkgs.isPyPy;

     src = pkgs.python27.pkgs.fetchPypi {
       inherit pname version;
       sha256 = "f4526d078aedd5187d0508aa5f9a01eae6a48a470ed678406da94b4cd6524b7e";
     };

     buildInputs = pkgs.lib.optional pkgs.stdenv.isDarwin pkgs.openssl;
     nativeBuildInputs = [ pkgs.postgresql ];

     doCheck = false;

     meta = with pkgs.lib; {
       description = "PostgreSQL database adapter for the Python programming language";
       license = with licenses; [ gpl2 zpl20 ];
     };
   };



   

    my_toolz = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "toolz";
      version = "0.7.4";
   
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "43c2c9e5e7a16b6c88ba3088a9bfc82f7db8e13378be7c78d6c14a5f8ed05afd";
      };

      doCheck = false;

      meta = {
        homepage = "https://github.com/pytoolz/toolz/";
        description = "List processing tools and functional utilities";
      };
    };


    my_pywebdav = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "pywebdav";
      version = "0.8";
   
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "0269x5l4nknfxg90lxkx3ynsvnr28gdhagv592vhbs9y4v470cma";
      };

      doCheck = false;

      meta = {
        homepage = "https://github.com/pytoolz/toolz/";
        description = "List processing tools and functional utilities";
      };
    };

    my_python-ldap = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "python-ldap";
      version = "3.2.0";
   
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "13nvrhp85yr0jyxixcjj012iw8l9wynxxlykm9j3alss6waln73x";
      };

      doCheck = false;
      propagatedBuildInputs = [  ] ;
      meta = {
        homepage = "https://github.com/pytoolz/toolz/";
        description = "List processing tools and functional utilities";
      };
    };







#https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/vatnumber/vatnumber-1.1.tar.gz

   my_vatnumber = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "vatnumber";
      version = "1.1";
      src = pkgs.fetchurl {
         url = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/vatnumber/vatnumber-1.1.tar.gz";
         #sha256 = "0c9ims85skikr2ciw06nzgk639r1sg1x1adc2ja24yiy93nnkz70";
         sha256 = "065fgz042ca2iy7kkjjhglqsavn82sxfdnz09jkhjxhk1r11fw7z";
      };
      #src = python27.pkgs.fetchPypi {
      #  inherit pname version;
      #  sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
      #};
      
      doCheck = false;
      propagatedBuildInputs = [  ] ;
      meta = {
        homepage = "";
        description = "vatnumber";
      };
    };


    my_pyyaml311 = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "PyYaml";
      version = "3.1.1";
      src = pkgs.fetchurl {
         url = "https://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz";
         #sha256 = "0c9ims85skikr2ciw06nzgk639r1sg1x1adc2ja24yiy93nnkz70";
         sha256 = "1s26125vfnskng58ym37xhwv8v0mm95b2cwbjfag8prfhy596v63";
      };
      #src = python27.pkgs.fetchPypi {
      #  inherit pname version;
      #  sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
      #};
      
      doCheck = false;
      propagatedBuildInputs = [  ] ;
      meta = {
        homepage = "";
        description = "PyYaml3.1.1";
      };
    };

    my_pyyaml512 = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "PyYaml";
      version = "5.1.2";
      src = /home/jan/Downloads/PyYAML-5.1.2.tar.gz;    
      doCheck = false;
      propagatedBuildInputs = [  ]  ;
      meta = {
        homepage = "";
        description = "PyYaml";
      };
    };
    

    my_magento = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "magento";
      version = "3.1";

      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
      };

      doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.six pkgs.python27.pkgs.suds-jurko ]  ;
      meta = {
        homepage = "https://github.com/fulfilio/python-magento";
        description = "Magento";
      };
    };

#    my_odoo12 = fetchFromGithub {
#      pname = "odoo";
#      version = "12.0";
#      src = 
#
#   }


    
    my_openid = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "python-openid";
      version = "2.2.5";
      #src = /home/jan/Downloads/python-openid-2.2.5.tar.gz;

      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
        sha256 = "1vvhxlghjan01snfdc4k7ykd80vkyjgizwgg9bncnin8rqz1ricj";
      };
      #python27.pkgs.six python27.pkgs.suds-jurko
      
      doCheck = false;
      propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "https://github.com/fulfilio/python-magento";
        description = "OpenID Connect";
      };
    };




   my_pillow = pkgs.python27.pkgs.buildPythonPackage rec {
     pname = "Pillow";
     version = "5.4.1";

     src = pkgs.python27.pkgs.fetchPypi {
       inherit pname version;
       #sha256 = "5233664eadfa342c639b9b9977190d64ad7aca4edc51a966394d7e08e7f38aaa";
       sha256 = "UjNmTq36NCxjm5uZdxkNZK16yk7cUalmOU1+COfzip8=";
     };

     doCheck = false; #!stdenv.isDarwin && !isPyPy;

     # Disable imagefont tests, because they don't work well with infinality:
     # https://github.com/python-pillow/Pillow/issues/1259
     postPatch = ''
       rm Tests/test_imagefont.py
     '';

     propagatedBuildInputs = [ pkgs.python27.pkgs.olefile ];

     checkInputs = [ pkgs.python27.pkgs.pytest pkgs.python27.pkgs.pytestrunner ];

     buildInputs = [
       pkgs.freetype pkgs.libjpeg pkgs.zlib pkgs.libtiff pkgs.libwebp pkgs.tcl pkgs.lcms2 ];
       #++ pkgs.stdenv.lib.optionals (pkgs.isPyPy) [ pkgs.tk pkgs.libX11 ];

     # NOTE: we use LCMS_ROOT as WEBP root since there is not other setting for webp.
     # NOTE: The Pillow install script will, by default, add paths like /usr/lib
     # and /usr/include to the search paths. This can break things when building
     # on a non-NixOS system that has some libraries installed that are not
     # installed in Nix (for example, Arch Linux has jpeg2000 but Nix doesn't
     # build Pillow with this support). We patch the `disable_platform_guessing`
     # setting here, instead of passing the `--disable-platform-guessing`
     # command-line option, since the command-line option doesn't work when we run
     # tests.
     preConfigure = let
       libinclude' = pkg: ''"${pkg.out}/lib", "${pkg.out}/include"'';
       libinclude = pkg: ''"${pkg.out}/lib", "${pkg.dev}/include"'';
     in ''
       sed -i "setup.py" \
           -e 's|^FREETYPE_ROOT =.*$|FREETYPE_ROOT = ${libinclude pkgs.freetype}|g ;
               s|^JPEG_ROOT =.*$|JPEG_ROOT = ${libinclude pkgs.libjpeg}|g ;
               s|^ZLIB_ROOT =.*$|ZLIB_ROOT = ${libinclude pkgs.zlib}|g ;
               s|^LCMS_ROOT =.*$|LCMS_ROOT = ${libinclude pkgs.lcms2}|g ;
               s|^TIFF_ROOT =.*$|TIFF_ROOT = ${libinclude pkgs.libtiff}|g ;
               s|^TCL_ROOT=.*$|TCL_ROOT = ${libinclude' pkgs.tcl}|g ;
               s|self\.disable_platform_guessing = None|self.disable_platform_guessing = True|g ;'
       export LDFLAGS="-L${pkgs.libwebp}/lib"
       export CFLAGS="-I${pkgs.libwebp}/include"
     ''
     # Remove impurities
     + pkgs.stdenv.lib.optionalString pkgs.stdenv.isDarwin ''
       substituteInPlace setup.py \
         --replace '"/Library/Frameworks",' "" \
         --replace '"/System/Library/Frameworks"' ""
     '';

     meta = with pkgs.stdenv.lib; {
       homepage = https://python-pillow.github.io/;
       description = "Fork of The Python Imaging Library (PIL)";
       longDescription = ''
         The Python Imaging Library (PIL) adds image processing
         capabilities to your Python interpreter.  This library
         supports many file formats, and provides powerful image
         processing and graphics capabilities.
       '';
       license = "http://www.pythonware.com/products/pil/license.htm";
       maintainers = with maintainers; [ goibhniu prikhi ];
     };
   };

    my_odooutils = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "odooutils";
      version = "0.0.1";

      src = pkgs.fetchFromGitHub {
           rev = "423022ae9c6e8a761e9fa262ae110795d962364c";
           owner = "galtys";
           repo = "odooutils";
           sha256 = "sha256-TrqIxwx6cGeQbuI6lOW2q68YqBDnFf/Ka3TG74InYc8=";
      };
      #src = /home/jan/github.com/odooutils;
      doCheck = false;
      propagatedBuildInputs = [ my_psycopg2 pkgs.python27Packages.toml ]  ;
      meta = {
        homepage = "https://github.com/galtys/odooutils";
        description = "Odoo Utils";
      };
    };
    
    my_reportlab = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "reportlab";
      version = "3.1.44";
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
        #sha256 = "08a6e63a4502d3a00062ba9ff9669f95577fbdb1a5f8c6cdb1230c5ee295273a";
        sha256 = "1m9nnqhv6wh1mgz66ffmfzmx4x2yxrp23hgihl7fs6pxzr52xhpn";
      };
      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow ];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
    # Remove all the test files that require access to the internet to pass.
#    rm tests/test_lib_utils.py
#    rm tests/test_platypus_general.py
#    rm tests/test_platypus_images.py
    # Remove the tests that require Vera fonts installed
#    rm tests/test_graphics_render.py
  '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "An Open Source Python library for generating PDFs and graphics ";
        description = "http://www.reportlab.com/; ";
      };
    };

    my_openupgradelib = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "openupgradelib";
      version = "3.11.1";
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
        #sha256 = "08a6e63a4502d3a00062ba9ff9669f95577fbdb1a5f8c6cdb1230c5ee295273a";
        #sha256 = "1m9nnqhv6wh1mgz66ffmfzmx4x2yxrp23hgihl7fs6pxzr52aaaa";
        sha256 = "sha256-s3rb83uU5kn+u5nqqIfuIYw7NyBhCH4145Aa9YXYy+0=";
      };
      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "An Open Source Python library for generating PDFs and graphics ";
        description = "http://www.reportlab.com/; ";
      };
    };

    my_jinja2 = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "Jinja2";
      version = "2.7.3";
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
        #sha256 = "08a6e63a4502d3a00062ba9ff9669f95577fbdb1a5f8c6cdb1230c5ee295273a";
        #sha256 = "1m9nnqhv6wh1mgz66ffmfzmx4x2yxrp23hgihl7fs6pxzr52aaaa";
        sha256 = "sha256-LiSsXQBNtXFJdqBKwOgMbfbkfpjDVMssDYL4h51Pj9s=";
        #sha256 = "sha256-s3rb83uU5kn+u5nqqIfuIYw7NyBhCH4145Aa9aaaa+0=";
      };
      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata pkgs.python27.pkgs.markupsafe];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "jinja ";
        description = "http://www.reportlab.com/; ";
      };
    };

    my_pypdf = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "pyPdf";
      version = "1.13";
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "0kbr95a85812drvhhnwrqq3pb85xq5j7i5w9bscl9m8b7im315hv";
        #sha256 = "08a6e63a4502d3a00062ba9ff9669f95577fbdb1a5f8c6cdb1230c5ee295273a";
        #sha256 = "1m9nnqhv6wh1mgz66ffmfzmx4x2yxrp23hgihl7fs6pxzr52aaaa";
        #sha256 = "sha256-LiSsXQBNtXFJdqBKwOgMbfbkfpjDVMssDYL4h51aaaa=";
        #sha256 = "sha256-s3rb83uU5kn+u5nqqIfuIYw7NyBhCH4145Aa9aaaa+0=";
        sha256 = "sha256-Ou3kw8nGrQfJjwWfkNsLCe04P3x5HEYQD2SeHKvaDjs=";
      };
      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata pkgs.python27.pkgs.markupsafe];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "jinja ";
        description = "http://www.reportlab.com/; ";
      };
    };

    my_schwifty = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "schwifty";
      version = "2018.9.1";
      #src = pkgs.python27.pkgs.fetchPypi {
      #  inherit pname version;
      #  sha256 = "sha256-wMy6k8IGOTTOe176FKIQEeTlkwy/+rbQ0nKM+9cVgtw=";
      #};
      src = pkgs.fetchFromGitHub {
           rev = "69376fade070dbfdf89c57a0060bc290f7a744bb";
           owner = "mdomke";
           repo = "schwifty";
           #sha256 = "sha256-TrqIxwx6cGeQbuI6lOW2q68YqBDnFf/Ka3TG74Idddd=";
           sha256 = "sha256-FnrIK6/4WuvF8Y8Lpo821ONsQpM9K/L2M0ppnc91Sq8=";
           
      };

      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata pkgs.python27.pkgs.markupsafe pkgs.python27.pkgs.pbr];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "jinja ";
        description = "http://www.reportlab.com/; ";
      };
    };

    my_bs4 = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "beautifulsoup4";
      version = "4.9.3";
      
      src = pkgs.python27.pkgs.fetchPypi {
        inherit pname version;
        #sha256 = "sha256-wMy6k8IGOTTOe176FKIQEeTlkwy/+rbQ0nKM+9caaaa=";
        sha256 = "sha256-hHKeMirR1bTSX4Bb+gW5At2WRQ9DhCxOmQZ9XhNp6yU=";
        #sha256 = "sha256-pIaFxY9Q/hJ3IkF7roP+a631ANVLVffjn/5Dt5hlOSU=";
      };
      
      #src = pkgs.fetchFromGitHub {
      #     rev = "69376fade070dbfdf89c57a0060bc290f7a744bb";
      #     owner = "mdomke";
      #     repo = "schwifty";
      #     sha256 = "sha256-FnrIK6/4WuvF8Y8Lpo821ONsQpM9K/L2M0ppnc91Sq8=";
      #};

      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata pkgs.python27.pkgs.markupsafe pkgs.python27.pkgs.soupsieve];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "jinja ";
        description = "http://www.reportlab.com/; ";
      };
    };
    my_unidecode = pkgs.python27.pkgs.buildPythonPackage rec {
      pname = "unidecode";
      version = "1.0.23";
      
      src = pkgs.fetchFromGitHub {
           rev = "e3c730e5830f15c613f65f1764258165f4e5f52f";
           owner = "avian2";
           repo = "unidecode";
           #sha256 = "sha256-FnrIK6/4WuvF8Y8Lpo821ONsQpM9K/L2M0ppnc9aaaa=";
           sha256 = "sha256-EW/csPHpOXiaGyJCKzzfr86DtmlT1E+ko3JOf/VAVTU=";
      };
      
      #src = pkgs.python27.pkgs.fetchPypi {
      #  inherit pname version;
      #  sha256 = "sha256-Ou3kw8nGrQfJjwWfkNsLCe04P3x5HEYQD2SeHKvaaaa=";
      #};
      
      #python27.pkgs.six python27.pkgs.suds-jurko
      checkInputs = [ pkgs.glibcLocales ];
      #buildInputs = [ my_pillow ]; #pkgs.python27.pkgs.pillow ];
      buildInputs = [ pkgs.python27.pkgs.pillow pkgs.python27.pkgs.lxml pkgs.python27.pkgs.cssselect pkgs.python27.pkgs.importlib-metadata pkgs.python27.pkgs.markupsafe];
      #buildInputs = [ pkgs.python27.pkgs.ft pkgs.python27.pkgs.pillow ];

      postPatch = ''
      '';
      doCheck = false;
      #propagatedBuildInputs = [ pkgs.python27.pkgs.python-jose pkgs.python27.pkgs.requests ]  ;
      meta = {
        homepage = "jinja ";
        description = "http://www.reportlab.com/; ";
      };
    };

   my-api-client = ps: with ps; [
     (
       pkgs.python27.pkgs.buildPythonPackage rec {
         pname = "api-client";
         version = "1.3.1";
         #format = "pyproject";
         src = pkgs.python27.pkgs.fetchPypi {
           pname = "api-client";
           inherit version;
           #sha256 = "sha256-EEVAr4Ixsj0BJAo0HWb+lPrFa6twf9wVnDXkLTVaaaa=";
           #sha256="sha256-fESSpVvVyfY4Ie3QFi1hd/ODtHM8/kIb073lFR6AxJs=";
           #sha256 = "sha256-BBR68gs4N83eo434ibofwZMYBLt3p9TZVSOhoLA+7KQ=";
           #sha256 = "sha256-JWnJmBkc0aBCvv+jz3wRGSdyN7S6H6Ah0gyB+pj6lek=";
           sha256 = "sha256-GU5cjytSAFQEZEYqaOqdBq2F1vN08D04TwmHEVcquUY=";
         };
         build-system = [setuptools];
         nativeBuildInputs = [pkgs.sqlite];
         #pythonImportsCheck = [ "apsw" ];
         propagatedBuildInputs = [
           setuptools
         ];
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   my-apiclient = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "apiclient";
         version = "1.0.4";
         #format = "pyproject";
         src = fetchPypi {
           pname = "apiclient";
           inherit version;
           #sha256 = "sha256-EEVAr4Ixsj0BJAo0HWb+lPrFa6twf9wVnDXkLTVaaaa=";
           #sha256="sha256-fESSpVvVyfY4Ie3QFi1hd/ODtHM8/kIb073lFR6AxJs=";
           #sha256 = "sha256-BBR68gs4N83eo434ibofwZMYBLt3p9TZVSOhoLA+7KQ=";
           sha256 = "sha256-JWnJmBkc0aBCvv+jz3wRGSdyN7S6H6Ah0gyB+pj6lek=";
         };
         build-system = [setuptools certifi urllib3];
         nativeBuildInputs = [pkgs.sqlite certifi urllib3];
         #pythonImportsCheck = [ "apsw" ];
         propagatedBuildInputs = [
           setuptools
         ];
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   
   #++(my-api-client pkgs27) #my_bs4
   #my_requests_oauthlib
    pkgs27=pkgs.python27Packages;
    #my_schwifty
    my_py_packages2=with pkgs.python27Packages; [ certifi urllib3 my_unidecode pbr my_twilio  chardet pycups phonenumbers  my_psycopg2 tabulate my_openupgradelib pillow  ldap my_pywebdav my_vatnumber gdata Babel chardet decorator docutils feedparser gevent greenlet html2text my_jinja2  lxml Mako markupsafe mock  ofxparse passlib  psutil  pydot  pyparsing my_pypdf pyserial python-dateutil pytz pyusb qrcode my_reportlab requests suds-jurko vobject my_werkzeug xlwt xlrd simplejson pychart unittest2 pycountry numpy wheel unicodecsv  matplotlib my_magento my_pyyaml311 my_openid setuptools my_helpscout  gspread  oauth2client toml my_odooutils pandas singledispatch my_oauthlib ]++(my-apiclient pkgs27); 
    

  mypython = pkgs.python27.buildEnv.override {
     extraLibs =  my_py_packages2;  
     ignoreCollisions = true;
  };

  myuserid = pkgs.stdenv.mkDerivation rec {
       MYHR= "${pkgs.coreutils}/bin/id";     
  };


in
  #mypython
  my_py_packages2
#pkgs.stdenv.mkDerivation rec {
#  name = "migrated_pjb70_env";
#  #phases = [ "installPhase" "fixupPhase" ];
#  #src = self;
#  #unpackPhase = "false";
#  #src = builtins.filterSource (path: type: false) ./.;
#  buildInputs = [ mypython pkgs.wkhtmltopdf pkgs.python27.pkgs.ipython];#
#
#}

#migrated_pjb70

#libsass  PyYaml
#pkgs.stdenv.mkDerivation rec {
#  name = "migrated_pjb70";
#  env = pkgs.buildEnv { name = name; paths = buildInputs; };
#
#  ERPPY_ROOT = "${mypython}";
#  buildInputs = [
#    mypython
#    pkgs.protobuf3_1
#    migrated_pjb70     
    #pkgs.python
    #pkgs.python27Packages.virtualenv
    #pkgs.python27Packages.pip
    #pkgs.go_1_4
    #pkgs.lua5_3
#  ];
#}


#pwgen |head -n 1 | python -c "import sys; sys.stdout.write(sys.stdin.read().strip())"
