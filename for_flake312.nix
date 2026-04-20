{ pkgs ? import <nixpkgs> {} }:

with pkgs.python312Packages;

let

    
   my_html5_print = ps: with ps; [
     # ...
     (
       buildPythonPackage rec {
         pname = "html5print";
         version = "0.1.2";
         src = fetchPypi {
           inherit pname version;
           sha256 = "sha256-0bbzmQ4Eb5zL4ttNHSFjEycfObUkYlid1PgMDVmRkwY=";
            };
         doCheck = false;
         propagatedBuildInputs = [
         ];
       }
     )
   ];

   my_classes = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "classes";
         version = "0.4.1";
         format = "pyproject";
         src = pkgs.fetchFromGitHub {
           owner = "dry-python";
           repo = "classes";
           rev = "refs/tags/${version}";
           hash = "sha256-r9/KujyUf1A3KzlStn74Qq2JbYkNA+I6ikX1fp+FsYg=";
         };
         nativeBuildInputs = [ poetry-core ];
         propagatedBuildInputs = [ typing-extensions ];
         doCheck = false;
       }
     )
   ];
   my_pydantic = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "classes";
         version = "0.4.1";
         format = "pyproject";
         src = pkgs.fetchFromGitHub {
           owner = "dry-python";
           repo = "classes";
           rev = "refs/tags/${version}";
           hash = "sha256-r9/KujyUf1A3KzlStn74Qq2JbYkNA+I6ikX1fp+FsYg=";
         };
         nativeBuildInputs = [ poetry-core ];
         propagatedBuildInputs = [ typing-extensions ];
         doCheck = false;
       }
     )
   ];



   
   # Override manim to include classes, dataclasses-json, and manim-voiceover
   my_plotly = ps: with ps; [
     (
       plotly.overridePythonAttrs (oldAttrs: {
         propagatedBuildInputs = (oldAttrs.propagatedBuildInputs or []);
         doCheck=false;
       })
     )
   ];

   # my_plotly = ps: with ps; [
   #   (
   #     buildPythonPackage rec {
   #       pname = "plotly";
   #       version = "v6.1.2";
   #       format = "pyproject";
   #       #build-system = [setuptools];
   #       src = pkgs.fetchFromGitHub {
   #         owner = "plotly";
   #         repo = "plotly.py";
   #         rev = "refs/tags/${version}";
   #         hash = "sha256-+vIq//pDLaaTmRGW+oytho3TfMmLCtuIoHeFenLVcek=";
   #       };
   #       nativeBuildInputs = [ poetry-core ];
   #       propagatedBuildInputs = [ setuptools  typing-extensions ];
   #       doCheck = false;
   #     }
   #   )
   # ];
   
   my_cloudinary = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "cloudinary";
         version = "1.41.0";
         src = fetchPypi {
           inherit pname version;
           sha256 = "sha256-4YlzmnlqfSrRXBmXF0HTOpMAgWsWwCgrSxTM8d0pSMA=";
         };
         propagatedBuildInputs = [
           certifi
           six
           urllib3
         ];
         doCheck = false;
       }
     )
   ];

   # Python sox package
   my_sox = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "sox";
         version = "1.5.0";
         src = fetchPypi {
           inherit pname version;
           ###sha256 = "sha256-4YlzmnlqfSrRXBmXF0HTOpMAgWsWwCgrSxTM8d0aaaa=";
           sha256 = "sha256-Ese+W7H1SNiR/hHoLAjPXxoddOIlKY9gCC5a6yRpraA=";
           #sha256 = "sha256-sPLRNpJFC4ic0/ZhJ+lvgBlC7CqsW7IWU9/RUODXaaaa";
           
         };
         propagatedBuildInputs = [ numpy ];
         buildInputs = [ pkgs.sox ];
         doCheck = false;
       }
     )
   ];
   # Python sox package
   my_sox141 = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "sox";
         version = "1.4.1";
         src = fetchPypi {
           inherit pname version;
           sha256 = "sha256-sPLRNpJFC4ic0/ZhJ+lvgBlC7CqsW7IWU9/RUODXEFU=";
         };
         propagatedBuildInputs = [ numpy ];
         buildInputs = [ pkgs.sox ];
         doCheck = false;
       }
     )
   ];

   my_manim_recorder029 = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "manim-recorder";
         version = "0.2.9";
         format = "pyproject";
         src = fetchPypi {
           pname = "manim_recorder";
           inherit version;
           #sha256 = "sha256-KdEk5XYg9rgsyZk1aVYBCgigAy5Fkoihozv/GMmlFgc=";
           sha256 = "sha256-YbNm5YUyvkiaAKTU4xgdWnzL94IllM/snOS4Z7zC2Z0=";
           #sha256 = "0k4g59rmzps83qdzcwv9ryz9s5nndarbd4vcgif9ncr5lybsaaaa";
         };
         nativeBuildInputs = [ poetry-core ];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           pyaudio
           pydub
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   
   # manim-voiceover package
   my_manim_voiceover = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "manim-voiceover";
         version = "0.3.7";
         format = "pyproject";
         src = fetchPypi {
           pname = "manim_voiceover";
           inherit version;
           sha256 = "0k4g59rmzps83qdzcwv9ryz9s5nndarbd4vcgif9ncr5lybsl4wr";
         };
         buildInputs = [] ;
         nativeBuildInputs = [ poetry-core ] ;
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           pyaudio
           pydub
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps)  ;
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   # manim-voiceover package
   my_manim_recorder = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "manim-recorder";
         version = "0.6.0";
         format = "pyproject";
         src = fetchPypi {
           pname = "manim_recorder";
           inherit version;
           sha256 = "sha256-KdEk5XYg9rgsyZk1aVYBCgigAy5Fkoihozv/GMmlFgc=";
           #sha256 = "0k4g59rmzps83qdzcwv9ryz9s5nndarbd4vcgif9ncr5lybsaaaa";
         };
         nativeBuildInputs = [ poetry-core ] ++ (my_manim_voiceover ps);
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           pyaudio
           pydub
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps) ++ (my_manim_voiceover ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];

   my-nordigen = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "nordigen-python";
         version = "0.1.2";
         #format = "pyproject";
         src = fetchPypi {
           pname = "nordigen-python";
           inherit version;
           #sha256 = "sha256-EEVAr4Ixsj0BJAo0HWb+lPrFa6twf9wVnDXkLTVaaaa=";
           #sha256="sha256-fESSpVvVyfY4Ie3QFi1hd/ODtHM8/kIb073lFR6AxJs=";
           sha256 = "sha256-BBR68gs4N83eo434ibofwZMYBLt3p9TZVSOhoLA+7KQ=";
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


   my-api-client = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "api-client";
         version = "1.3.1";
         #format = "pyproject";
         src = fetchPypi {
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
   
   my-piecash = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "piecash";
         version = "1.2.1";
         #format = "pyproject";
         src = fetchPypi {
           pname = "piecash";
           inherit version;
           #sha256 = "sha256-EEVAr4Ixsj0BJAo0HWb+lPrFa6twf9wVnDXkLTVaaaa=";
           #sha256="sha256-fESSpVvVyfY4Ie3QFi1hd/ODtHM8/kIb073lFR6AxJs=";
           #sha256 = "sha256-BBR68gs4N83eo434ibofwZMYBLt3p9TZVSOhoLA+7KQ=";
           #sha256 = "sha256-JWnJmBkc0aBCvv+jz3wRGSdyN7S6H6Ah0gyB+pj6lek=";
           #sha256 = "sha256-GU5cjytSAFQEZEYqaOqdBq2F1vN08D04TwmHEVcquUY=";
           sha256 = "sha256-f5xcc0LfO5zRRXrfS4L+pDDxT6k74X5Sx91BwCq/cQQ=";
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
   my-strip_hints = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "strip_hints";
         version = "0.1.13";
         format = "pyproject";
         src = fetchPypi {
           inherit pname;
           inherit version;
           sha256 = "sha256-H+rr3mEmm6Deoefwk99/+dTfSYDM5+PCLtbYauQ9vQY=";
         };
         build-system = [setuptools];
         nativeBuildInputs = [poetry-core];
         #pythonImportsCheck = [ "apsw" ];
         propagatedBuildInputs = [
           setuptools
         ];
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];

   
   #
   my-python-apsw = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "apsw";
         version = "3.48.0.0";
         #format = "pyproject";
         src = fetchPypi {
           pname = "apsw";
           inherit version;
           #sha256 = "sha256-EEVAr4Ixsj0BJAo0HWb+lPrFa6twf9wVnDXkLTVaaaa=";
           sha256="sha256-fESSpVvVyfY4Ie3QFi1hd/ODtHM8/kIb073lFR6AxJs=";
           #
         };
         build-system = [setuptools];
         nativeBuildInputs = [pkgs.sqlite];
         pythonImportsCheck = [ "apsw" ];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           nbdev #fast core needed
           starlette
           
           itsdangerous
           uvicorn
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   my_toolslm = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "toolslm";
         version = "0.2.3";
         format = "pyproject";
         src = pkgs.fetchFromGitHub {
           owner = "AnswerDotAI";
           repo = "toolslm";
           rev = "refs/tags/${version}";
           #hash = "sha256-r9/KujyUf1A3KzlStn74Qq2JbYkNA+I6ikX1fp+aaaa=";
           hash = "sha256-Nts3XXO/UJcKCqhM1LGT57TEbesdgPFgYdbUsa9pGkc=";
         };
         nativeBuildInputs = [ poetry-core setuptools ];
         propagatedBuildInputs = [ typing-extensions nbdev httpx];
         doCheck = false;
       }
     )
   ];
   
   my-apsw = import ./apsw.nix {inherit lib;
                                inherit buildPythonPackage;
                                fetchurl=pkgs.fetchurl;
                                inherit setuptools;
                                sqlite=pkgs.sqlite;};
   my-python-apswutils = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "python-apswutils";
         version = "0.1.0";
         format = "pyproject";
         src = fetchPypi {
           pname = "apswutils";
           inherit version;
           sha256 = "sha256-TFdrJZ1wig9yzc7ZJWXk94MJkT0ggtvjyb9lMULdvlg=";
           
         };
         nativeBuildInputs = [ poetry-core];
         propagatedBuildInputs = [
           gtts
           mutagen
           #apsw
           my-apsw
           #(my-python-apsw ps)
           pip
           nbdev #fast core needed
           starlette
           
           itsdangerous
           uvicorn
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];

   my-python-fastlite = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "python-fastlite";
         version = "0.2.0";
         format = "pyproject";
         src = fetchPypi {
           pname = "fastlite";
           inherit version;
           sha256 = "sha256-emBmWgTd5w2aNoABJb15X8h1opHXKR9T+mvhzsCzYOc=";
         };
         nativeBuildInputs = [ poetry-core ];
         build-system = [setuptools];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           pyaudio
           pydub
           nbdev #fast core needed
           starlette
           itsdangerous
           #(my-python-apswutils ps)
           uvicorn
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];

   
   my-python-mistletoe = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "python-mistletoe";
         version = "1.4.0";
         format = "pyproject";
         src = fetchPypi {
           pname = "mistletoe";
           inherit version;
           sha256 = "sha256-FjD5BuXku+Zv3rTSnSd+LqUV1kK7GKm0mxNjYamBjJ0=";
         };
         nativeBuildInputs = [ poetry-core ];
         build-system = [setuptools];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           pyaudio
           pydub
           nbdev #fast core needed
           starlette
           itsdangerous
           #(my-python-apswutils ps)
           uvicorn
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   
   my-python-fasthtml = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "python-fasthtml";
         version = "0.12.20";
         format = "pyproject";
         src = fetchPypi {
           pname = "python_fasthtml";
           inherit version;
           sha256 = "sha256-9NihwrmPBucM+FNEXLsUB8ROke1SmuRlwOiAugGVMdE=";
         };
         nativeBuildInputs = [ poetry-core ];
         build-system = [setuptools];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           (my-python-fastlite ps)
           pyaudio
           pydub
           nbdev #fast core needed
           starlette
           itsdangerous
           (my-python-apswutils ps)
           uvicorn
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];

   my-monster-ui = ps: with ps; [
     (
       buildPythonPackage rec {
         pname = "python-monster-ui";
         version = "1.0.21";
         format = "pyproject";
         src = fetchPypi {
           pname = "monsterui";
           inherit version;
           sha256 = "sha256-7e8RKS7bnhYoUyG5MIzwZI2UH/Fje/DLCD0oNr6CBS4=";
         };
         nativeBuildInputs = [ poetry-core ];
         propagatedBuildInputs = [
           gtts
           mutagen
           pip
           lxml
           
           (my-python-mistletoe ps)
           pyaudio
           pydub
           python-dotenv
           python-slugify
           setuptools
         ] ++ (my_sox ps);
         doCheck = false;
         dontCheckRuntimeDeps = true;
       }
     )
   ];
   

   
   # Override manim to include classes, dataclasses-json, and manim-voiceover
   my_manim = ps: with ps; [
     (
       manim.overridePythonAttrs (oldAttrs: {
         propagatedBuildInputs = (oldAttrs.propagatedBuildInputs or []) ++ [
           dataclasses-json sympy
         ] ++ (my_classes ps) ++ (my_manim_voiceover ps) ++ (my_manim_recorder ps) ;
         buildInputs = [] ++  (my_manim_recorder ps);
         nativeBuildInputs = [ poetry-core ] ++ (my_manim_recorder ps);

       })
     )
   ];
   # from typing import override   ++ (my_manim_recorder ps) ++ (my_manim_recorder029 ps)
    #my_locust = ...load testing tool
   #pyldap, vatnumber, pypiwin32 my_libsaass qtconsole
   #jupyterlab notebook ipywidgets pyrender django whitenoise brotli gunicorn psycopg2 pynput evdev unicodecsv

  mypython = pkgs.python312.buildEnv.override {
    extraLibs = with pkgs.python312Packages; [ toml scipy matplotlib pandas numpy scipy pillow watchdog skia-pathops isosurfaces cloup poetry-core     click
                                               requests-oauthlib
                                               click-default-group
                                               youtube-transcript-api
                                               cloup
                                               pynput
                                               pypdf2
                                               colour
                                               sqlmodel
                                               pydantic                                               
                                               grpcio
                                               grpcio-tools
                                               gtts
                                               importlib-metadata
                                               isosurfaces
                                               jupyterlab
                                               manimpango
                                               mapbox-earcut
                                               moderngl
                                               moderngl-window
                                               mutagen
                                               networkx
                                               numpy
                                               pillow
                                               pycairo
                                               pydub
                                               pygments
                                               pip
                                               pyaudio
                                               python-dotenv
                                               python-slugify
                                               rich
                                               scipy
                                               setuptools
                                               sympy
                                               passlib
                                               screeninfo
                                               skia-pathops
                                               uvicorn
                                               tabulate
                                               flask
                                               flask-sqlalchemy
                                               srt
                                               #pytest-doctestplus
                                               #plotly
                                               fastapi
                                               reportlab
                                               pypdf
                                               polib
                                               psycopg2
                                               lxml
                                               lxml-html-clean
                                               zeep
                                               rjsmin
                                               pyopenssl
                                               geoip2
                                               qrcode
                                               xlwt
                                               xlrd
                                               
                                               bcrypt
                                               pyjwt
                                               jinja2
                                               
                                               XlsxWriter
                                               python-stdnum
                                               numpy
                                               
                                               #api-client
                                               #apiclient
                                               #nordigen-python
                                               svgelements
    python-multipart                                           
    tqdm
    watchdog
                                             ] ++ (my_cloudinary pkgs.python312Packages) ++ (my_manim pkgs.python312Packages) ++(my_sox pkgs.python312Packages) ++ (my_classes pkgs.python312Packages) ++(my-python-fasthtml pkgs.python312Packages) ++ (my-monster-ui pkgs.python312Packages) ++ (my-python-apswutils pkgs.python312Packages) ++ (my-python-fastlite pkgs.python312Packages) ++ (my-python-mistletoe pkgs.python312Packages) ++ (my_plotly pkgs.python312Packages) ++ (my_toolslm pkgs.python312Packages) ++ (my-nordigen pkgs.python312Packages) ++ (my-api-client pkgs.python312Packages) ++ (my-piecash pkgs.python312Packages) ++ (my_manim_voiceover pkgs.python312Packages) ++ (my-strip_hints pkgs.python312Packages);
    #ignoreCollisions = true;
    #++ (my_manim_recorder pkgs.python312Packages) 
  };

in
  mypython

    #portaudio
    #++ 
    # 
    #
