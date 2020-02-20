{ pkgs, lib, config, ... }:

let
  cfg = config.services.exchanges-monitor;
in {
  options = {
    services.exchanges-monitor = {
      enable = lib.mkEnableOption "exchange monitor";
    };
  };
  config = lib.mkIf cfg.enable {
    users.users.exchanges-monitor = {
      home = "/var/empty";
      isSystemUser = true;
    };
    systemd.services.exchanges-monitor = {
      wantedBy = [ "multi-user.target" ];
      script = ''
        exec exchanges-monitor
      '';
      serviceConfig = {
        User = "exchanges-monitor";
        Restart = "always";
        RestartSec = "15s";
      };
    };
    services.prometheus2.scrapeConfigs = [
      {
        job_name = "exchanges-monitor";
        scrape_interval = "60s";
        metrics_path = "/";
        static_configs = [
          {
            targets = [
              "localhost:8000"
            ];
            labels = { alias = "exchanges-monitor"; };
          }
        ];
      }
    ];
  };
}
