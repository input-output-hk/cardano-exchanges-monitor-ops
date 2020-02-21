{ targetEnv
, medium
, xlarge
, xlarge-monitor
, ...
}:
with (import ../nix {});
let

  inherit (lib) recursiveUpdate mapAttrs listToAttrs imap1;
  inherit (iohk-ops-lib) roles modules

  nodes = mapAttrs  (_: mkNode) {
    monitoring = {
      deployment.ec2.region = "eu-central-1";
      imports = [
        xlarge-monitor
        roles.monitor
        ../modules/monitoring-exchanges.nix
        ../modules/exchanges-monitor-service.nix
      ];
      node = {
        roles.isMonitor = true;
        org = "IOHK";
      };

      services.monitoring-services.logging = false;
    };
  };

  mkNode = args:
    recursiveUpdate {
      deployment.targetEnv = targetEnv;
      nixpkgs.overlays = pkgs.cardano-ops-overlays;
    } args;

in {
  network.description = "Exchanges monitoring cluster - ${globals.deploymentName}";
  network.enableRollback = true;
} // nodes
