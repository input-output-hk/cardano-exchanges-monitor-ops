{ python3, makeWrapper, runCommand }:

let
  python = python3.withPackages (ps: with ps; [ prometheus_client requests ]);
in runCommand "exchanges-monitor" {
  buildInputs = [ makeWrapper ];
} ''
  mkdir -p $out/bin
  makeWrapper ${python}/bin/python $out/bin/exchanges-monitor --add-flags ${./exchanges-monitor.py}
''
