{ ... }:

with (import ../lib.nix);
let
  iohk-pkgs = import ../default.nix {};
  mkHydra = extraImport: { config, pkgs, ... }: {
    _file = ./infrastructure.nix;
    # On first setup:

    # Locally: $ ssh-keygen -C "hydra@hydra.example.org" -N "" -f static/id_buildfarm
    # On Hydra: $ /run/current-system/sw/bin/hydra-create-user alice --full-name 'Alice Q. User' --email-address 'alice@example.org' --password foobar --role admin

    imports = [
      ../modules/common.nix
      ../modules/hydra-slave.nix
      ../modules/hydra-master-common.nix
      extraImport
    ];
  };
  mkHydraBuildSlave = { config, name, pkgs, ... }: {
    imports = [
      ../modules/common.nix
      ../modules/hydra-slave.nix
    ];
  };
in {
  hydra        = mkHydra ../modules/hydra-master-main.nix;
  mantis-hydra = mkHydra ../modules/hydra-master-mantis.nix;

  cardano-deployer = { config, pkgs, ... }: {
    imports = [
      ../modules/common.nix
    ];

    environment.systemPackages = [ iohk-pkgs.iohk-ops ];

    networking.firewall.allowedTCPPortRanges = [
      { from = 24962; to = 25062; }
    ];
  };

  bors-ng = { config, pkgs, ...}: {
    imports = [
      ../modules/common.nix
      ./bors-ng.nix
    ];
  };
}
