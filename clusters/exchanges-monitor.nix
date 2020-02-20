{ targetEnv
, medium
, xlarge
, xlarge-monitor
, ...
}:
with (import ../nix {});
let

  nodes = mapAttrs  (_: mkNode) {
    monitoring = {
      deployment.ec2.region = "eu-central-1";
      imports = [
        xlarge-monitor
        roles.monitor
        ../modules/monitoring-cardano.nix
      ];
      node = {
        roles.isMonitor = true;
        org = "IOHK";
      };

      services.prometheus = {
        scrapeConfigs = [
          # TODO: remove once explorer exports metrics at path `/metrics`
          {
            job_name = "explorer-exporter";
            scrape_interval = "10s";
            metrics_path = "/metrics2/exporter";
            static_configs = [{
              targets = [ "explorer-ip" ];
              labels = { alias = "explorer-exporter"; };
            }];
          }
          # TODO: remove once explorer python api is deprecated
          {
            job_name = "explorer-python-api";
            scrape_interval = "10s";
            metrics_path = "/metrics/explorer-python-api";
            static_configs = [{
              targets = [ "explorer-ip" ];
              labels = { alias = "explorer-python-api"; };
            }];
          }
        ];
      };
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
