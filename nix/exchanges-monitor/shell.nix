
let
  pkgs = import ../. {};
  python = pkgs.python35.withPackages(ps: with ps; [ prometheus_client requests ]);
  dependencies = [
    python
    python.pkgs.ipython
  ];
  shell = pkgs.mkShell {
    name = "exchanges-monitor-shell";
    buildInputs = dependencies;
  };

in shell
