{ sourcePaths ? import ./sources.nix
, system ? builtins.currentSystem
, crossSystem ? null
, config ? {} }:

let
  # overlays from ops-lib (include ops-lib sourcePaths):
  ops-lib-overlays = (import sourcePaths.ops-lib {}).overlays;

  # our own overlays:
  local-overlays = [
    (import ./util.nix)
  ];

  globals =
    if builtins.pathExists ../globals.nix
    then [(self: _: {
      globals = import ../globals-defaults.nix self // import ../globals.nix self;
    })]
    else builtins.trace "globals.nix missing, please add symlink" [(self: _: {
      globals = import ../globals-defaults.nix self;
    })];

  # merge upstream sources with our own:
  upstream-overlays = [
      ( _: super: {

      iohkNix = import sourcePaths.iohk-nix {};

      cardano-ops-overlays = overlays;
      sourcePaths = (super.sourcePaths or {}) // sourcePaths;
    })
  ];

  overlays =
    ops-lib-overlays ++
    local-overlays ++
    globals ++
    upstream-overlays;
in
  import sourcePaths.nixpkgs {
    inherit overlays system crossSystem config;
  }
