{ sourcePaths ? import ./sources.nix
, system ? builtins.currentSystem
, crossSystem ? null
, config ? {} }:

let
  # overlays from ops-lib (include ops-lib sourcePaths):
  ops-lib-overlays = (import sourcePaths.ops-lib {}).overlays;

  iohkNix = import sourcePaths.iohk-nix {};

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

      inherit iohkNix;

      cardano-ops-overlays = overlays;
      sourcePaths = (super.sourcePaths or {}) // sourcePaths;
    })
  ];

  overlays =
    ops-lib-overlays ++
    local-overlays ++
    globals ++
    upstream-overlays;

  # use our own nixpkgs if it exists in our sources,
  # otherwise use iohkNix default nixpkgs.
  nixpkgs = if (sourcePaths ? nixpkgs)
    then (builtins.trace "Not using IOHK default nixpkgs (use 'niv drop nixpkgs' to use default for better sharing)"
      sourcePaths.nixpkgs)
    else (builtins.trace "Using IOHK default nixpkgs"
      iohkNix.nixpkgs);
in
  import nixpkgs {
    inherit overlays system crossSystem config;
  }
