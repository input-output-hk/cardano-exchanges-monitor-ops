pkgs:
let
  requireEnv = name:
    let value = builtins.getEnv name;
    in if value == "" then
      abort "${name} environment variable is not set"
    else
      value;
in {

  static = import ./static;

  deploymentName = "${builtins.baseNameOf ./.}";

  environmentName = pkgs.globals.deploymentName;

  dnsZone = "dev.iohkdev.io";
  domain = "${pkgs.globals.deploymentName}.${pkgs.globals.dnsZone}";

  environments = pkgs.iohkNix.cardanoLib.environments;

  environmentConfig = pkgs.globals.environments.${pkgs.globals.environmentName};

  deployerIp = requireEnv "DEPLOYER_IP";

  extraPrometheusExportersPorts = [];
}
