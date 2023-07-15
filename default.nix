with import <nixpkgs> {};
let 
  nixpkgs = pkgs;
  pyp = nixpkgs.python311Packages;
  grpcio-reflection = pyp.buildPythonPackage rec {
    pname = "grpcio-reflection";
    version = "1.54.0";
    src = pyp.fetchPypi {
      inherit pname version;
      sha256 = "804326e1add80050cab248107d28f226be58ec49d5a2d08f14a150d8a2621678";
    };
    propagatedBuildInputs = [
      pyp.grpcio
      pyp.grpcio-tools
    ];
  };
  yagrc = pyp.buildPythonPackage rec {
    pname = "yagrc";
    version = "1.1.1";
    src = pyp.fetchPypi {
      inherit pname version;
      sha256 = "e01b801bdeef11553c28b380bbce787366643a6b7947079408cf4638be3fe86b";
    };
    propagatedBuildInputs = [
      pyp.grpcio
      pyp.grpcio-tools
      grpcio-reflection
    ];
  };
in 
(python311.withPackages (ps: with ps; [
  numpy
  matplotlib
  ffmpeg-python
  grpcio
  grpcio-tools
  yagrc
])).env