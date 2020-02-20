
let
  pkgs = import ../ {};
  dependencies = with pkgs.python3Packages; [
    requests
    prometheus_client
    ipython
  ];
  shell = pkgs.mkShell {
    name = "exchanges-monitor-shell";
    buildInputs = dependencies;
  };

in shell
